from src.download import Download
import boto3
import json
import os

class S3Loader(Download):

    def __init__(self, bucket):
        self.bucket = bucket

    # def download(self, matchData):
    #     self.upload_file(self, matchData)

    def download(self, matchData):
        """Upload a file to an S3 bucket

        :param matchData: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        object_name = str(matchData['matchId']) + ".json"
        
        #write file
        with open(object_name, "w") as f:
            f.write( json.dumps( matchData, indent=4 ) )


        # Upload the file
        s3_client = boto3.client('s3')
        with open(object_name, "rb") as f:
            s3_client.upload_fileobj(f, self.bucket, object_name)
        
            # print("Error")
            # #Delete file
            # os.remove(object_name)


            #return False

        # Delete file
        os.remove(object_name)
        return True