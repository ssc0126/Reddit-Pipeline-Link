import os
import boto3
import configparser
import pathlib
import botocore
from botocore.exceptions import ClientError
import sys


config_file = "my_config.ini"
config_file_path = pathlib.Path(__file__).parent.absolute()
print(config_file_path)
config = configparser.ConfigParser()
config.read(f"{config_file_path}/{config_file}")


ACCESS_KEY = config.get('AWS', 'aws_access_key_id')
SECRET_KEY = config.get('AWS', 'aws_secret_access_key')
BUCKET_NAME = config.get('AWS', 'bucket_name')


try:
  FILENAME = sys.argv[1]
except Exception as e:
  print(f"Please input csv file name as cmd line arguemnt. Error {e}")
  sys.exit(1)


#FILENAME = f"{cmd_arg}"


def s3_service_conn():
    try:
        client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key= SECRET_KEY)
        return client
    except:
        print('s3 connection error')


def make_bucket(connection):
    #https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html
    bucket_exists = True
    try:
        #checks if bucket already exists 
        connection.head_bucket(Bucket = BUCKET_NAME)
        
    except ClientError as err:
        error = err.response['Error']['Code']
        if error != '200':
            print(f'{err} \n')
            bucket_exists = False
            
    if bucket_exists == False:
        try:
            connection.create_bucket(Bucket = BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
            print('Success')

        except ClientError as err:
            err2 = err.response['Error']['Code']
            print(f'{err2} \n')
            print('Could not create bucket')
            print('\n')

def upload_file_to_s3(connection):
    path = pathlib.Path(__file__).parent.absolute()
    #print(path)
    try:
        connection.upload_file(Filename = f"{path}/FileDump/{FILENAME}", Bucket = BUCKET_NAME, Key = FILENAME)
    except  ClientError as err:
        print(f"upload failute. {err}")


def main():
    connection  =  s3_service_conn()
    bucket = make_bucket(connection)
    upload_file_to_s3(connection)


if __name__ == '__main__':
  main()
