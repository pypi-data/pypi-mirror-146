from pydantic import BaseModel

class Meta(BaseModel):
    current_version: str = '1.0.0'
    last_version_url: str = ''