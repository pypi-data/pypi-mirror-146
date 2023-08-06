"""Tests for S3DataMover job deletion."""
import time

import pytest
from kubernetes.client import (
    ApiException,
    BatchV1Api,
)

from netapp_dataops.k8s.data_movers.s3 import S3DataMover

from test_scripts.utilities import (
    verify_job_succeeds,
)


def test_data_mover_job_deletion(k8s_pvc,
                                 s3_bucket_full,
                                 k8s_s3_secret,
                                 k8s_client,
                                 k8s_namespace,
                                 config_data,
                                 namespace_name,
                                 k8s_cleanup_jobs):
    """Test the ability to delete a job.

    Test Steps:
        * Use the S3DataMover to create a job (get_bucket)
        * Wait for the job to complete
        * Delete the job using the S3DataMover object's delete_job method
        * Verify the job has been removed from K8s

    :param k8s_pvc:
    :param s3_bucket_full:
    :param k8s_s3_secret:
    :param k8s_client:
    :param k8s_namespace:
    :param config_data:
    :param namespace_name: Provides the namespace name to use for verifications.
    :param k8s_cleanup_jobs:
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
        credentials_secret=k8s_s3_secret,
    )

    job = data_mover.get_bucket(bucket=s3_bucket_full, pvc=k8s_pvc)
    assert job

    # Let the job complete
    verify_job_succeeds(data_mover=data_mover, job=job, timeout=60)

    # Now delete the job from K8s
    data_mover.delete_job(job=job)

    # Wait for the job to be deleted
    time.sleep(10)

    # Verify the job has been removed
    api_instance = BatchV1Api(api_client=k8s_client)

    with pytest.raises(ApiException) as read_error:
        api_instance.read_namespaced_job(name=job, namespace=namespace_name)
    assert "Reason: Not Found" in str(read_error.value)
