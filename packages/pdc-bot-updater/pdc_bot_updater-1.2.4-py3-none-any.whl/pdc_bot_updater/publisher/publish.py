import json
import os
from tqdm import tqdm

from pydantic import BaseModel
from google.cloud import storage
from google.api_core.exceptions import NotFound

from ..core.meta import Meta

class Archive(BaseModel):
    app_name: str
    version: str
    

class AppArchiver:
    app_name: str 
    
    meta: Meta
    bucket: storage.Bucket
    
    def __init__(self, app_name: str) -> None:
        self.app_name = app_name
    
    def get_meta(self):
        blob = self.bucket.blob(f'{self.app_name}/meta.json')
        try:
            text = blob.download_as_text()
            meta = Meta.parse_obj(json.loads(text))
        except NotFound as e:
            meta = Meta.parse_obj({})
            self.meta = meta
            self.upload_meta()
            
        self.meta = meta
        
        return meta
    
    def upload_meta(self):
        blob = self.bucket.blob(f'{self.app_name}/meta.json')
        
        metastr = json.dumps(self.meta.dict())
        print(f'updating meta {metastr}')
        
        blob.upload_from_string(metastr)
        blob.make_public()
        
    
    def upload_archive(self, filename: str, version: str):
        CHUNK_SIZE = 262144
        
        blob = self.bucket.blob(f'{self.app_name}/app_v{version}.zip', chunk_size=CHUNK_SIZE)
        with open(filename, 'rb') as f:
            total_bytes = os.fstat(f.fileno()).st_size
            with tqdm.wrapattr(f, "read", total=total_bytes, miniters=1, desc=f"upload to {filename}") as file_obj:
                blob.upload_from_file(file_obj)
        
        blob.make_public()
        self.meta.current_version = version
        self.meta.last_version_url = blob.public_url
        self.upload_meta()
        
        return blob.public_url
        
    
    def get_list_archive(self):
        raise NotImplementedError('get_list_archive not implemented')
        
        
        
def configure_client(bucket_id: str):
    client = storage.Client()
    
    AppArchiver.bucket = client.get_bucket(bucket_id)


if __name__ == '__main__':
    configure_client('pdcartifact')
    
    app = AppArchiver('automap')
    app.get_meta()
    app.upload_archive('test/assets/test_loc.zip', '2.5.0')
    
    