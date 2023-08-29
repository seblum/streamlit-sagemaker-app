import os
import time
from functools import wraps
from typing import Any, Callable, Tuple

import boto3
from boto3.session import Session


def timeit(func) -> Callable[..., Any]:
    """
    Decorator function to measure the execution time of a function.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.

    Raises:
        None
    """

    @wraps(func)
    def timeit_wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"\nFunction {func.__name__} took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


class AWSSession:
    """
    A class for managing AWS sessions and performing S3 operations.

    Attributes:
        __region_name (str): The AWS region name.
        __aws_access_key_id (str): The AWS access key ID.
        __aws_secret_access_key (str): The AWS secret access key.
        __aws_role_name (str): The AWS role name.
        __boto3_role_session (Session): The AWS session with the assumed role.
        __s3fs_session (S3FileSystem): The S3 file system session.

    Methods:
        _get_role_access(session: Session) -> Tuple[str, str, str]: Retrieves the role access credentials.
        set_sessions(): Sets up the AWS sessions with the assumed role.
        upload_npy_to_s3(data: np.array, s3_bucket: str, file_key: str) -> None: Uploads a NumPy array to S3.
        download_npy_from_s3(s3_bucket: str, file_key: str) -> np.array: Downloads a NumPy array from S3.
        read_image_from_s3(s3_bucket: str, imname: str) -> np.array: Reads an image from S3.
        list_files_in_bucket(path: str) -> list: Lists files in a bucket.

    """

    def __init__(self):
        self.__region_name = os.getenv("AWS_REGION")
        self.__aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.__aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.__aws_role_name = os.getenv("AWS_ROLE_NAME")

        self.__boto3_role_session = None

    def _get_role_access(self, session: Session) -> Tuple[str, str, str]:
        """
        Retrieves the role access credentials using the provided session.

        Args:
            session (Session): The AWS session object.

        Returns:
            Tuple[str, str, str]: The access key ID, secret access key, and session token.

        Raises:
            None
        """
        sts = session.client("sts", region_name=self.__region_name)
        account_id = sts.get_caller_identity()["Account"]
        # https://www.learnaws.org/2022/09/30/aws-boto3-assume-role/
        response = sts.assume_role(
            RoleArn=f"arn:aws:iam::{account_id}:role/{self.__aws_role_name}",
            RoleSessionName=f"{self.__aws_role_name}-session",
        )
        return (
            response["Credentials"]["AccessKeyId"],
            response["Credentials"]["SecretAccessKey"],
            response["Credentials"]["SessionToken"],
        )

    def set_sessions(self):
        """
        Sets up the AWS sessions with the assumed role.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        user_session = boto3.Session(
            region_name=self.__region_name,
            aws_access_key_id=self.__aws_access_key_id,
            aws_secret_access_key=self.__aws_secret_access_key,
        )
        (
            tmp_aws_access_key_id,
            tmp_aws_secret_access_key,
            tmp_aws_session_token,
        ) = self._get_role_access(user_session)
        self.__boto3_role_session = boto3.Session(
            region_name=self.__region_name,
            aws_access_key_id=tmp_aws_access_key_id,
            aws_secret_access_key=tmp_aws_secret_access_key,
            aws_session_token=tmp_aws_session_token,
        )

    @timeit
    def get_sagemaker_endpoints(self) -> dict:
        """
        Fetch a list of Amazon SageMaker endpoints.

        Returns:
            dict: A dictionary containing information about the SageMaker endpoints.
                Example response:
                {
                    'Endpoints': [
                        {
                            'EndpointName': 'string',
                            'EndpointArn': 'string',
                            'EndpointConfigName': 'string',
                            'ProductionVariants': [
                                {
                                    'VariantName': 'string',
                                    'DeployedImages': [
                                        {
                                            'SpecifiedImage': 'string',
                                            'ResolvedImage': 'string',
                                            'ResolutionTime': datetime(2015, 1, 1)
                                        },
                                    ],
                                    'CurrentWeight': 123.0,
                                    'DesiredWeight': 123.0,
                                    'CurrentInstanceCount': 123,
                                    'DesiredInstanceCount': 123
                                },
                            ],
                            'CreationTime': datetime(2015, 1, 1),
                            'LastModifiedTime': datetime(2015, 1, 1),
                            'EndpointStatus': 'string',
                            'FailureReason': 'string',
                            'MonitoringScheduleArn': 'string',
                            'Tags': [
                                {
                                    'Key': 'string',
                                    'Value': 'string'
                                },
                            ],
                            'EndpointConfigName': 'string'
                        },
                    ],
                    'NextToken': 'string'
                }
        """
        client = self.__boto3_role_session.client("sagemaker")
        response = client.list_endpoints(
            SortBy="CreationTime",
            SortOrder="Descending"
            # SortBy='Name'|'CreationTime'|'Status',
            # SortOrder='Ascending'|'Descending',
            # NextToken='string',
            # MaxResults=123,
            # NameContains='string',
            # CreationTimeBefore=datetime(2015, 1, 1),
            # CreationTimeAfter=datetime(2015, 1, 1),
            # LastModifiedTimeBefore=datetime(2015, 1, 1),
            # LastModifiedTimeAfter=datetime(2015, 1, 1),
            # StatusEquals='OutOfService'|'Creating'|'Updating'|'SystemUpdating'|'RollingBack'|'InService'|'Deleting'|'Failed'
        )
        return response
