from django.conf import settings
from requests_oauthlib import OAuth2Session

ZOOM_AUTHORIZATION_BASE_URL = "https://zoom.us/oauth/authorize"
ZOOM_TOKEN_URL = "https://zoom.us/oauth/token"


def get_zoom_oauth_session(state=None, token=None):
    return OAuth2Session(
        client_id=settings.ZOOM_CLIENT_ID,
        redirect_uri=settings.ZOOM_REDIRECT_URI,
        state=state,
        token=token
    )


def get_zoom_authorization_url():
    zoom = get_zoom_oauth_session()
    authorization_url, state = zoom.authorization_url(ZOOM_AUTHORIZATION_BASE_URL)
    return authorization_url, state


def fetch_zoom_token(code):
    zoom = get_zoom_oauth_session()
    token = zoom.fetch_token(
        ZOOM_TOKEN_URL,
        code=code,
        client_secret=settings.ZOOM_CLIENT_SECRET
    )
    return token
