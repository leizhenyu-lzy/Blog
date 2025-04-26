import os
import webbrowser
import msal
from dotenv import load_dotenv

MS_GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

def get_access_token(application_id, client_secret, scopes):
    """
    handle the authentication process and return an access token for Microsoft Graph API
    """
    client = msal.ConfidentialClientApplication(
        client_id=application_id,
        client_credential=client_secret,
        authority='https://login.microsoftonline.com/consumers/'
    )  # application that can securely store your client secret

    # check if there is a refresh token stored
    refresh_token = None
    if os.path.exists('refresh_token.txt'):
        with open('refresh_token.txt', 'r') as file:
            refresh_token = file.read().strip()

    if refresh_token:
        # try to acquire a new access token using the refresh token
        token_response = client.acquire_token_by_refresh_token(refresh_token, scopes=scopes)
    else:
        # No refresh token, proceed with the authorization code flow using the get authorization request URL
        auth_request_url = client.get_authorization_request_url(scopes)
        webbrowser.open(auth_request_url)
        authorization_code = input('Enter the authorization code: ')

        if not authorization_code:
            raise ValueError("Authorization code is empty")

        token_response = client.acquire_token_by_authorization_code(
            code=authorization_code,
            scopes=scopes
        )

    if 'access_token' in token_response:
        # store the refresh token securely
        if 'refresh_token' in token_response:
            with open('refresh_token.txt', 'w') as file:
                file.write(token_response['refresh_token'])
        return token_response['access_token']
    else:
        raise ValueError("Failed to acquire access token: " + str(token_response.get('error_description')))



def main():
    load_dotenv()
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES = ["User.Read", "Mail.Read", "Mail.Send"]

    try:
        access_token = get_access_token(APPLICATION_ID, CLIENT_SECRET, SCOPES)
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        print(headers)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()





