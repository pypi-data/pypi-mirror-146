import requests
from .exceptions import *
from .utils import Singleton

__all__ = ['auth']


class Auth(metaclass=Singleton):
    def __init__(self):
        """
        Initializes the Auth class.
        """
        self.password = None
        self.username = None
        self._token = None
        self.base_api_url = "http://deepgis:8010"

    def login(self, username, password):
        self.username = username
        self.password = password
        self._get_token()

    def check_login(self):
        """
        Checks if the user is logged in.
        :return: None
        """
        user_info_api = f"{self.base_api_url}/users/me"
        response = requests.get(user_info_api, headers=self._get_token_header())
        if response.status_code == 200:
            return response.json()
        else:
            raise UnAuthorizedException("Failed to check login. Check if you have login.")

    def _get_token(self):
        """
        Gets the token from the server.
        :return:
        """
        if self._token:
            return
        login_api = f"{self.base_api_url}/auth/jwt/login"
        payload = {"username": self.username, "password": self.password}
        response = requests.post(login_api, data=payload)
        if response.status_code == 200:
            token = response.json()["access_token"]
            self._token = token
        else:
            raise UnAuthorizedException("Failed to login. Check if you have entered the correct credentials.")

    def _get_token_header(self):
        if self._token is None:
            self._get_token()
        return {"Authorization": "Bearer " + self._token}


auth = Auth()
