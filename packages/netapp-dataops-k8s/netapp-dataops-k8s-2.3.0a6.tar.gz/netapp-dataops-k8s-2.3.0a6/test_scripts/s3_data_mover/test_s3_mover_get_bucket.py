"""Tests for S3DataMover get_bucket method."""
from kubernetes.client import (
    CoreV1Api,
)

from netapp_dataops.k8s.data_movers.s3 import S3DataMover
from test_scripts.utilities import (
    get_data_pod,
    verify_job_succeeds,
    wait_for_pod_completion
)


def test_s3_get_bucket_valid(k8s_pvc,
                             s3_bucket_full,
                             k8s_s3_secret,
                             k8s_namespace,
                             k8s_client,
                             namespace_name,
                             s3_resource,
                             config_data,
                             k8s_cleanup_jobs):
    """Test the get_bucket method with a bucket with files and a PVC.

    Requirements:
        * Working K8s cluster with PVC support
        * Working S3 object storage service

    Dependencies
        * A new (empty) PVC volume
        * An S3 bucket with some objects
        * A valid S3 Config Secret on the K8s cluster

    Test Steps:
        * Run the S3DataMover get_bucket method
        * Verify the job name is returned from the get_bucket method
        * Verify the job completes in a reasonable time
        * Verify the job succeeds
        * Verify the files exist in the PVC

    :param k8s_pvc:
    :param s3_bucket_full:
    :param k8s_s3_secret:
    :param k8s_namespace:
    :param s3_resource:
    """
    s3_protocol = config_data['s3_protocol']
    if s3_protocol == 'https':
        use_https = True
    else:
        use_https = False

    data_mover = S3DataMover(
        s3_host=config_data['s3_host'],
        s3_port=config_data['s3_port'],
        use_https=use_https,
        verify_certificates=config_data['s3_verify_certs'],
        namespace=k8s_namespace,
        credentials_secret=k8s_s3_secret
    )

    job = data_mover.get_bucket(bucket=s3_bucket_full, pvc=k8s_pvc)
    assert job

    initial_status = data_mover.get_job_status(job=job)
    # This verifies the job name is correct and we can get the status
    assert initial_status

    verify_job_succeeds(data_mover=data_mover, job=job, timeout=30)

    # Verify the files exist in the PVC
    api_instance = CoreV1Api(api_client=k8s_client)
    verify_command = "find /mnt/data -type f"
    pod_request = get_data_pod(namespace=namespace_name, pvc=k8s_pvc, command=verify_command)
    verify_pod = api_instance.create_namespaced_pod(namespace=namespace_name, body=pod_request)
    pod_name = verify_pod.metadata.name
    print("Using pod {} to verify the file was copied.".format(pod_name))

    wait_for_pod_completion(client=k8s_client, namespace=namespace_name, pod=pod_name, timeout=60)
    pod_log = api_instance.read_namespaced_pod_log(name=pod_name, namespace=namespace_name)
    file_names = ['alpha.txt', 'bravo.txt', 'mercury.txt']
    for txt in file_names:
        assert txt in pod_log


def test_s3_get_bucket_with_pvc_dir(k8s_pvc,
                                    s3_bucket_full,
                                    k8s_s3_secret,
                                    k8s_namespace,
                                    k8s_client,
                                    namespace_name,
                                    s3_resource,
                                    config_data,
                                    k8s_cleanup_jobs):
    """Test the get_bucket method with a pvc directory specified.

    Requirements:
        * Working K8s cluster with PVC support
        * Working S3 object storage service

    Dependencies
        * A new (empty) PVC volume
        * An S3 bucket with some objects
        * A valid S3 Config Secret on the K8s cluster

    Test Steps:
        * Run the S3DataMover get_bucket method with a pvc_dir specified.
        * Verify the job name is returned from the get_bucket method
        * Verify the job completes in a reasonable time
        * Verify the job succeeds
        * Verify the files exist in the PVC within the directory specified.

    :param k8s_pvc:
    :param s3_bucket_full:
    :param k8s_s3_secret:
    :param k8s_namespace:
    :param s3_resource:
    """
    s3_protocol = config_data['s3_protocol']
    if s3_protocol == 'https':
        use_https = True
    else:
        use_https = False

    data_mover = S3DataMover(
        s3_host=config_data['s3_host'],
        s3_port=config_data['s3_port'],
        use_https=use_https,
        verify_certificates=config_data['s3_verify_certs'],
        namespace=k8s_namespace,
        credentials_secret=k8s_s3_secret
    )

    target_dir = "source/data"
    job = data_mover.get_bucket(bucket=s3_bucket_full, pvc=k8s_pvc, pvc_dir=target_dir)
    assert job

    initial_status = data_mover.get_job_status(job=job)
    # This verifies the job name is correct and we can get the status
    assert initial_status

    verify_job_succeeds(data_mover=data_mover, job=job, timeout=30)

    # Verify the files exist in the PVC
    api_instance = CoreV1Api(api_client=k8s_client)
    verify_command = "find /mnt/data -type f"
    pod_request = get_data_pod(namespace=namespace_name, pvc=k8s_pvc, command=verify_command)
    verify_pod = api_instance.create_namespaced_pod(namespace=namespace_name, body=pod_request)
    pod_name = verify_pod.metadata.name
    print("Using pod {} to verify the file was copied.".format(pod_name))

    wait_for_pod_completion(client=k8s_client, namespace=namespace_name, pod=pod_name, timeout=60)
    pod_log = api_instance.read_namespaced_pod_log(name=pod_name, namespace=namespace_name)
    print(f"pod_log: \n{pod_log}")
    file_names = ['source/data/alpha.txt', 'source/data/bravo.txt', 'source/data/planets/mercury.txt']
    for txt in file_names:
        assert txt in pod_log
