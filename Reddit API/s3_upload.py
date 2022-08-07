import os
import boto3
import configparser
import pathlib
import botocore
from botocore.exceptions import ClientError
config_file = "my_config.ini"
config_file_path = os.getcwd()#pathlib.Path(__file__).parent.absolute()
#print(config_file_path)
config = configparser.ConfigParser()
config.read(f"{config_file_path}\{config_file}")
ACCESS_KEY = config.get('AWS', 'aws_access_key_id')
SECRET_KEY = config.get('AWS', 'aws_secret_access_key')
BUCKET_NAME = config.get('AWS', 'bucket_name')
def s3_service_conn():
    try:
        client = boto3.('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        return client
    except:
        print('s3 connection error')

def upload_file(connection, file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
connection  =  s3_service_conn()
#https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html
bucket_exists = True
try:
    #checks if bucket already exists 
    connection.head_bucket(Bucket = BUCKET_NAME)
    
except ClientError as err:
     error = err.response['Error']['Code']
     print(error)
     if error != 200:
        bucket_exist = False
        
if bucket_exists == False:
    try:
        connection.create_bucket(Bucket = BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})

    except ClientError as err:
        print('Could not create bucket')

