import base64
from datetime import datetime
import json
import time

from kubernetes import config
from kubernetes.client import (
    ApiClient,
    ApiException,
    BatchV1Api,
    CoreV1Api,
    V1Container,
    V1Namespace,
    V1ObjectMeta,
    V1PersistentVolumeClaim,
    V1PersistentVolumeClaimSpec,
    V1PersistentVolumeClaimVolumeSource,
    V1Pod,
    V1PodSpec,
    V1ResourceRequirements,
    V1Secret,
    V1Volume,
    V1VolumeMount,
)
import pytest


@pytest.fixture(scope="function", params=[None, "minio/mc:RELEASE.2021-06-13T17-48-22Z"])
def mover_image(request) -> str:
    """Fixture to provide a valid S3DataMover image tag to use.

    The value of None represents no specified image tag which is the default. In that case the latest
    minio mc image is used.

    When a string value is provided the S3DataMover will attempt to use that string as ts the image
    tag for the image to pull. This will only work if a valid minio mc image tag is provided.

    :param request: The pytest request object.
    :return: The value of the image to use when creating the S3DataMover object.
    """
    yield request.param


@pytest.fixture(scope="function")
def k8s_cleanup_jobs(k8s_client, namespace_name):
    """Fixture to remove any jobs created.

    :param k8s_client: Fixture providing the K8s client.
    :param k8s_namespace: Fixture providing the K8s namespace.
    """
    yield
    api_instance = BatchV1Api(api_client=k8s_client)
    selector = "created-by=ntap-dsutil"
    job_list = api_instance.list_namespaced_job(namespace=namespace_name,
                                                label_selector=selector)
    for v1_job in job_list.items:
        print("Cleanup removing job {}".format(v1_job.metadata.name))
        api_instance.delete_namespaced_job(name=v1_job.metadata.name, namespace=namespace_name)

    core_api = CoreV1Api(api_client=k8s_client)
    pod_list = core_api.list_namespaced_pod(namespace=namespace_name, label_selector=selector)
    for v1_pod in pod_list.items:
        print("Cleanup removing pod {}".format(v1_pod.metadata.name))
        try:
            core_api.delete_namespaced_pod(name=v1_pod.metadata.name, namespace=namespace_name)
        except Exception as error:
            print(f"Caught exception: {error}")
        # Pod deletion seems to take some time cleanup. This is the simple solution.
        time.sleep(10)


@pytest.fixture(scope="session")
def k8s_client(config_data) -> ApiClient:
    try:
        kube_file = config_data['kube_config_file']
        print(f"Loading K8s config from file {kube_file}")
        api_client = config.new_client_from_config(config_file=kube_file)
    except KeyError:
        # No kube config file specified, so try using the default
        print("Loading K8s config from the default location.")
        api_client = config.new_client_from_config()
    yield api_client


# @pytest.fixture(scope="session", params=[None])
@pytest.fixture(scope="session", params=[None, "dataops-test"])
def k8s_namespace(request, k8s_client) -> str:
    """Fixture to provide the name of a namespace to use.

    :param request: The pytest request.
    :param k8s_client: The fixture providing the k8s client.
    :return: The name of a namespace to use.
    """
    created_here = False
    core_api = CoreV1Api(api_client=k8s_client)
    if request.param is not None:
        body = V1Namespace(metadata=V1ObjectMeta(name=request.param))
        try:
            core_api.create_namespace(body=body)
            created_here = True
        except ApiException as api_error:
            error_body = json.loads(api_error.body)
            if error_body['reason'] != "AlreadyExists":
                raise api_error

    yield request.param

    if created_here:
        core_api.delete_namespace(name=request.param)


@pytest.fixture(scope="session")
def namespace_name(k8s_namespace):
    """Fixture to provide the explicit name of the namespace.

    This provides the name of the namespace to be used with verification functions.
    This translates the None name to the actual default name.

    :param k8s_namespace:
    :return: The namespace name
    """
    if k8s_namespace is None:
        name = 'default'
    else:
        name = k8s_namespace
    return name


def get_secret_encoding(value: str):
    """Get the required base64 encoding for a string for a K8s secret.

    :param value: The string to be encoded.
    :return: The base64 value
    """
    value_bytes = value.encode('ascii')
    return base64.b64encode(value_bytes).decode('ascii')


