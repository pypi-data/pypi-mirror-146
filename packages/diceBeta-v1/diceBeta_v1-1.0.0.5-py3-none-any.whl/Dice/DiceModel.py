# -*- coding: utf-8 -*- 
#pip install google-cloud-storage
import os
from google.cloud import storage
import requests
import time
import random

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

def run_inferapi(path='', K=5, token_url=""):
    config = {'url': path, "k": str(K)}
    result = requests.post(token_url, data = config)

    return result.text

def run_trainapi(path='', aug="True", token_url=""):
    if aug != None:
        config = {'url': path, "augmentation": aug}
    else:
        config = {'url': path}
    print(config)
    result = requests.post(token_url, data = config)

    return result.text

def run_initapi(model="", class_dict="", token_url=""):
    config = {'model': model, "class_dict": class_dict}
    result = requests.post(token_url, data = config)

    return None


class dice:
    def __init__(self, key_path):
        return None
    
    def download_metric(self, destination_file_name="metric_result.jpg"):
        bucket_name = "nnc-gifticon"
        source_blob_name = "test_folder/metric_result.jpg"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.key
        download_blob(self.key, bucket_name, source_blob_name, destination_file_name)

class ImageModel(dice):
    def __init__(self, key_path, model, class_dict=None):
        self.key = key_path
        self.name = str(int(random.random() * 10000000))
        token_url_infer = "http://3.39.109.198:8000/list/initial/"
        token_url_train = "http://3.37.231.42:8000/list/initial/"
        class_name = "image_folder/" + self.name + ".pickle"
        bucket_name = "nnc-gifticon"
        class_url = upload_to_bucket(self.key, class_name, class_dict, bucket_name)
        run_initapi(model=model, class_dict=class_url, token_url=token_url_infer)
        run_initapi(model=model, class_dict=class_url, token_url=token_url_train)

    def train(self, data, aug="True"):
        token_url = "http://3.37.231.42:8000/list/train/"
        blob_name = "image_folder/" + self.name + "." + data.split(".")[-1]
        bucket_name = "nnc-gifticon"
        url = upload_to_bucket(self.key, blob_name, data, bucket_name)
        accuracy = eval(run_trainapi(path=url, aug=aug, token_url=token_url))
        return accuracy

    def infer(self, data, K=1):
        token_url = "http://3.39.109.198:8000/list/inference/"
        blob_name = "image_folder/data." + data.split(".")[-1]
        bucket_name = "nnc-gifticon"
        url = upload_to_bucket(self.key, blob_name, data, bucket_name)
        result = eval(run_inferapi(path=url, K=K, token_url=token_url))
        return result[0], result[1]

class TextModel(dice):
    def __init__(self, key_path, model, class_dict=None):
        self.key = key_path
        self.name = str(int(random.random() * 10000000))
        token_url_infer = "http://3.39.136.1:8000/list/initial/"
        token_url_train = "http://3.34.68.203:8000/list/initial/"
        class_name = "text_folder/" + self.name + ".pickle"
        bucket_name = "nnc-gifticon"
        class_url = upload_to_bucket(self.key, class_name, class_dict, bucket_name)
        run_initapi(model=model, class_dict=class_url, token_url=token_url_infer)
        run_initapi(model=model, class_dict=class_url, token_url=token_url_train)

    def train(self, data):
        token_url = "http://3.34.68.203:8000/list/train/"
        blob_name = "text_folder/data." + data.split(".")[-1]
        bucket_name = "nnc-gifticon"
        url = upload_to_bucket(self.key, blob_name, data, bucket_name)
        accuracy = eval(run_trainapi(path=url, aug=None, token_url=token_url))
        return accuracy

    def infer(self, data, K=1):
        token_url = "http://3.39.136.1:8000/list/inference/"
        category, prob = eval(run_inferapi(path=data, K=K, token_url=token_url))
        return category, prob
    

if __name__ == '__main__':
    #data = "/Users/kim-yeong-geun/Downloads/data.zip"
    data = "/Users/kim-yeong-geun/Downloads/13776.jpg"
    #destination_file_name = "metric_result.jpg"
    key_path = "/Users/kim-yeong-geun/Documents/grpc/Dice/elite-striker-343511-2249c8c11f81.json"
    class_dict = "dictionary.pickle"
    K = 1
    data = "스타벅스/카페 아메리카노 T2잔+슈크림/가드 바우쿠헤+The 초초 초콕···/7627 0753 8265/교환처 스타벅스/유효기간 2022년05월28일/주문번호 1578509166/kakaotalk 선물하기/"
    #model = ImageModel(key_path, "regnety_040", class_dict)
    #acc = model.train(data="/Users/kim-yeong-geun/Downloads/data.zip")
    model = TextModel(key_path, "monologg/koelectra-base-v3-discriminator", class_dict)
    acc = model.train(data="/Users/kim-yeong-geun/Downloads/double_data2.csv")
    #category, prob = model.infer(data, K)
    print(acc)
    #model.download_metric(destination_file_name)