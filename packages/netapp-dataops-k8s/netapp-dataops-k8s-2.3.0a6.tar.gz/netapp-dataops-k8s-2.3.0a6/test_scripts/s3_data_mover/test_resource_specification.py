"""Tests for S3DataMover resource specification."""
import time

import pytest
from kubernetes.client import (
    CoreV1Api,
)

from netapp_dataops.k8s.data_movers.s3 import S3DataMover


@pytest.fixture(scope="function")
def default_namespace(namespace_name):
    if namespace_name != "default":
        pytest.skip("Skipping multiple namespace testing.")
    yield namespace_name


def test_valid_resource_limits(k8s_pvc,
                               s3_bucket_full,
                               k8s_s3_secret,
                               k8s_client,
                               default_namespace,
                               config_data,
                               k8s_cleanup_jobs):
    """Test the ability to set valid cpu and memory limits for the S3DataMover job/pod.

    Initial baselining of the minio/mc container showed cpu and memory usage roughly
    at the following levels.
        cpu = 2539685n
        memory =844Ki

    Test Steps:
        * Instantiate an S3DataMover object providing resource limits but not requests
        * Start a data movement operation (any operation is sufficient)
        * Get the pod info for the data movement pod and verify resource limits and requests
            are set.

    :param k8s_pvc:
    :param s3_bucket_full:
    :param k8s_s3_secret:
    :param k8s_client:
    :param default_namespace:
    :param config_data:
    :param k8s_cleanup_jobs:
    """
    s3_protocol = config_data['s3_protocol']
    if s3_protocol == 'https':
        use_https = True
    else:
        use_https = False

    memory_limit = "10000Ki"
    cpu_limit = "500m"

    data_mover = S3DataMover(
        s3_host=config_data['s3_host'],
        s3_port=config_data['s3_port'],
        use_https=use_https,
        verify_certificates=config_data['s3_verify_certs'],
        namespace=default_namespace,
        credentials_secret=k8s_s3_secret,
        cpu_limit=cpu_limit,
        memory_limit=memory_limit
    )

    job = data_mover.get_bucket(bucket=s3_bucket_full, pvc=k8s_pvc)
    assert job

    # Wait for the job to be created
    time.sleep(10)

    # Verify the resource limits were set
    pod_selection = f"job-name={job}"
    core_api = CoreV1Api(api_client=k8s_client)
    job_pods = core_api.list_namespaced_pod(namespace=default_namespace, label_selector=pod_selection)

    # We expect to find one pod associated with the job
    pod_count = len(job_pods.items)
    assert pod_count == 1

    pod_resources = job_pods.items[0].spec.containers[0].resources
    assert pod_resources.limits['cpu'] == cpu_limit
    assert pod_resources.limits['memory'] == memory_limit

    # When we only set limits, requests get set to the limit value
    assert pod_resources.requests['cpu'] == cpu_limit
    assert pod_resources.requests['memory'] == memory_limit


def test_valid_resource_requests(k8s_pvc,
                                 s3_bucket_full,
                                 k8s_s3_secret,
                                 k8s_client,
                                 default_namespace,
                                 config_data,
                                 k8s_cleanup_jobs):
    """Test the ability to set valid cpu and memory requests for a S3DataMover job/pod.

    Test Steps:
        * Instantiate an S3DataMover object providing valid cpu and memory requests
        * Start a data movement operation (any operation will work)
        * Verify the data movement pod's container is configured with the resource requests
        * Verify there are no resource limits since none were specified

    :param k8s_pvc:
    :param s3_bucket_full:
    :param k8s_s3_secret:
    :param k8s_client:
    :param default_namespace:
    :param config_data:
    :param k8s_cleanup_jobs:
    """
    s3_protocol = config_data['s3_protocol']
    if s3_protocol == 'https':
        use_https = True
    else:
        use_https = False

    requested_memory = "8000Ki"
    requested_cpu = "300m"

    data_mover = S3DataMover(
        s3_host=config_data['s3_host'],
        s3_port=config_data['s3_port'],
        use_https=use_https,
        verify_certificates=config_data['s3_verify_certs'],
        namespace=default_namespace,
        credentials_secret=k8s_s3_secret,
        cpu_request=requested_cpu,
        memory_request=requested_memory
    )

    job = data_mover.get_bucket(bucket=s3_bucket_full, pvc=k8s_pvc)
    assert job

    # Wait for the job to be created
    time.sleep(10)

    # Verify the resource limits were set
    pod_selection = f"job-name={job}"
    core_api = CoreV1Api(api_client=k8s_client)
    job_pods = core_api.list_namespaced_pod(namespace=default_namespace, label_selector=pod_selection)

    # We expect to find one pod associated with the job
    pod_count = len(job_pods.items)
    assert pod_count == 1

    pod_resources = job_pods.items[0].spec.containers[0].resources
    assert pod_resources.requests['cpu'] == requested_cpu
    assert pod_resources.requests['memory'] == requested_memory

    # When only the requests are set the limits should have no value
    assert pod_resources.limits is None
