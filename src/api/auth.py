import webbrowser
from fyers_apiv3 import fyersModel
from src.config import CLIENT_ID, SECRET_KEY, REDIRECT_URI

def generate_auth_code():
    """Initiates the login flow and returns the auth link."""
    session = fyersModel.SessionModel(
        client_id=CLIENT_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code"
    )
    return session, session.generate_authcode()

def get_token_from_auth_code(auth_code):
    """Exchanges auth_code for an access_token."""
    session, _ = generate_auth_code()
    session.set_token(auth_code)
    response = session.generate_token()
    return response