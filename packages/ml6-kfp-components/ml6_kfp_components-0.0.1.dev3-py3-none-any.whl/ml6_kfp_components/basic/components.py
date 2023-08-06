from typing import NamedTuple

from kfp.v2 import dsl
from kfp.v2.dsl import Metrics, Model, Output, Artifact, Input

import ml6_kfp_components

BASE_IMAGE = f"{ml6_kfp_components.GCP_CONTAINER_REPO}/basic"
TAG = ml6_kfp_components.__version__


@dsl.component(base_image=f"{BASE_IMAGE}:{TAG}")
def AddServingConfigOp(
        model: Input[Model],
        configured_model: Output[Artifact],
        serving_config: dict,
):
    from copy import copy

    configured_model.uri = model.uri
    configured_model.metadata = copy(model.metadata)
    configured_model.metadata.update(serving_config)


@dsl.component(base_image=f"{BASE_IMAGE}:{TAG}")
def AddModelToTritonRepoOp(
        model_artifact: Input[Model],
        model_config: Input[Artifact],
        model_repo: str,
        model_name: str,
        model_version: int,
        model: Output[Model],
        model_subdir: str = ""
):
    """Adds a model artifact to a triton model registry.

    Args:
        model_artifact: the model artifact to move to the triton model repository
        model_config: the triton config for the model
        model_repo: gcs path to the root of the target model repository
        model_name: the model name for the model artifact
        model_version: the version under which to save the model
        model: the output artifact handle for the model in the triton repository
        model_subdir: optional sub-directory of the model under the version
    """
    from pathlib import Path
    import shutil

    model_artifact_uri_fuse = model_artifact.uri.replace("gs://", "/gcs/")
    model_config_uri_fuse = model_config.uri.replace("gs://", "/gcs/")
    model_repo_fuse = model_repo.replace("gs://", "/gcs/")

    config_path = Path(model_config_uri_fuse)
    model_source = Path(model_artifact_uri_fuse)

    target_path = Path(model_repo_fuse, model_name)
    if config_path.exists():
        target_path.mkdir(parents=True, exist_ok=True)
        shutil.copy(config_path, target_path / "config.pbtxt")

    target_path = target_path / str(model_version)
    if target_path.exists():
        shutil.rmtree(target_path)

    target_path.mkdir(parents=True, exist_ok=True)
    target_path = target_path / model_subdir
    shutil.copytree(model_source, target_path, dirs_exist_ok=True)

    model.uri = model_repo
    model.metadata = model_artifact.metadata


@dsl.component(base_image=f"{BASE_IMAGE}:{TAG}")
def GetWorkerPoolSpecsOp(
        worker_pool_specs: list,
        args: dict = {},
        hyperparams: dict = {},
        env: dict = {},
) -> list:
    for spec in worker_pool_specs:
        if "args" not in spec["container_spec"]:
            spec["container_spec"]["args"] = []
        for k, v in args.items():
            spec["container_spec"]["args"].append(f"--{k.replace('_', '-')}={v}")
        for k, v in hyperparams.items():
            spec["container_spec"]["args"].append(f"--{k.replace('_', '-')}={v}")

        if env:
            if "env" not in spec["container_spec"]:
                spec["container_spec"]["env"] = []
            for k, v in env.items():
                spec["container_spec"]["env"].append(dict(name=k, value=v))

    return worker_pool_specs


@dsl.component(base_image=f"{BASE_IMAGE}:{TAG}")
def GetCustomJobResultsOp(
        project: str,
        location: str,
        job_resource: str,
        model: Output[Model],
        checkpoints: Output[Artifact],
        metrics: Output[Metrics],
):
    import json
    from pathlib import Path
    import google.cloud.aiplatform as aip
    from google.protobuf.json_format import Parse
    from google_cloud_pipeline_components.proto.gcp_resources_pb2 import GcpResources

    aip.init(project=project, location=location)

    training_gcp_resources = Parse(job_resource, GcpResources())
    custom_job_id = training_gcp_resources.resources[0].resource_uri
    custom_job_name = custom_job_id[custom_job_id.find("project"):]

    job = aip.CustomJob.get(custom_job_name)
    job_resource = job.gca_resource
    job_base_dir = f"{job_resource.job_spec.base_output_directory.output_uri_prefix}/{job.name}"

    job_base_dir_fuse = Path(job_base_dir.replace("gs://", "/gcs/"))
    model_uri_fuse = job_base_dir_fuse / "model"
    checkpoints_uri_fuse = job_base_dir_fuse / "checkpoints"
    metrics_uri_fuse = job_base_dir_fuse / "metrics"

    with open(model_uri_fuse / "metadata.json") as fh:
        model_metadata = json.load(fh)

    with open(metrics_uri_fuse / "metrics.json") as fh:
        metrics_dict = json.load(fh)

    for k, v in metrics_dict.items():
        metrics.log_metric(k, v)

    model.metadata = model_metadata

    model.uri = str(model_uri_fuse).replace("/gcs/", "gs://")
    checkpoints.uri = str(checkpoints_uri_fuse).replace("/gcs/", "gs://")
    metrics.uri = str(metrics_uri_fuse).replace("/gcs/", "gs://")


@dsl.component(base_image=f"{BASE_IMAGE}:{TAG}")
def GetHyperparameterTuningJobResultsOp(
        project: str, location: str, job_resource: str,
        study_spec_metrics: list, trials: Output[Artifact]
) -> NamedTuple('outputs', [('best_params', dict)]):  # noqa: F821
    import google.cloud.aiplatform as aip
    from google_cloud_pipeline_components.proto.gcp_resources_pb2 import GcpResources
    from google.protobuf.json_format import Parse
    from google.cloud.aiplatform_v1.types import study

    aip.init(project=project, location=location)

    gcp_resources_proto = Parse(job_resource, GcpResources())
    tuning_job_id = gcp_resources_proto.resources[0].resource_uri
    tuning_job_name = tuning_job_id[tuning_job_id.find("project"):]

    job = aip.HyperparameterTuningJob.get(tuning_job_name)
    job_resource = job.gca_resource
    job_base_dir = f"{job_resource.trial_job_spec.base_output_directory.output_uri_prefix}/" \
                   f"{job.name}"

    trials.uri = job_base_dir

    if len(study_spec_metrics) > 1:
        raise RuntimeError(
            "Unable to determine best parameters for multi-objective hyperparameter tuning."
        )

    metric = study_spec_metrics[0]["metric_id"]
    goal = study_spec_metrics[0]["goal"]
    if goal == study.StudySpec.MetricSpec.GoalType.MAXIMIZE:
        best_fn = max
        goal_name = "maximize"
    elif goal == study.StudySpec.MetricSpec.GoalType.MINIMIZE:
        best_fn = min
        goal_name = "minimize"
    best_trial = best_fn(
        job_resource.trials,
        key=lambda trial: trial.final_measurement.metrics[0].value
    )

    trials.metadata = dict(
        metric=metric,
        goal=goal_name,
        num_trials=len(job_resource.trials),
        best_metric_value=best_trial.final_measurement.metrics[0].value
    )

    from collections import namedtuple
    output = namedtuple('outputs', ['best_params'])
    return output(best_params={p.parameter_id: p.value for p in best_trial.parameters})
