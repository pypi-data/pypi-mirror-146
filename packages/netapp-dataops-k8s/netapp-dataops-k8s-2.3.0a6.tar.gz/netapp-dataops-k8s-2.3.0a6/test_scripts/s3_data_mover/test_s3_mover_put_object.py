"""Tests for the S3 Data Mover put functionality."""
import time

import boto3

from netapp_dataops.k8s.data_movers.s3 import S3DataMover
from test_scripts.utilities import (
    verify_job_succeeds
)


def test_s3_put_object_without_directory(pvc_with_data,
                                         s3_bucket_empty,
                                         k8s_s3_secret,
                                         k8s_namespace,
                                         k8s_cleanup_jobs,
                                         s3_resource,
                                         config_data):
    """Test the put_object method with a single valid object without relative directory.

    Requirements:
        * Working K8s cluster with PVC support
        * Working S3 object storage service

    Dependencies
        * A PVC volume with files
        * An empty S3 bucket
        * A valid S3 Config Secret on the K8s cluster

    Test Steps:
        * Run the put_object method
        * Verify the job completes in a timely manner.
        * Verify the object exists in S3 at the expected location.

    :param pvc_with_data: Fixture providing the PVC volume with files.
    :param s3_bucket_empty: Fixture providing the empty S3 bucket.
    :param k8s_s3_secret: Fixture providing the S3 config secret.
    :param k8s_namespace: Fixture providing the name of the namespace to use.
    :param k8s_cleanup_jobs: Fixture to cleanup created jobs.
    :param s3_resource: Fixture providing Boto3 resource object.
    :param config_data: Fixture providing the raw configuration data.
    """
    print("Running test_s3_put_object_single_valid")

    s3_protocol = config_data['s3_protocol']
    if s3_protocol == 'https':
        use_https = True
    else:
        use_https = False

    # See the implementation of pvc_with_data for valid files
    object_name = "one.txt"

    data_mover = S3DataMover(
        s3_host=config_data['s3_host'],
        s3_port=config_data['s3_port'],
        use_https=use_https,
        verify_certificates=config_data['s3_verify_certs'],
        namespace=k8s_namespace,
        credentials_secret=k8s_s3_secret
    )

    job = data_mover.put_object(bucket=s3_bucket_empty, pvc=pvc_with_data, file_location=object_name,
                                object_key=object_name)

    verify_job_succeeds(data_mover=data_mover, job=job, timeout=60)

    bucket = s3_resource.Bucket(name=s3_bucket_empty)
    bucket_objects = bucket.objects.all()
    key_found = False
    for s3_object in bucket_objects:
        print("S3 object: {}".format(s3_object))
        if s3_object.key == object_name:
            key_found = True
            break
    assert key_found


def test_s3_put_object_with_directory(pvc_with_data,
                                      s3_bucket_empty,
                                      k8s_s3_secret,
                                      k8s_namespace,
                                      k8s_cleanup_jobs,
                                      s3_resource,
                                      config_data):
    """Test the put_object method with a valid object with relative directory.

    :param pvc_with_data: Fixture providing the PVC volume with files.
    :param s3_bucket_empty: Fixture providing the empty S3 bucket.
    :param k8s_s3_secret: Fixture providing the S3 config secret.
    :param k8s_namespace: Fixture providing the name of the namespace to use.
    :param k8s_cleanup_jobs: Fixture to cleanup created jobs.
    :param s3_resource: Fixture providing Boto3 resource object.
    :param config_data: Fixture providing the raw configuration data.
    """
    s3_protocol = config_data['s3_protocol']
    if s3_protocol == 'https':
        use_https = True
    else:
        use_https = False

    # See the implementation of pvc_with_data for valid files
    # For this test we want to validate transferring a file within a directory.
    object_name = "layer2/three.txt"

    data_mover = S3DataMover(
        s3_host=config_data['s3_host'],
        s3_port=config_data['s3_port'],
        use_https=use_https,
        verify_certificates=config_data['s3_verify_certs'],
        namespace=k8s_namespace,
        credentials_secret=k8s_s3_secret
    )

    job = data_mover.put_object(bucket=s3_bucket_empty, pvc=pvc_with_data, file_location=object_name,
                                object_key=object_name)

    verify_job_succeeds(data_mover=data_mover, job=job, timeout=60)

    bucket = s3_resource.Bucket(name=s3_bucket_empty)
    bucket_objects = bucket.objects.all()
    key_found = False
    for s3_object in bucket_objects:
        print("S3 object: {}".format(s3_object))
        if s3_object.key == object_name:
            key_found = True
            break
    assert key_found
