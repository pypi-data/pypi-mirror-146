from copyreg import pickle
import zipfile
import subprocess
from io import BytesIO
from packaging import version
import os
import pickle

from tqdm import tqdm
import requests

from ..core.meta import Meta

class MetaNotFound(Exception):
    pass

class LocalMetaNotFound(Exception):
    pass

class UpdaterError(Exception):
    pass

class Updater:
    client_url: str
    app_name: str
    
    def __init__(self, app_name: str, bucket_id: str = 'pdcartifact') -> None:
        self.app_name = app_name
        self.client_url = f'https://storage.googleapis.com/{bucket_id}/'
    
    def get_local_meta(self) -> Meta:
        fname = '.meta'
        
        if not os.path.exists(fname):
            raise LocalMetaNotFound(f'localmeta not found')
        else:
            with open(fname, 'rb') as f:
                meta = pickle.load(f)
            
        return meta
                
    def get_remote_meta(self) -> Meta:
        url = f'{self.client_url}{self.app_name}/meta.json'
        res = requests.get(url)
        
        if res.status_code == 404:
            raise MetaNotFound(f'meta apliaksi {self.app_name}')
        
        if res.status_code != 200:
            raise UpdaterError(f'error {res.status_code} --> {res.text}')
        
        return Meta.parse_obj(res.json())
    
    def check_update(self) -> bool:
        print('checking update...')
        
        remote_meta = self.get_remote_meta()
        
        try:
            local_meta = self.get_local_meta()
        except LocalMetaNotFound:
            fname = '.meta'
            local_meta = self.get_remote_meta()
            with open(fname, 'wb') as f:
                pickle.dump(local_meta, f)
            os.system(f'attrib +h {fname}')
            
            print(f'new version available.. {local_meta.current_version}')
            print('update now..')
            self.run_update(remote_meta)
            
            return
        
        
        latest_version = remote_meta.current_version
        current_version = local_meta.current_version
        
        if version.parse(latest_version) > version.parse(current_version):
            print(f'new version available.. {latest_version}')
            print('update now..')
            
            self.run_update(remote_meta)
            
        with open(fname, 'wb') as f:
                pickle.dump(remote_meta, f)
    
    def run_update(self, meta, distfold = './'):
        res = requests.get(meta.last_version_url, stream=True)
        
        total = int(res.headers.get('content-length', 0))
        fname = meta.last_version_url.split('/')[-1]
        
        with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in res.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
        
        with open(fname, 'rb') as f:
            zip_ref = zipfile.ZipFile(f)
            zip_ref.extractall(distfold)
        
        os.remove(fname)
        
    def extract_zip(self, zip_file, dest_dir):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
            
    
    def detach_process(self, cmd):
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
            

if __name__ == '__main__':
    updater = Updater('automap')
    updater.check_update()
    updater.detach_process(['ping', '8.8.8.8', '-t'])
