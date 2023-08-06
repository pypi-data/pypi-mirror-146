"""Miscellaneous utility functions for tests."""
from datetime import datetime
import time

from kubernetes.client import (
    ApiClient,
    CoreV1Api,
    V1Container,
    V1ObjectMeta,
    V1PersistentVolumeClaimVolumeSource,
    V1Pod,
    V1PodSpec,
    V1Volume,
    V1VolumeMount,
)

from netapp_dataops.k8s.data_movers.s3 import (
    S3DataMover
)


def get_data_pod(namespace: str, pvc: str, command: str):
    """Get a POD definition with a mounted PVC.

    This is intended to be used for as a utility pod to create or verify data on the pvc.

    :param namespace:
    :param pvc:
    :param command:
    :return: The V1Pod object.
    """
    mount_path = "/mnt/data"
    data_volume_name = "dataops-test-volume"

    pod_request = V1Pod(
        metadata=V1ObjectMeta(
            namespace=namespace,
            generate_name="dataops-datapod-",
            labels={"created-by": "ntap-dsutil"}
        ),
        spec=V1PodSpec(
            containers=[
                V1Container(
                    name="dataops-test-data",
                    image="busybox:stable-musl",
                    volume_mounts=[V1VolumeMount(mount_path=mount_path, name=data_volume_name)],
                    command=["sh"],
                    args=["-c", command]
                )
            ],
            volumes=[
                V1Volume(
                    name=data_volume_name,
                    persistent_volume_claim=V1PersistentVolumeClaimVolumeSource(
                        claim_name=pvc
                    )
                )
            ],
            restart_policy="Never"
        )
    )
    return pod_request


def check_timeout(timeout: int, start_time: datetime):
    elapsed = datetime.now() - start_time
    if elapsed.seconds > timeout:
        raise TimeoutError()


def verify_job_succeeds(data_mover: S3DataMover, job: str, timeout: int):
    """Common code to verify a job succeeds.

    The common job status flow should be something like this.
    NotStarted -> Started -> Active -> Completed

    Completion can mean succeeded or failed. This function explicitly verifies an
    expectation of success.

    :param data_mover:
    :param job:
    :param timeout:
    """
    start_time = datetime.now()
    job_completed = False
    job_started = False

    while not job_started:
        check_timeout(timeout=timeout, start_time=start_time)
        time.sleep(1)
        job_started = data_mover.is_job_started(job=job)

    while not job_completed:
        check_timeout(timeout=timeout, start_time=start_time)
        if not data_mover.is_job_active(job=job):
            job_completed = True
            break
        else:
            time.sleep(1)

    assert data_mover.did_job_succeed(job=job)


def wait_for_pod_completion(client: ApiClient, namespace: str, pod: str, timeout: int):
    """Wait for a pod to reach a terminal status.

    This will check the phase of a Pod until a terminal phase is reached or the requested timeout
    is reached.

    :param client: The API Client for K8s.
    :param namespace: The namespace of the pod.
    :param pod: The name of the pod.
    :param timeout: The maximum number of seconds to wait. After this raise an error.
    """
    api_instance = CoreV1Api(api_client=client)
    running = True
    start = datetime.now()

    while running:
        time.sleep(1)
        pod_data: V1Pod = api_instance.read_namespaced_pod_status(name=pod, namespace=namespace)
        if pod_data.status.phase not in ["Pending", "Running"]:
            running = False
        else:
            current = datetime.now()
            elapsed = current - start
            if elapsed.seconds > timeout:
                print(f"Final pod status was {pod_data.status.phase}")
                raise TimeoutError()
