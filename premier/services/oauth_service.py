import base64
import os
import requests

class OAuthService:
    def __init__(self):
        self.token_url = os.getenv("OAUTH_SERVICE")

    def get_access_token(self):
        payload = 'grant_type=client_credentials'
        consumerKey = os.getenv("OATH_CONSUMER_KEY")
        consumerSecretKey = os.getenv("OATH_CONSUMER_SECRET_KEY")
        input_bytes = ':'.join([consumerKey, consumerSecretKey]).encode('utf-8')
        base64_encoded = base64.b64encode(input_bytes)
        base64_decoded = base64_encoded.decode('utf-8')
        
        auth = 'Basic ' + base64_decoded
        headers = {
                    'Authorization': auth,
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
        try:
            response = requests.request("POST", self.token_url, headers=headers, data=payload)
            token_data = response.json()
            access_token = token_data.get("access_token")
            return access_token
        except requests.exceptions.RequestException as e:
            raise Exception("Error retrieving access token") from e
