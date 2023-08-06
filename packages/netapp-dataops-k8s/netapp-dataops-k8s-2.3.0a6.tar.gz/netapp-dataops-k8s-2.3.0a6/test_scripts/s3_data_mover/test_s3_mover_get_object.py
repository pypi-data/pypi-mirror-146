"""Tests for S3DataMover get_object method."""
import time

from kubernetes.client import (
    CoreV1Api,
)
from netapp_dataops.k8s.data_movers.s3 import S3DataMover
from test_scripts.utilities import (
    get_data_pod,
    verify_job_succeeds,
    wait_for_pod_completion
)


def test_s3_get_object_without_directory(k8s_pvc,
                                         s3_bucket_full,
                                         k8s_s3_secret,
                                         k8s_namespace,
                                         k8s_client,
                                         namespace_name,
                                         s3_resource,
                                         config_data,
                                         k8s_cleanup_jobs):
    """Test the get_object method with a bucket with files and a PVC.

    Requirements:
        * Working K8s cluster with PVC support
        * Working S3 object storage service

    Dependencies
        * A new (empty) PVC volume
        * An S3 bucket with some objects
        * A valid S3 Config Secret on the K8s cluster

    Variations:
        * The k8s_namespace fixture is parameterized.
            * Value of None is verifying the S3DataMover class uses the default namespace
                if no namespace is explicitly provided.
            * Other values verify the S3DataMover class uses the explicitly named namespace.

    Test Steps:
        * Run the S3DataMover get_object method
        * Verify the job name is returned from the get_bucket method
        * Verify the job completes in a reasonable time
        * Verify the job succeeds
        * Verify the file exists in the PVC

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

    object_name = "bravo.txt"
    job = data_mover.get_object(bucket=s3_bucket_full, pvc=k8s_pvc, object_key=object_name)
    assert job

    initial_status = data_mover.get_job_status(job=job)
    # This verifies the job name is correct and we can get the status
    assert initial_status

    verify_job_succeeds(data_mover=data_mover, job=job, timeout=60)

    # Verify the file exists on the PVC
    api_instance = CoreV1Api(api_client=k8s_client)
    verify_command = "ls /mnt/data"
    pod_request = get_data_pod(namespace=namespace_name, pvc=k8s_pvc, command=verify_command)
    verify_pod = api_instance.create_namespaced_pod(namespace=namespace_name, body=pod_request)
    pod_name = verify_pod.metadata.name
    print("Using pod {} to verify the file was copied.".format(pod_name))

    wait_for_pod_completion(client=k8s_client, namespace=namespace_name, pod=pod_name, timeout=60)
    pod_log = api_instance.read_namespaced_pod_log(name=pod_name, namespace=namespace_name)
    print(f"Pod log: \n{pod_log}")
    assert object_name in pod_log


def test_s3_get_object_with_directory(k8s_pvc,
                                      s3_bucket_full,
                                      k8s_s3_secret,
                                      k8s_namespace,
                                      k8s_client,
                                      namespace_name,
                                      s3_resource,
                                      config_data,
                                      k8s_cleanup_jobs):
    """Test the get_object method with an object with a directory in the name.

    Requirements:
        * Working K8s cluster with PVC support
        * Working S3 object storage service

    Dependencies
        * A new (empty) PVC volume
        * An S3 bucket with an object with a directory name.
        * A valid S3 Config Secret on the K8s cluster

    Variations:
        * The k8s_namespace fixture is parameterized.
            * Value of None is verifying the S3DataMover class uses the default namespace
                if no namespace is explicitly provided.
            * Other values verify the S3DataMover class uses the explicitly named namespace.

    Test Steps:
        * Run the S3DataMover get_object method for the object within a directory in the bucket.
        * Verify the job name is returned from the get_bucket method
        * Verify the job completes in a reasonable time
        * Verify the job succeeds
        * Verify the file exists in the PVC

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

    object_name = "planets/mercury.txt"
    job = data_mover.get_object(bucket=s3_bucket_full, pvc=k8s_pvc, object_key=object_name)
    assert job

    initial_status = data_mover.get_job_status(job=job)
    # This verifies the job name is correct and we can get the status
    assert initial_status

    verify_job_succeeds(data_mover=data_mover, job=job, timeout=60)

    # Verify the file exists on the PVC
    api_instance = CoreV1Api(api_client=k8s_client)
    verify_command = "find /mnt/data -type f"
    pod_request = get_data_pod(namespace=namespace_name, pvc=k8s_pvc, command=verify_command)
    verify_pod = api_instance.create_namespaced_pod(namespace=namespace_name, body=pod_request)
    pod_name = verify_pod.metadata.name
    print("Using pod {} to verify the file was copied.".format(pod_name))

    wait_for_pod_completion(client=k8s_client, namespace=namespace_name, pod=pod_name, timeout=60)
    pod_log = api_instance.read_namespaced_pod_log(name=pod_name, namespace=namespace_name)
    print(f"Pod log: \n{pod_log}")
    assert object_name in pod_log


def test_s3_get_object_with_file_location(k8s_pvc,
                                          s3_bucket_full,
                                          k8s_s3_secret,
                                          k8s_namespace,
                                          k8s_client,
                                          namespace_name,
                                          s3_resource,
                                          config_data,
                                          k8s_cleanup_jobs):
    """Test the get_object method with the file location specified.

    Requirements:
        * Working K8s cluster with PVC support
        * Working S3 object storage service

    Dependencies
        * A new (empty) PVC volume
        * An S3 bucket with an object.
        * A valid S3 Config Secret on the K8s cluster

    Variations:
        * The k8s_namespace fixture is parameterized.
            * Value of None is verifying the S3DataMover class uses the default namespace
                if no namespace is explicitly provided.
            * Other values verify the S3DataMover class uses the explicitly named namespace.

    Test Steps:
        * Run the S3DataMover get_object method for the object with a file location specified.
        * Verify the job name is returned from the get_bucket method
        * Verify the job completes in a reasonable time
        * Verify the job succeeds
        * Verify the file exists in the PVC

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

    object_name = "planets/mercury.txt"
    destination = "planet_names/mercury.txt"
    job = data_mover.get_object(bucket=s3_bucket_full, pvc=k8s_pvc, object_key=object_name, file_location=destination)
    assert job

    initial_status = data_mover.get_job_status(job=job)
    # This verifies the job name is correct and we can get the status
    assert initial_status

    verify_job_succeeds(data_mover=data_mover, job=job, timeout=60)

    # Verify the file exists on the PVC
    api_instance = CoreV1Api(api_client=k8s_client)
    verify_command = "find /mnt/data -type f"
    pod_request = get_data_pod(namespace=namespace_name, pvc=k8s_pvc, command=verify_command)
    verify_pod = api_instance.create_namespaced_pod(namespace=namespace_name, body=pod_request)
    pod_name = verify_pod.metadata.name
    print("Using pod {} to verify the file was copied.".format(pod_name))

    wait_for_pod_completion(client=k8s_client, namespace=namespace_name, pod=pod_name, timeout=60)
    pod_log = api_instance.read_namespaced_pod_log(name=pod_name, namespace=namespace_name)
    print(f"Pod log: \n{pod_log}")
    assert destination in pod_log
