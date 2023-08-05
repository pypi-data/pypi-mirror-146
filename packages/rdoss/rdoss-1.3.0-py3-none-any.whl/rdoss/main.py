from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
class Rdfs(CosS3Client):
    def __init__(self,secret_id,secret_key,region = 'ap-shanghai'):
        self.secret_id =secret_id
        self.secret_key = secret_key
        self.region =region
        token = None
        scheme = 'https'
        self.config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key, Token=token, Scheme=scheme)
        CosS3Client.__init__(self=self,conf=self.config)
class RdBucket(Rdfs):
    def list(self):
        res = Rdfs.list_buckets(self)
        return(res)
    def create(self,Bucket='zhengjia-1251945645'):
        self.Bucket = Bucket
        res = Rdfs.create_bucket(self,Bucket=self.Bucket)
        return(res)

class RdFile(Rdfs):
    def upload(self,key,file_name,Bucket='zhengjia-1251945645'):
        self.Bucket =Bucket
        self.key = key
        with open(file_name, 'rb') as fp:
            response = Rdfs.put_object(self,
                Bucket=self.Bucket,
                Body=fp,
                Key=self.key,
                StorageClass='STANDARD',
                EnableMD5=False
            )
        return(response['ETag'])
    def download(self):
        pass



if __name__ =='__main__':
    pass






