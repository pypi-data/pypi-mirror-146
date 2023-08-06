import logging
import os

import requests

logger = logging.getLogger(__name__)

API_BASE_URL = "https://api.influenceth.io"

INFLUENCE_CLIENT_ID = os.environ.get("INFLUENCE_CLIENT_ID")
INFLUENCE_CLIENT_SECRET = os.environ.get("INFLUENCE_CLIENT_SECRET")


class InfluenceClient:
    def __init__(
        self,
        base_url: str = API_BASE_URL,
        client_id: str = INFLUENCE_CLIENT_ID,
        client_secret: str = INFLUENCE_CLIENT_SECRET,
        session: requests.Session = requests.Session(),
        refresh_token: bool = True,
    ) -> None:
        """[summary]

        Args:
            base_url (str, optional): the base url for the API. Defaults to https://api.influenceth.io.
            client_id (str, optional): the client id used to fetch the initial session token. Defaults to INFLUENCE_CLIENT_ID.
            client_secret (str, optional): [description]. Defaults to INFLUENCE_CLIENT_SECRET.
            session (requests.Session, optional): [description]. Defaults to requests.Session().
            fetch_token (bool, optional): [description]. Defaults to True.
        """
        self._base_url = base_url
        self._session = session
        self.client_id = client_id
        self.client_secret = client_secret
        if refresh_token:
            self.refresh_token()

    def refresh_token(self) -> None:
        """Refreshes the API token from the Influence Server. Called automatically during initialization by default."""
        token_req = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        token_resp = self._session.post(
            self._base_url + "/v1/auth/token", json=token_req
        )
        token_resp.raise_for_status()
        self._access_token = token_resp.json()["access_token"]
        self._session.headers["Authorization"] = "Bearer " + self._access_token

    def _get_by_url(self, url: str):
        """Sends a GET request to the Influence API.

        For Internal Use Only

        Args:
            url (str): the url of the request

        Raises:
            Exception: if there is no authorization configured for the client
            HTTPError: for invalid responses

        Returns:
            dict: the json response from the API
        """
        if "Authorization" not in self._session.headers:
            raise Exception("Request will fail: authorization is required.")
        if url.startswith("/"):
            url = API_BASE_URL + url
        result = self._session.get(url)
        result.raise_for_status()
        result_json = result.json()
        return result_json

    def get_asteroid(self, serial: int) -> dict:
        """Retrieves an asteroid, identified by a serial number, from the Influence API

        Args:
            serial (int): the serial number of the asteroid

        Returns:
            dict: the JSON response from the API
        """
        return self._get_by_url(f"/v1/asteroids/{serial}")

    def get_crewmate(self, serial: int) -> dict:
        """Retrieves a crewmate, identified by a serial number, from the Influence API

        Args:
            serial (int): the serial number of the asteroid

        Returns:
            dict: the JSON response from the API
        """
        return self._get_by_url(f"/v1/crew/{serial}")
