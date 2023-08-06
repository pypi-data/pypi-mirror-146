"""Tests for S3DataMover put_bucket method."""
import os
import time

from netapp_dataops.k8s.data_movers.s3 import S3DataMover


def test_s3_put_bucket_valid(pvc_with_data,
                             s3_bucket_empty,
                             k8s_s3_secret,
                             k8s_namespace,
                             mover_image,
                             s3_resource,
                             config_data,
                             k8s_cleanup_jobs):
    """Test the put_bucket method with a PVC and valid empty bucket.

    NOTE: This test also validates specification of a valid image name.

    Requirements:
        * Working K8s cluster with PVC support
        * Working S3 object storage service

    Dependencies
        * A PVC volume with files
        * An empty S3 bucket
        * A valid S3 Config Secret on the K8s cluster

    Test Steps:
        * Run the S3DataMover put_object method
        * Verify the job name is returned from the put_object method
        * Verify the job completes in a reasonable time
        * Verify the job succeeds
        * Verify the files exist in the bucket

    :param pvc_with_data:
    :param s3_bucket_empty:
    :param k8s_s3_secret:
    :param k8s_namespace:
    :param mover_image:
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
        image_name=mover_image,
        credentials_secret=k8s_s3_secret
    )

    job = data_mover.put_bucket(bucket=s3_bucket_empty, pvc=pvc_with_data)
    assert job

    initial_status = data_mover.get_job_status(job=job)
    # This verifies the job name is correct and we can get the status
    assert initial_status

    job_completed = False
    for step in range(30):
        if not data_mover.is_job_active(job=job):
            job_completed = True
            assert data_mover.did_job_succeed(job=job)
            break
        else:
            time.sleep(2)
    # Verify the job completed and we didn't timeout of the loop
    assert job_completed

    # Verify the files exist in the bucket
    bucket = s3_resource.Bucket(name=s3_bucket_empty)
    bucket_objects = bucket.objects.all()

    pvc_filenames = ["one.txt", "two.txt", "three.txt"]
    for s3_object in bucket_objects:
        print("S3 object: {}".format(s3_object))
        # Note: put_bucket currently retains directory structures so keys may have dir names included
        key_base = os.path.basename(s3_object.key)
        print(f"Key basename: {key_base}")
        if key_base in pvc_filenames:
            pvc_filenames.remove(key_base)
    # Verify we found all the files
    assert not pvc_filenames


def test_s3_put_bucket_with_pvc_dir(pvc_with_data,
                                    s3_bucket_empty,
                                    k8s_s3_secret,
                                    k8s_namespace,
                                    mover_image,
                                    s3_resource,
                                    config_data,
                                    k8s_cleanup_jobs):
    """Test the put_bucket method with a pvc directory specified.

    NOTE: This test also validates specification of a valid image name.

    Requirements:
        * Working K8s cluster with PVC support
        * Working S3 object storage service

    Dependencies
        * A PVC volume with files
        * An empty S3 bucket
        * A valid S3 Config Secret on the K8s cluster

    Test Steps:
        * Run the S3DataMover put_bucket method with a pvc_dir specifid
        * Verify the job name is returned from the put_object method
        * Verify the job completes in a reasonable time
        * Verify the job succeeds
        * Verify the files exist in the bucket

    :param pvc_with_data:
    :param s3_bucket_empty:
    :param k8s_s3_secret:
    :param k8s_namespace:
    :param mover_image:
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
        image_name=mover_image,
        credentials_secret=k8s_s3_secret
    )

    base_dir = 'layer2'
    job = data_mover.put_bucket(bucket=s3_bucket_empty, pvc=pvc_with_data, pvc_dir=base_dir)
    assert job

    initial_status = data_mover.get_job_status(job=job)
    # This verifies the job name is correct and we can get the status
    assert initial_status

    job_completed = False
    for step in range(30):
        if not data_mover.is_job_active(job=job):
            job_completed = True
            assert data_mover.did_job_succeed(job=job)
            break
        else:
            time.sleep(2)
    # Verify the job completed and we didn't timeout of the loop
    assert job_completed

    # Verify the files exist in the bucket
    bucket = s3_resource.Bucket(name=s3_bucket_empty)
    bucket_objects = bucket.objects.all()

    # pvc_filenames = ["one.txt", "two.txt", "three.txt"]
    pvc_filenames = ["three.txt"]
    expected_keys = ["three.txt", "layer3/four.txt"]
    for s3_object in bucket_objects:
        print("S3 object: {}".format(s3_object))
        # Note: put_bucket currently retains directory structures so keys may have dir names included
        if s3_object.key in expected_keys:
            expected_keys.remove(s3_object.key)
        # key_base = os.path.basename(s3_object.key)
        # print(f"Key basename: {key_base}")
        # if key_base in pvc_filenames:
        #     pvc_filenames.remove(key_base)
    # Verify we found all the files
    assert not expected_keys
