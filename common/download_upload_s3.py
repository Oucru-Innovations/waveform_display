from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory, send_file
import boto3
from common.utilities import *


class DownUpS3:
    def __init__(self,server,BUCKET,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY):
        self.server = server
        self.BUCKET = BUCKET
        self.AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY

    # @server.route("/downloads/<path:file_path>",methods=['GET']) # define route when call function
    def download(self,file_path):
        """Serve a file from the upload directory."""
        output = self.download_file(file_path,self.BUCKET)
        url = 'https://%s.s3.amazonaws.com/%s' % (self.BUCKET, file_path)
        print('================================')
        print(url)
        return send_from_directory(".", file_path,cache_timeout=0, as_attachment=True)

    def make_s3_connection(self):
        s3 = boto3.client('s3',
                          aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY)
        return s3

    def download_file(self,file_name):
        """
        Function to download a given file from an S3 bucket
        """
        s3 = boto3.resource('s3',
                          aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY)
        output = f"/downloads/{file_name}"
        # s3.Bucket(bucket).download_file(file_name, output)
        s3.meta.client.download_file(self.BUCKET,file_name,file_name)
        print("download successful")
        return output

    def list_files(self):
        """
        Function to list files in a given S3 bucket
        """
        s3 = boto3.client('s3')
        contents = []
        for item in s3.list_objects(Bucket=self.BUCKET)['Contents']:
            contents.append(item)

        return contents

    def file_download_link(self,filename):
        """Create a Plotly Dash 'A' element that downloads a file from the app."""
        location = "/downloads/{}".format(urlquote(filename))
        return html.A(filename, href=location)

    # @server.route('/')
    def upload_to_s3(self,file_name,file_content):

      s3 = self.make_s3_connection()
      s3.upload_fileobj(io.BytesIO(bytearray(file_content,'utf-8')), self.BUCKET, file_name)

    def upload_file(self,file_name, bucket):
        """
        Function to upload a file to an S3 bucket
        """
        object_name = file_name
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(file_name, bucket, object_name)

        return response