from json import dumps
from typing import Optional
from unittest.mock import patch, MagicMock

from math import floor

import time
from uuid import uuid4

from requests import Response, Request

from dnastack import DataConnectClient
from dnastack.auth.authorizers import ClientCredentialsAuth, PersonalAccessTokenAuth, OAuthTokenAuth, \
    SessionAuthorizationRequired, SessionReauthorizationRequired, SessionRefreshRequired
from dnastack.auth.session_store import Session, InMemorySessionStorage, SessionManager
from dnastack.configuration import Authentication, ServiceEndpoint, Oauth2Authentication
from dnastack.helpers.environments import env
from ..exam_helper import token_endpoint, client_secret, client_id, \
    authorization_endpoint, personal_access_endpoint, redirect_url, ExtendedBaseTestCase


class FauxSessionCreator:
    def __init__(self,
                 config_hash: str,
                 expiry_timestamp_delta: int,
                 refresh_token: Optional[str] = None):
        self.config_hash = config_hash
        self.expiry_timestamp_delta = expiry_timestamp_delta
        self.refresh_token = refresh_token

    def __call__(self, request_url: Optional[str] = None) -> Session:
        return self.make(self.config_hash, self.expiry_timestamp_delta, self.refresh_token)

    @staticmethod
    def make(config_hash: str,
             expiry_timestamp_delta: int,
             refresh_token: Optional[str] = None):
        current_timestamp = floor(time.time())
        return Session(config_hash=config_hash,
                       access_token='faux_access_token',
                       refresh_token=refresh_token,
                       token_type='faux_token_type',
                       issued_at=current_timestamp,
                       valid_until=current_timestamp + expiry_timestamp_delta)


class BaseAuthTest(ExtendedBaseTestCase):
    def _trigger_authorization_process(self, auth: OAuthTokenAuth):
        request = Request()
        auth(request)
        self.assertIsNotNone(auth._session)
        self.assertIn('Authorization', request.headers)


class TestAuthorizerUnitTest(BaseAuthTest):
    """
    Unit tests for authorizers

    .. note::
        (1) Please note that most of the time, the test will overwrite the "create_session" method of each
        OAuthTokenAuth. This will not affect the original implementation of the method.
    """

    auth_info = Authentication(oauth2=Oauth2Authentication(grant_type='client_credentials',
                                                           resource_url='https://foo.bar'))
    service_endpoint = ServiceEndpoint(
        id='test_endpoint',
        adapter_type='test_adapter',
        url='http://localhost:12345/',
        authentication=auth_info
    )

    def test_authorizer_authorize_first_time(self):
        session_storage = InMemorySessionStorage()
        session_manager = SessionManager(session_storage)

        auth = OAuthTokenAuth(self.service_endpoint, session_manager)
        auth.create_session = FauxSessionCreator(self.auth_info.get_content_hash(), 3600)  # See note (1)

        with self.assertRaises(SessionAuthorizationRequired):
            # noinspection PyStatementEffect
            auth.session

        self._trigger_authorization_process(auth)

        current_session = auth.session

        self.assertIsNotNone(current_session)
        self.assertGreater(current_session.valid_until, time.time())
        self.assertTrue(current_session.is_valid())

    def test_authorizer_handles_auth_info_update_with_reauthorization(self):
        session_with_old_config = FauxSessionCreator.make('old_config_hash', 60)
        session_storage = InMemorySessionStorage()
        session_storage['test_endpoint'] = session_with_old_config
        session_manager = SessionManager(session_storage)

        auth = OAuthTokenAuth(self.service_endpoint, session_manager)
        auth.create_session = FauxSessionCreator(self.auth_info.get_content_hash(), 60)  # See note (1)

        with self.assertRaises(SessionReauthorizationRequired):
            # noinspection PyStatementEffect
            auth.session

        self._trigger_authorization_process(auth)

        current_session = auth.session

        self.assertIsNotNone(current_session)
        self.assertNotEqual(current_session, session_with_old_config)
        self.assertTrue(current_session.is_valid())

    def test_authorizer_handles_stale_session_with_reauthorization(self):
        stale_session = FauxSessionCreator.make(self.auth_info.get_content_hash(), -60)
        session_storage = InMemorySessionStorage()
        session_storage['test_endpoint'] = stale_session
        session_manager = SessionManager(session_storage)

        auth = OAuthTokenAuth(self.service_endpoint, session_manager)
        auth.create_session = FauxSessionCreator(self.auth_info.get_content_hash(), 60)  # See note (1)

        with self.assertRaises(SessionReauthorizationRequired):
            # noinspection PyStatementEffect
            auth.session

        self._trigger_authorization_process(auth)

        current_session = auth.session

        self.assertIsNotNone(current_session)
        self.assertNotEqual(current_session, stale_session)
        self.assertGreater(current_session.valid_until, stale_session.valid_until)
        self.assertTrue(current_session.is_valid())
        self.assertFalse(stale_session.is_valid())

    def test_authorizer_handles_stale_session_with_token_refresh(self):
        stale_session = FauxSessionCreator.make(self.auth_info.get_content_hash(), -60, 'faux_refresh_token_1')
        session_storage = InMemorySessionStorage()
        session_storage['test_endpoint'] = stale_session
        session_manager = SessionManager(session_storage)

        auth = OAuthTokenAuth(self.service_endpoint, session_manager)

        with self.assertRaises(SessionRefreshRequired):
            # noinspection PyStatementEffect
            auth.session

        with patch('requests.post') as mock_post_method:
            mock_response = MagicMock(Response)
            mock_response.ok = True
            mock_response.json.return_value = {
                'access_token': 'fake_access_token',
                'refresh_token': 'fake_refresh_token',
                'token_type': 'fake_token_type',
                'expires_in': 100,
            }

            mock_post_method.return_value = mock_response

            self._trigger_authorization_process(auth)

        current_session = auth.session

        self.assertIsNotNone(current_session)
        self.assertNotEqual(current_session, stale_session)
        self.assertGreater(current_session.valid_until, stale_session.valid_until)
        self.assertTrue(current_session.is_valid())
        self.assertFalse(stale_session.is_valid())