@pytest.fixture(scope="session")
def k8s_s3_secret(config_data, k8s_client, namespace_name) -> str:
    """Fixture to provide a K8s secret for use with S3 data movement.

    :param config_data: The config_data fixture.
    :param k8s_client: Fixture providing the K8s client.
    :param namespace_name: Fixture providing the K8s namespace.
    :return: The name of the K8s secret for S3 use.
    """
    s3_access_key = config_data['s3_access_key']
    s3_secret_key = config_data['s3_secret_key']
    secret_name = "dataops-test-secret"

    api_instance = CoreV1Api(api_client=k8s_client)
    secret_body = V1Secret(
        metadata=V1ObjectMeta(name=secret_name, namespace=namespace_name),
        data={'access_key': get_secret_encoding(s3_access_key),
              'secret_key': get_secret_encoding(s3_secret_key)}
    )
    api_instance.create_namespaced_secret(namespace=namespace_name, body=secret_body)

    yield secret_name

    try:
        api_instance.delete_namespaced_secret(name=secret_name, namespace=namespace_name)
    except ApiException:
        pass


@pytest.fixture(scope="session")
def k8s_storage_class(config_data) -> str:
    """Fixture to provide the storage class name.

    The configuration parameter is required for this value. There is no default.

    :param config_data: The config_data fixture.
    :return: The name of the storage class to use.
    """
    storage_class_name = config_data['storage_class_name']
    yield storage_class_name


@pytest.fixture(scope="function")
def k8s_pvc(k8s_client, namespace_name, k8s_storage_class):
    """Fixture to provide a PVC for testing.

    :param k8s_client: Fixture providing the K8s client.
    :param namespace_name: Fixture providing the namespace to use.
    :param k8s_storage_class: Fixture providing the storage class to use.
    :return: The name of the created PVC.
    """
    pvc_name = "dataops-test-pvc"
    storage_size = "2Gi"
    api_instance = CoreV1Api(api_client=k8s_client)
    pvc_body = V1PersistentVolumeClaim(
        metadata=V1ObjectMeta(name=pvc_name),
        spec=V1PersistentVolumeClaimSpec(
            access_modes=["ReadWriteMany"],
            resources=V1ResourceRequirements(requests={'storage': storage_size}),
            storage_class_name=k8s_storage_class
        )
    )
    # Loop for up to approximately 5 minutes if waiting for an existing volume to be removed
    for _ in range(30):
        try:
            api_instance.create_namespaced_persistent_volume_claim(namespace=namespace_name, body=pvc_body)
        except ApiException as api_error:
            error_body = json.loads(api_error.body)
            if error_body['reason'] == "AlreadyExists":
                print("Waiting for pvc to finish terminating.")
                time.sleep(10)
            else:
                raise
        else:
            break
    yield pvc_name

    # If the pod isn't removed this won't error but the PVC won't go away.
    api_instance.delete_namespaced_persistent_volume_claim(name=pvc_name, namespace=namespace_name,
                                                           grace_period_seconds=0)


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


@pytest.fixture(scope="function")
def pvc_with_data(k8s_client, config_data, namespace_name, k8s_pvc):
    """Setup a PVC with data to be used by a test.

    :return:
    """
    api_instance = CoreV1Api(api_client=k8s_client)
    mount_path = "/mnt/data"
    data_volume_name = "dataops-test-volume"
    pod_name = "dataops-test-create-volumedata"
    create_commands = [
        f"echo 'file1' > {mount_path}/one.txt",
        f"echo 'file2' > {mount_path}/two.txt",
        f"mkdir {mount_path}/layer2",
        f"mkdir {mount_path}/layer2/layer3",
        f"echo 'file3' > {mount_path}/layer2/three.txt",
        f"echo 'file4' > {mount_path}/layer2/layer3/four.txt"
    ]
    command = ";".join(create_commands)

    # Create POD to generate data on k8s_pvc
    pod_request = V1Pod(
        metadata=V1ObjectMeta(name=pod_name, namespace=namespace_name),
        spec=V1PodSpec(
            containers=[
                V1Container(
                    name="dataops-test-create-data",
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
                        claim_name=k8s_pvc
                    )
                )
            ],
            restart_policy="Never"
        )
    )

    pod: V1Pod = api_instance.create_namespaced_pod(namespace=namespace_name, body=pod_request)

    wait_for_pod_completion(client=k8s_client, namespace=namespace_name, pod=pod_name, timeout=60)

    yield k8s_pvc

    api_instance.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace_name)
