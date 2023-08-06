import typing

import requests

import FCSAPIAccess.scope as scopes
import FCSAPIAccess.exceptions as exceptions

import FCSAPIAccess.fcs_monitoring as fcs_monitoring
import FCSAPIAccess.fcs_notification as fcs_notification
import FCSAPIAccess.fcs_project as fcs_project


class FCSAPIAccess:
    url_base = "https://fangcloudservices.pythonanywhere.com/api/v1"

    def __init__(
            self, client_id: str, client_secret: str, scope: typing.Union[typing.List[scopes.Scope], scopes.Scope]
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope

        if isinstance(self._scope, scopes.Scope):
            self._scope = [self._scope]

        self._access_token, self._refresh_token = self.client_credentials()

        self.monitoring = fcs_monitoring.FangMonitoringServices(self._access_token)
        self.notification = fcs_notification.FangNotificationServices(self._access_token)
        self.project = fcs_project.FangCloudServicesAPI(self._access_token)

        self._composite_objects = [
            self.monitoring,
            self.notification,
            self.project
        ]

        for o in self._composite_objects:
            o._status_check = self._check_status

    def client_credentials(self) -> typing.Tuple[str, str]:
        r = requests.post(self.url_base + "/project/oauth2", json={
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "scope": self.get_scope_string()
        })

        if r.status_code == 400:
            if r.json()["error"] == "invalid_grant":
                raise exceptions.InvalidGrantException(
                    "The provided client_id and client_secret do not match an active application"
                )

        approved_scope: str = r.json()["scope"]
        self._scope = [scopes.Scope(s) for s in approved_scope.split(" ")]

        return r.json()["access_token"], r.json()["refresh_token"]

    def refresh_token(self) -> typing.Tuple[str, str]:
        r = requests.post(self.url_base + "/project/oauth2", json={
            "grant_type": "refresh_token",
            "client_id": self._client_id,
            "access_token": self._access_token,
            "refresh_token": self._refresh_token
        })
        return r.json()["access_token"], r.json()["refresh_token"]

    def get_scope_string(self) -> str:
        return " ".join(s.value for s in self._scope)

    def set_access_token(self, access_token: str, refresh_token: str = None):
        self._access_token = access_token

        if refresh_token is not None:
            self._refresh_token = refresh_token

        for o in self._composite_objects:
            o.headers = {'Authorization': 'Bearer {}'.format(access_token)}

    def is_approved(self, scope: scopes.Scope):
        return scope in self._scope

    def scope(self) -> typing.List[scopes.Scope]:
        return self._scope

    def _check_status(self, r: requests.Response, retry: callable):
        if r.status_code == 400:
            response = r.json()

            if "error" in response:
                if response["error"] == "expired_code":
                    self.set_access_token(*self.refresh_token())
                    return retry()

        if r.status_code == 500:
            try:
                raise exceptions.APIErrorException(r.json()["message"])
            except KeyError:
                raise exceptions.APIErrorException(
                    "An unknown server has occurred. Please contact support for more info"
                )
