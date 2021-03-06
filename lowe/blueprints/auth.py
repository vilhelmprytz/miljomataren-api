from flask import Blueprint, request, abort, session, redirect
from requests import get, post
from json import dumps
from oauthlib.oauth2 import WebApplicationClient

from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, BASE_URL, FRONTEND_URL
from models import APIResponse
from orm import User

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

auth_blueprint = Blueprint("auth", __name__)

# oauth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return get(GOOGLE_DISCOVERY_URL).json()


@auth_blueprint.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=f"{BASE_URL}/api/auth/callback",
        scope=["openid", "email", "profile"],
    )

    return APIResponse(response={"login_uri": request_uri}).serialize()


@auth_blueprint.route("/callback")
def callback():
    # Get authorization code Google sent back
    code = request.args.get("code")

    # What URL do we need to request to in order to do things on
    # behalf of the user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=f"{BASE_URL}/api/auth/callback",
        code=code,
    )
    token_response = post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse tokens
    client.parse_request_body_response(dumps(token_response.json()))

    # Get basic user information (email, name, profile_picture..)
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = get(uri, headers=headers, data=body)

    # Make sure google considers their email as verified
    if userinfo_response.json().get("email_verified"):
        email = userinfo_response.json()["email"]
        user = User.query.filter_by(email=email)

        if len(user.all()) == 0:
            abort(401, "Email is not registered user")
        user = user.first()

        user = {
            "id": user.id,
            "email": email,
            "picture": userinfo_response.json()["picture"],
            "name": userinfo_response.json()["name"],
        }

        # authenticated
        session["authenticated"] = True
        session["user"] = user

        return redirect(FRONTEND_URL)
    else:
        abort(400, "Email not verified by Google or not available")
