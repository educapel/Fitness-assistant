import requests
from dotenv import load_dotenv
import os

load_dotenv()

GRAFANA_URL = os.getenv("GRAFANA_URL")
GRAFANA_USER = os.getenv("GRAFANA_ADMIN_USER")
GRAFANA_PASSWORD = os.getenv("GRAFANA_ADMIN_PASSWORD")


def create_service_account_token():
    auth = (GRAFANA_USER, GRAFANA_PASSWORD)
    headers = {"Content-Type": "application/json"}

    # Step 1: Create a service account
    sa_payload = {
        "name": "ProgrammaticServiceAccount",
        "role": "Admin",
        "isDisabled": False
    }

    print("Creating service account...")
    response = requests.post(
        f"{GRAFANA_URL}/api/serviceaccounts",
        auth=auth,
        headers=headers,
        json=sa_payload
    )

    if response.status_code == 201:
        service_account = response.json()
        sa_id = service_account["id"]
        print(f"Service account created with ID: {sa_id}")
    elif response.status_code == 409:
        print("Service account already exists, finding existing one...")
        # Get existing service accounts
        response = requests.get(f"{GRAFANA_URL}/api/serviceaccounts/search", auth=auth)
        if response.status_code == 200:
            accounts = response.json()["serviceAccounts"]
            sa_id = None
            for account in accounts:
                if account["name"] == "ProgrammaticServiceAccount":
                    sa_id = account["id"]
                    break
            if not sa_id:
                print("Could not find existing service account")
                return None
        else:
            print(f"Failed to get service accounts: {response.text}")
            return None
    else:
        print(f"Failed to create service account: {response.text}")
        return None

    # Step 2: Create a token for the service account
    token_payload = {
        "name": "ProgrammaticToken",
        "role": "Admin"
    }

    print(f"Creating token for service account {sa_id}...")
    response = requests.post(
        f"{GRAFANA_URL}/api/serviceaccounts/{sa_id}/tokens",
        auth=auth,
        headers=headers,
        json=token_payload
    )

    if response.status_code == 200:
        token_data = response.json()
        print("Service account token created successfully!")
        print(f"Token: {token_data['key']}")
        return token_data['key']
    else:
        print(f"Failed to create token: {response.text}")
        return None


def create_legacy_api_key():
    """Try the legacy API key method for older Grafana versions"""
    auth = (GRAFANA_USER, GRAFANA_PASSWORD)
    headers = {"Content-Type": "application/json"}

    # Try different endpoints
    endpoints = [
        "/api/auth/keys",
        "/api/admin/keys",
        "/api/api-keys"
    ]

    payload = {
        "name": "ProgrammaticKey",
        "role": "Admin",
        "secondsToLive": None  # Never expires
    }

    for endpoint in endpoints:
        print(f"Trying {endpoint}...")
        try:
            response = requests.post(
                f"{GRAFANA_URL}{endpoint}",
                auth=auth,
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                print(f"Success with {endpoint}!")
                return response.json()["key"]
            else:
                print(f"{endpoint} failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"{endpoint} error: {e}")

    return None


def main():
    print("Attempting to create Grafana API credentials...")
    print("=" * 60)

    # First try service account tokens (modern approach)
    token = create_service_account_token()

    if not token:
        print("\nService account approach failed, trying legacy API keys...")
        token = create_legacy_api_key()

    if token:
        print(f"\n✅ Success! Your API token is: {token}")
        print("\nAdd this to your .env file:")
        print(f"GRAFANA_API_KEY={token}")
    else:
        print("\n❌ Failed to create API credentials")
        print("\nPlease check:")
        print("1. Grafana is running and accessible")
        print("2. Username/password are correct")
        print("3. User has admin privileges")


if __name__ == "__main__":
    main()