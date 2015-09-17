import json
import urllib.request


def call_restful_service(service_url):
    """Generic method to call a web service over HTTP and return the response as JSON

    Keyword arguments:
    service_url -- a string containing the URL to call. Note that we expect all variables
                   to have been filled in already and expect a URL to call (no replacements)
    """
    _response = urllib.request.urlopen(service_url)
    _parsed_json = json.loads(_response.read().decode('utf-8'))
    _response.close()
    return _parsed_json