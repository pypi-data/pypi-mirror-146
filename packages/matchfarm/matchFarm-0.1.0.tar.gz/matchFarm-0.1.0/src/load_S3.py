from src.download import Download
import boto3

class S3Loader(Download):

    def __init__(self, bucket):
        self.bucket = bucket

    def upload_file(self, matchData):
        """Upload a file to an S3 bucket

        :param matchData: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        object_name = str(matchData['matchId']) + ".json"
        

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(matchData, self.bucket, object_name)
        except e as e:
            print(e)
            return False
        return True