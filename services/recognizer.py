import base64
import hmac
import hashlib
import time
import requests
from config import ACRCLOUD_CONFIG

def recognize_song(file_path):
    access_key = ACRCLOUD_CONFIG["access_key"]
    access_secret = ACRCLOUD_CONFIG["access_secret"]
    host = ACRCLOUD_CONFIG["host"]

    http_method = "POST"
    http_uri = "/v1/identify"

    data_type = "audio"
    signature_version = "1"
    timestamp = str(int(time.time()))

    string_to_sign = "\n".join([http_method, http_uri, access_key, data_type, signature_version, timestamp])
    sign = base64.b64encode(hmac.new(access_secret.encode("utf-8"), string_to_sign.encode("utf-8"), hashlib.sha1).digest()).decode("utf-8")

    with open(file_path, "rb") as f:
        sample_data = f.read()

    files = {
        "sample": ("sample", sample_data, "audio/mpeg"),
    }

    data = {
        "access_key": access_key,
        "data_type": data_type,
        "signature": sign,
        "signature_version": signature_version,
        "timestamp": timestamp,
    }

    url = f"https://{host}/v1/identify"
    try:
        response = requests.post(url, files=files, data=data)
        return response.json()
    except Exception as e:
        print(f"Recognition error: {e}")
        return None