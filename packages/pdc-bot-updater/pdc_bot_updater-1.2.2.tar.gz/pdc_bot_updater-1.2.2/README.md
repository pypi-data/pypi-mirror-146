# pdc_updater
implementasi auto updater dengan memakai cloud storage google

### set environtment
set GOOGLE_APPLICATION_CREDENTIALS=credentials.json


# Example
### Publising Aplication
```
from pdc_bot_updater.publisher.publish import configure_client, AppArchiver

bucket_id = 'artifact'
folder_app = 'aplikasi_bot'

configure_client(bucket_id)


archiver = AppArchiver(folder_app)
archiver.get_meta()
archiver.upload_archive(f'dist/aplication.zip', version='1.0.0')
```

### Updating App
```
from pdc_bot_updater.client.updater import Updater

bucket_id = 'artifact'
folder_app = 'aplikasi_bot'

updater = Updater(folder_app, bucket_id)
updater.check_update()
updater.detach_process(['application.exe'])

```


