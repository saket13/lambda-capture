import boto3
import os


class AWS_Utils():

    def __init__(self, service_name: str):
        self.service_client = boto3.client(
            service_name,
            region_name=os.getenv('AWS_S3_REGION_NAME'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

    def get_service_client_instance(self):
        return self.service_client