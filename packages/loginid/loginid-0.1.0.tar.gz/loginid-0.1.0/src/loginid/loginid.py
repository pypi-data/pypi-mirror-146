from os import error
import requests
import json
import jwt
from .errors import LoginIDError

import random
from datetime import datetime
import base64
import hashlib

from typing import Optional


class LoginID:
    DEFAULT_JWT_ALOGORITHM = 'ES256'
    SUPPORTED_JWT_ALGORITHMS = {DEFAULT_JWT_ALOGORITHM}
    DEFAULT_BASE_URL = "https://directweb.usw1.loginid.io"

    ALLOWED_CODE_TYPES = {'short', 'long', 'phrase'}

    def __init__(self, client_id: str, private_key: str, base_url: str) -> None:
        """ This server SDK leverages either a web or mobile application
        and requires an API credential to be assigned to that integration.

        Args:
            client_id (str): The client ID
            private_key (str): API private key
            base_url (str): LoginID serivce address

        Example::

            from loginid import LoginID
            lid = LoginID(CLIENT_ID, PRIVATE_KEY)


        """
        self._private_key = private_key
        self._client_id = client_id
        self._base_url = (base_url or self.DEFAULT_BASE_URL).rstrip('/')

    def client_id(self) -> str:
        """Extract the client id

        Returns:
            str: The client id
        """
        return self._client_id

    #### Begin Helper Functions ####
    def _get_utc_epoch(self):
        """
        returns the current UTC epoch in seconds
        """
        return int((datetime.utcnow()-datetime(1970, 1, 1)).total_seconds())

    def _random_string(self, length: int = 16) -> str:
        """
        Generate a random string of given length with alphanumeric characters

        Args:
            length (int): length of the output string

        Returns:
            str: a random string
        """
        possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        ret = [random.choice(possible) for _ in range(length)]
        return "".join(ret)

    def _get_public_key(self, kid: Optional[str] = None) -> str:
        """Return the server's public key with `kid`

        Args:
            kid (str, optional): the kid included in jwt's header. Defaults to "".

        Returns:
            str: The public key in PEM format
        """
        # ensure kid is not None
        kid = kid or ""

        params = {"kid": kid} if kid else None

        r = requests.get(f'{self._base_url}/certs', params=params)
        if (r.status_code != 200):
            error = r.json()
            raise LoginIDError(
                r.status_code, error['code'], error['message'])

        # TODO: cache the public key
        return r.text

    def _update_payload(self, payload: dict, user_id: Optional[str] = None, username: Optional[str] = None) -> None:
        """Update payload with user_id and username if present

        Args:
            payload (dict): payload to be updated
            user_id (str, optional): user id to be updated. Defaults to None.
            username (str, optional): username to be updated. Defaults to None.
        """

        # verify that either user_id or username is present
        if not (user_id or username):
            raise LoginIDError(
                400, "bad_request", "either `user_id` or `username` must be present")

        if user_id:
            payload['user_id'] = user_id
        if username:
            payload['username'] = username

    def _request(self, method: str, url: str, token_scope: Optional[str] = None,
                 payloads: Optional[dict] = None, params: Optional[dict] = None,
                 headers: Optional[dict] = None, expect=200) -> dict:
        """
        Make a request to the LoginID service
        """
        methods = {
            'post': requests.post,
            'get': requests.get,
            'put': requests.put,
            'delete': requests.delete
        }
        r_method = methods.get(method.lower(), None)
        if r_method is None:
            raise LoginIDError(400, "INVALID_METHOD", "Invalid method")

        if headers is None:
            headers = headers or {
                "Content-type": "application/json",
                "Authorization": "Bearer " + self.generate_service_token(token_scope),
                "X-Client-ID": self._client_id
            }

        _url = f'{self._base_url}{url}'
        print(f'{method} {_url}')
        if payloads is not None:
            r = r_method(_url, data=json.dumps(payloads), headers=headers)
        else:
            r = r_method(_url, params=params, headers=headers)

        if (r.status_code != expect):
            try:
                error = r.json()
            except Exception:
                raise LoginIDError(500, 'UNKNOWN_ERROR', r.text)

            raise LoginIDError(
                r.status_code,
                error.get('code', 'UNKNOWN_ERROR'),
                error.get('message', r.text or "Unknown error")
            )
        # only return json if there is a response
        return r.json() if expect != 204 else {}

    #### End Helper Functions ####

    def verify_token(self, token: str, username: Optional[str] = None) -> bool:
        """Verify a JWT token returned upon user authorization

        Args:
            token (str): JWT token
            username (str, optional): if given, checks for if `username` matches the `udata` in JWT. Defaults to None.

        Returns:
            bool: `True` if the token is valid, `False` otherwise (including errors)
        """

        try:
            headers = jwt.get_unverified_header(token)

            # extract algo, kid from headers, default to None
            algo, kid = headers.get('alg'), headers.get('kid')

            # verify that algo is supported
            assert algo in self.SUPPORTED_JWT_ALGORITHMS, f"{algo} is not an allowed algorithm."

            # obtain public key from LogInID
            public_key = self._get_public_key(kid)

            payload = jwt.decode(
                token, public_key,
                algorithms=algo, audience=self._client_id
            )

            if username is not None:
                return username == payload['udata']
            return True
        except:
            return False

    def generate_service_token(self, scope: str,
                               username: Optional[str] = None, user_id: Optional[str] = None,
                               algo: Optional[str] = None, nonce: Optional[str] = None) -> str:
        """
        Generate a service token

        Args:
            scope (str): the scope of the service
            username (str, optional): the username to-be granted by the token
            user_id (str, optional): the user_id to be granted by the token. If `username` is given, this is ignored
            algo (str, optional): Encryption algorithm, defaults to `"ES256"`
            nonce (str, optional): nonce for the token, randomly generated if not given

        Returns:
            str: the JWT service token
        """
        algo = algo or self.DEFAULT_JWT_ALOGORITHM
        assert algo in self.SUPPORTED_JWT_ALGORITHMS, f"{algo} is not an allowed algorithm."

        payloads = {
            "client_id": self._client_id,
            "type": scope,
            "nonce": nonce or self._random_string(16),
            "iat": self._get_utc_epoch()
        }

        if username is not None:
            payloads['username'] = username
        elif user_id is not None:
            payloads['user_id'] = user_id

        jwt_headers = {"alg": algo, "typ": "JWT"}

        return jwt.encode(
            payloads, self._private_key, algorithm=algo,
            headers=jwt_headers
        )

    # Tx Flow
    def generate_tx_auth_token(self, tx_payload: str,
                               nonce: Optional[str] = None,
                               algo: Optional[str] = None) -> str:
        """Generate an Authorization Token for Transaction Flow

        Args:
            tx_payload (str): The transaction payload
            username (str, optional): The username
            nonce (str, optional): optional nonce for the token, auto-generated if not given
            algo (str, optional): Encryption algorithm, defaults to `"ES256"`

        Returns:
            str: The JWT authorization token
        """

        algo = algo or self.DEFAULT_JWT_ALOGORITHM
        assert algo in self.SUPPORTED_JWT_ALGORITHMS, f"{algo} is not an allowed algorithm."

        # hash and encode tx_payload
        payload_hash = hashlib.sha256(tx_payload.encode()).digest()
        payload_hash = (base64.urlsafe_b64encode(payload_hash)
                              .decode().strip('=')
                        )

        payloads = {
            'type': 'tx.create',
            'nonce': nonce or self._random_string(16),
            'payload_hash': payload_hash,
            'iat': self._get_utc_epoch()
        }

        return jwt.encode(
            payloads, self._private_key,
            algorithm=algo,
            headers={'alg': algo, 'typ': 'JWT'}
        )

    def create_tx(self, tx_payload: str, nonce: str = None) -> str:
        """Create a transaction and return its ID

        Args:
            tx_payload (str): The transaction payload
            username (str, optional): The username that initiates the transaction
            nonce (str, optional): The optional nonce, randomly generated if not provided


        Returns:
            str: The transaction id if no error
        """

        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + self.generate_tx_auth_token(tx_payload)
        }
        payloads = dict(
            client_id=self._client_id,
            tx_payload=tx_payload,
            nonce=nonce or self._random_string()
        )

        return self._request('post', "/tx", payloads=payloads, headers=headers)['id']

    def verify_transaction(self, tx_token: str, tx_payload: str) -> bool:
        """Verify the jwt token returned upon completion of a transaction

        Args:
            tx_token (str): The JWT token
            tx_payload (str): the original transaction payload

        Returns: `True` if the token is valid, `False` if not
        """
        headers = jwt.get_unverified_header(tx_token)
        algo, kid = headers.get('alg'), headers.get('kid', '')
        if algo not in self.SUPPORTED_JWT_ALGORITHMS:
            raise ValueError(f"{algo} is not an allowed algorithm")

        # get public key
        public_key = self._get_public_key(kid)

        payload = jwt.decode(tx_token, public_key, algorithms=algo,
                             audience=self._client_id)

        to_hash = "".join([
            tx_payload,
            payload.get("nonce", ""),
            payload.get("server_nonce", "")
        ])
        hash = hashlib.sha256(to_hash.encode()).digest()
        hash = base64.urlsafe_b64encode(hash).decode().strip('=')

        return payload.get('tx_hash') == hash

    # Code
    def validate_code_type(self, code_type: str) -> None:
        """Check if a code type is valid, raise an error if not

        Args:
            code_type (str): code type

        """
        if code_type not in self.ALLOWED_CODE_TYPES:
            raise LoginIDError(400, 'BAD_REQUEST',
                               f"{code_type} is not a valid code type")

    def wait_code(self, username: str, code: str, code_type: str, no_jwt: bool = False) -> dict:
        """ Wait for a given code

        Args:
            username (str): The username
            code (str): The code associate to the username
            code_type (str): Type of the code
            no_jwt (bool, optional): If `True`, a JWT token will not be included in the response. Defaults to `False`

        Returns: response json
        """
        self.validate_code_type(code_type)
        no_jwt = bool(no_jwt)

        url = f'/authenticate/code/wait'

        payloads = {
            "client_id": self._client_id,
            "username": username,
            "authentication_code": {
                "code": code,
                "type": code_type
            },
            "no_jwt": no_jwt
        }

        r = self._request('post', url, payloads=payloads)
        json_response = r.json()

        # only validate the JWT if no_jwt is False
        if not no_jwt:
            token = json_response.get('jwt')
            if (token is None) or (not self.verify_token(token)):
                raise LoginIDError(500, "internal_error", "Invalid token")

        return json_response
