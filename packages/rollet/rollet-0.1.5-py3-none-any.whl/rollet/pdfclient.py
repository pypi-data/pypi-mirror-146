
__all__ = [
    "GrobidClient",
    "grobid_service"
]

from typing import List, Dict, Union
from requests.compat import urljoin
from copy import deepcopy
import json, requests, os

class ApiClient(object):
    accept_type = 'application/xml'
    api_base = None

    def __init__(
            self,
            base_url: str,
            username: str = None,
            api_key: str = None,
            status_endpoint: str = None,
            timeout: int = 60
    ):
        """
        Initialise client.
        base_url: The base URL to the service being used.
        username: The username to authenticate with.
        api_key: The API key to authenticate with.
        timeout: Maximum time before timing out.
        """
        self.base_url = base_url
        self.username = username
        self.api_key = api_key
        self.status_endpoint = urljoin(self.base_url, status_endpoint)
        self.timeout = timeout

    @staticmethod
    def encode(request, data):
        """ Add request content data to request body, set Content-type header.
        Should be overridden by subclasses if not using JSON encoding.
        Args:
            request (HTTPRequest): The request object.
            data (dict, None): Data to be encoded.
        Returns:
            HTTPRequest: The request object.
        """
        if data is None:
            return request

        request.add_header('Content-Type', 'application/json')
        request.data = json.dumps(data)

        return request

    @staticmethod
    def decode(response):
        """ Decode the returned data in the response.
        Should be overridden by subclasses if something else than JSON is
        expected.
        Args:
            response (HTTPResponse): The response object.
        Returns:
            dict or None.
        """
        try:
            return response.json()
        except ValueError as e:
            return e.message

    def get_credentials(self) -> Dict:
        """ Returns parameters to be added to authenticate the request.
        This lives on its own to make it easier to re-implement it if needed.
        Returns:
            dict: A dictionary containing the credentials.
        """
        return {"username": self.username, "api_key": self.api_key}

    def call_api(
            self,
            method: str,
            url: str,
            headers: Dict[str, str] = None,
            params: Dict[str, str] = None,
            data: Dict[str, str] = None,
            files: Dict[str, str] = None,
            timeout: int = None,
    ):
        """
        This returns object containing data, with error details if applicable.
        method: The HTTP method to use.
        url: Resource location relative to the base URL.
        headers: Extra request headers to set.
        params: Query-string parameters.
        data: Request body for POST or PUT requests.
        files: Files to be passed to the request.
        timeout: Maximum time before timing out.

        :return: ResultParser or ErrorParser.
        """
        headers = deepcopy(headers) or {}
        headers['Accept'] = self.accept_type
        params = deepcopy(params) or {}
        data = data or {}
        files = files or {}
        r = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            files=files,
            data=data,
            timeout=timeout,
        )

        return r, r.status_code

    def get(self,
        url: str,
        params: Dict[str, str] = None,
        **kwargs
    ):
        """ 
        Call the API with a  GET request.
        url: Resource location relative to the base URL.
        params: Query-string parameters.
        :return: ResultParser or ErrorParser.
        """
        return self.call_api(
            "GET",
            url,
            params=params,
            **kwargs
        )

    def delete(self, url, params=None, **kwargs):
        """ Call the API with a DELETE request.
        Args:
            url (str): Resource location relative to the base URL.
            params (dict or None): Query-string parameters.
        Returns:
            ResultParser or ErrorParser.
        """
        return self.call_api(
            "DELETE",
            url,
            params=params,
            **kwargs
        )

    def put(self, url, params=None, data=None, files=None, **kwargs):
        """ Call the API with a PUT request.
        Args:
            url (str): Resource location relative to the base URL.
            params (dict or None): Query-string parameters.
            data (dict or None): Request body contents.
            files (dict or None: Files to be passed to the request.
        Returns:
            An instance of ResultParser or ErrorParser.
        """
        return self.call_api(
            "PUT",
            url,
            params=params,
            data=data,
            files=files,
            **kwargs
        )

    def post(self, url, params=None, data=None, files=None, **kwargs):
        """ Call the API with a POST request.
        Args:
            url (str): Resource location relative to the base URL.
            params (dict or None): Query-string parameters.
            data (dict or None): Request body contents.
            files (dict or None: Files to be passed to the request.
        Returns:
            An instance of ResultParser or ErrorParser.
        """
        return self.call_api(
            method="POST",
            url=url,
            params=params,
            data=data,
            files=files,
            **kwargs
        )

    def service_status(self, **kwargs):
        """ Call the API to get the status of the service.
        Returns:
            An instance of ResultParser or ErrorParser.
        """
        return self.call_api(
            'GET',
            self.status_endpoint,
            params={'format': 'json'},
            **kwargs
        )


class GrobidClient(ApiClient):

    def __init__(self,
        host: str = None,
        port: int = None
    ):
        if not host: host = str(os.getenv('GROBID_HOST', 'localhost'))
        if not port: port = int(os.getenv('GROBID_PORT', 8070))

        if not host.startswith("http"):
            host = "http://" + host
        self.host = host
        self.port = port
        self.url = f"{self.host}:{self.port}"

    def test_alive(self):
        url = f"{self.url}/api/isalive"
        rsp = requests.get(url, verify = False)
        return rsp.status_code == 200

    def serve(
        self,
        service: str,
        pdf_file,
        generateIDs: int = 1,
        consolidate_header: int = 0,
        consolidate_citations: int = 0,
        teiCoordinates: List = ["persName", "figure", "ref", "biblStruct", "formula"]
    ):

        if isinstance(pdf_file, str):
            with open(pdf_file, 'rb') as fp:
                pdf_file = fp
        files = {'input': pdf_file}
        url = f"{self.url}/api/{service}"

        the_data = {
            "generateIDs": generateIDs,
            "consolidateHeader": consolidate_header,
            "consolidateCitations": consolidate_citations,
            "teiCoordinates": teiCoordinates
        }

        rsp, _ = self.post(
            url = url,
            files = files,
            data = the_data,
            headers = {'Accept': 'text/plain'}
        )

        return rsp
    

def grobid_service(
    host: str = 'localhost',
    port: Union[str, int] = '8070'
):
    os.environ.update(**{'GROBID_HOST': str(host), 'GROBID_PORT': str(port)})