class TestEndToEnd(BaseAuthTest):
    """
    Test authentication flows

    .. note:: The URL used in the authorization tests are fake.
    """

    test_resource_url = env('E2E_PROTECTED_DATA_CONNECT_URL', default='https://data-connect-trino.viral.ai/')

    def test_client_credentials_flow(self):
        test_endpoint = self.__create_endpoint(
            client_id=client_id,
            client_secret=client_secret,
            grant_type='client_credentials',
            resource_url=self.test_resource_url,
            token_endpoint=token_endpoint
        )

        auth = ClientCredentialsAuth(test_endpoint)

        self._trigger_authorization_process(auth)

        auth_session = auth.session
        self.assertIsNotNone(auth_session)
        self.assertIsNotNone(auth_session.config_hash)
        self.assert_not_empty(auth_session.access_token, 'empty access token')
        self.assertIsNone(auth_session.refresh_token, 'non-empty refresh token')
        self.assertGreater(auth_session.valid_until, 0)

        # As the OAuth server may respond too quickly, this is to ensure that the expiry times are different.
        time.sleep(1)

        # Reauthorize the endpoint with updated config
        test_endpoint.authentication.oauth2.redirect_url = 'https://dnastack.com/'

        self._trigger_authorization_process(auth)

        refreshed_auth_session = auth.session
        self.assertIsNotNone(refreshed_auth_session)
        self.assertIsNotNone(refreshed_auth_session.config_hash)
        self.assert_not_empty(refreshed_auth_session.access_token, 'empty access token')
        self.assertIsNone(refreshed_auth_session.refresh_token, 'non-empty refresh token')
        self.assertGreater(refreshed_auth_session.valid_until, 0)

        # Check that the session has been refreshed when the auth info is updated.
        self.assertNotEqual(refreshed_auth_session, auth_session)
        self.assertNotEqual(refreshed_auth_session.config_hash, auth_session.config_hash)
        self.assertNotEqual(refreshed_auth_session.access_token, auth_session.access_token)
        self.assertGreater(refreshed_auth_session.valid_until, auth_session.valid_until)

    def test_personal_access_token_flow(self):
        email = env('E2E_AUTH_TEST_PAT_EMAIL')
        token = env('E2E_AUTH_TEST_PAT_TOKEN')

        if not email or not token:
            self.skipTest('The PAT flow test does not have both email and token.')

        auth = PersonalAccessTokenAuth(self.__create_endpoint(
            authorization_endpoint=authorization_endpoint,
            client_id=client_id,
            client_secret=client_secret,
            grant_type='authorization_code',
            personal_access_endpoint=personal_access_endpoint,
            personal_access_email=email,
            personal_access_token=token,
            redirect_url=redirect_url,
            resource_url=self.test_resource_url,
            token_endpoint=token_endpoint,
        ))

        self._trigger_authorization_process(auth)

        auth_session = auth.session
        self.assertIsNotNone(auth_session)
        self.assert_not_empty(auth_session.access_token, 'empty access token')
        self.assert_not_empty(auth_session.refresh_token, 'empty refresh token')
        self.assertGreater(auth_session.valid_until, 0)

    def __create_endpoint(self, **kwargs) -> ServiceEndpoint:
        return ServiceEndpoint(
            id=f'auto-test-{uuid4()}',
            adapter_type=DataConnectClient.get_adapter_type(),
            url=self.test_resource_url,
            authentication=Authentication(oauth2=Oauth2Authentication(**kwargs)),
        )
