# -*- coding: utf-8 -*- 
#pip install google-cloud-storage
import os
from google.cloud import storage
import requests

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_key.json" 


def upload_to_bucket(key_path, blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket(아까 만들었던 저장소)"""

    storage_client = storage.Client.from_service_account_json(
        key_path)
    #print(buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    
    #접근권한 public 으로 설정
    #blob.make_public()
    
    #파일 url 만들어주기
    url = blob.public_url
    #returns a public url
    return url

def download_blob(key_path, bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client().from_service_account_json(
        key_path)

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )

def run_inferapi(path='', K=5, class_dict="", token_url="http://3.39.109.198:8000/list/inference/"):
    config = {'url': path, "k": str(K), "class_dict": class_dict}
    print(config)
    result = requests.post(token_url, data = config)
    print(result.text)

    return result.text

def run_trainapi(path='', model="", aug="True", token_url=""):
    if aug != None:
        config = {'url': path, 'model': model, "augmentation": aug}
    else:
        config = {'url': path, 'model': model}
    print(config)
    result = requests.post(token_url, data = config)
    print(result.text)

    return result.text


class dice:
    def __init__(self, key_path):
        self.key = key_path

    def download_metric(self, destination_file_name="metric_result.jpg"):
        bucket_name = "nnc-gifticon"
        source_blob_name = "test_folder/metric_result.jpg"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.key
        download_blob(self.key, bucket_name, source_blob_name, destination_file_name)

class ImageModel(dice):
    def train(self, data, model="resnext50_32x4d", aug="True"):
        token_url = "http://3.37.231.42:8000/list/train/"
        blob_name = "image_folder/data." + data.split(".")[-1]
        bucket_name = "nnc-gifticon"
        url = upload_to_bucket(self.key, blob_name, data, bucket_name)
        run_trainapi(path=url, model=model, aug=aug, token_url=token_url)

    def infer(self, data, K=1, class_dict=''):
        token_url = "http://3.39.109.198:8000/list/inference/"
        blob_name = "image_folder/data." + data.split(".")[-1]
        class_name = "image_folder/class_dict.pickle"
        bucket_name = "nnc-gifticon"
        url = upload_to_bucket(self.key, blob_name, data, bucket_name)
        class_dict = upload_to_bucket(self.key, class_name, class_dict, bucket_name)
        run_inferapi(path=url, K=K, class_dict=class_dict, token_url=token_url)

class TextModel(dice):
    def train(self, data, model="monologg/koelectra-base-v3-discriminator"):
        token_url = "http://3.34.68.203:8000/list/train/"
        blob_name = "text_folder/data." + data.split(".")[-1]
        bucket_name = "nnc-gifticon"
        url = upload_to_bucket(self.key, blob_name, data, bucket_name)
        run_trainapi(path=url, model=model, aug=None, token_url=token_url)

    def infer(self, data, class_dict="", K=1):
        token_url = "http://3.38.33.107:8000/list/inference/"
        class_name = "text_folder/class_dict.pickle"
        bucket_name = "nnc-gifticon"
        class_dict = upload_to_bucket(self.key, class_name, class_dict, bucket_name)
        run_inferapi(path=data, K=K, class_dict=class_dict, token_url=token_url)
    

if __name__ == '__main__':
    data = "/Users/kim-yeong-geun/Downloads/13776.jpg"
    destination_file_name = "metric_result.jpg"
    key_path = "/Users/kim-yeong-geun/Documents/grpc/Dice/elite-striker-343511-2249c8c11f81.json"
    model = ImageModel(key_path)
    #model.infer(data)
    model.download_metric(destination_file_name)