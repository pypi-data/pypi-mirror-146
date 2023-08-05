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

if __name__ =='__main__':
    pass






