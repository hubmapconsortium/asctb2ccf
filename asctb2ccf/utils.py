"""Basic utilities module"""
import requests


def request_get(url):
    """
    Performs a get request that provides a (somewhat) useful error message.
    """
    try:
        response = requests.get(url)
    except ImportError:
        raise ImportError("Couldn't retrieve the data, check your URL")
    else:
        return response


def json_handler(url):
    """Returns request in JSON (dict) format"""
    return request_get(url).json()
