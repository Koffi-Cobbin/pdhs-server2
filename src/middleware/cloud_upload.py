from os import environ
from cloudinary.uploader import upload
import cloudinary
from cloudinary.utils import cloudinary_url


cloudinary.config(
    cloud_name = "thehivecloudstorage",
    api_key = "159559222499375",
    api_secret = "Y63wxrblUk5qU5ls77ln6O_Gxec"
)

def upload_file(file_to_upload):
  if file_to_upload:
    try:
      upload_result = upload(file_to_upload)
    except:
      return {"msg":"Error uploading file"}
    
    return upload_result.get("url")
    
  

