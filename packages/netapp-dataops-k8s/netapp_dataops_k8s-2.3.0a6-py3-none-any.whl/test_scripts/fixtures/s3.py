"""Fixtures for managing S3."""
import boto3
import botocore.exceptions
import mypy_boto3_s3
import pytest


@pytest.fixture(scope="session")
def s3_resource(config_data) -> mypy_boto3_s3.S3ServiceResource:
    """Fixture to provide the Boto3 S3 resource for interacting with S3.

    :param config_data: The config_data fixture.
    :return: The S3 service resource
    """
    # All config definitions are required
    s3_host = config_data['s3_host']
    s3_port = config_data['s3_port']
    s3_protocol = config_data['s3_protocol']
    s3_access_key = config_data['s3_access_key']
    s3_secret_key = config_data['s3_secret_key']
    s3_verify_certs = config_data['s3_verify_certs']
    endpoint = f"{s3_protocol}://{s3_host}:{s3_port}"

    session = boto3.Session(aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key)
    resource = session.resource(service_name='s3', endpoint_url=endpoint, verify=s3_verify_certs)
    yield resource


@pytest.fixture(scope="function")
def s3_bucket_empty(s3_resource):
    """Fixture to provide an empty bucket for a test.

    This fixture will create a new bucket during setup and remove it during teardown.

    :param s3_resource: The fixture providing the s3 resource object.
    :return: The name of the empty bucket.
    """
    # TODO: Should the name be configurable?
    bucket_name = "dataops-test-empty"
    try:
        s3_resource.create_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as ce:
        # Determining the exception type here is annoying
        # In testing I saw BucketAlreadyOwnedByYou, but other types might occur
        if ce.response['Error']['Code'] == "BucketAlreadyOwnedByYou":
            bucket = s3_resource.Bucket(name=bucket_name)
            existing_objects = bucket.objects.all()
            try:
                next(iter(existing_objects))
            except StopIteration:
                print("There are no objects. This bucket will work!")
            else:
                raise Exception(f"Bucket {bucket_name} exists and is not empty.")
        else:
            raise ce

    yield bucket_name

    test_bucket = s3_resource.Bucket(name=bucket_name)
    # Before deleting the bucket we must delete all objects
    # We can delete all objects safely because we know we started with an empty bucket
    test_bucket.objects.all().delete()
    # Now we can delete the bucket!
    test_bucket.delete()


@pytest.fixture(scope="function")
def s3_bucket_full(s3_resource, tmp_path):
    """Fixture to provide a bucket with data for a test.

    This fixture will create a bucket and populate it with some objects.

    :param s3_resource: Fixture that provides the S3 resource for the configuration.
    :param tmp_path: Fixture providing a tmp directory for the test.
    :return: The name of the bucket.
    """
    bucket_name = "dataops-test-full"
    try:
        bucket = s3_resource.create_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError:
        raise Exception(f"Bucket {bucket_name} already exists.")

    # Create temporary files to upload
    file1 = tmp_path / "alpha.txt"
    file1.write_text('Alpha is first.')
    file2 = tmp_path / "bravo.txt"
    file2.write_text('Bravo is second.')
    dir1 = tmp_path / 'planets'
    dir1.mkdir()
    file3 = dir1 / 'mercury.txt'
    file3.write_text('Mercury is closest to sol.')

    bucket.upload_file(str(file1), file1.name)
    bucket.upload_file(str(file2), file2.name)
    bucket.upload_file(str(file3), "planets/{}".format(file3.name))

    yield bucket_name

    # Reminder, this doesn't fail if there are no objects to delete
    bucket.objects.all().delete()
    bucket.delete()
