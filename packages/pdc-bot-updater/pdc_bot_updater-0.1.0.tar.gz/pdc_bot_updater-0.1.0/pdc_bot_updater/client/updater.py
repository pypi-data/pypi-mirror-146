import zipfile
import subprocess
from io import BytesIO

import requests

from ..core.meta import Meta

class MetaNotFound(Exception):
    pass

class UpdaterError(Exception):
    pass

        
class Updater:
    client_url: str = 'https://storage.googleapis.com/pdcartifact/'
    app_name: str
    
    def __init__(self, app_name: str) -> None:
        self.app_name = app_name
    
    def get_meta(self) -> Meta:
        url = f'{self.client_url}{self.app_name}/meta.json'
        res = requests.get(url)
        
        if res.status_code == 404:
            raise MetaNotFound(f'meta apliaksi {self.app_name}')
        
        if res.status_code != 200:
            raise UpdaterError(f'error {res.status_code} --> {res.text}')
        
        return Meta.parse_obj(res.json())
    
    def run_update(self, distfold = './'):
        meta = self.get_meta()
        res = requests.get(meta.last_version_url, stream=True)
        file = BytesIO(res.content)
        zip_ref = zipfile.ZipFile(file)
        zip_ref.extractall(distfold)
        
        
    def extract_zip(self, zip_file, dest_dir):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
            
    
    def detach_process(self, cmd):
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
            

if __name__ == '__main__':
    updater = Updater('automap')
    updater.run_update()
    updater.detach_process(['ping', '8.8.8.8', '-t'])
