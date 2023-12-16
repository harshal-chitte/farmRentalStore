import requests
import logging
from farmer.constant import UrlConst
import json


def login_api(payload=None):
    try:
        reponse =requests.post(
            url=f"{UrlConst.API_URL.value}/users/login/",
            data=payload
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def register_api(payload=None):
    try:
        reponse =requests.post(
            url=f"{UrlConst.API_URL.value}/users/register/",
            data=payload
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e
    

def get_api_call(url, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=url,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e

def post_api_call(url,payload, token=None, files=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",

        }
        reponse =requests.post(
            url=url,
            headers=headers,
            data=payload,
            files = files
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def put_api_call(url,payload, token=None, files=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.put(
            url=url,
            headers=headers,
            data=payload,
            files = files
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def delete_api_call(url, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.delete(
            url=url,
            headers=headers,
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e