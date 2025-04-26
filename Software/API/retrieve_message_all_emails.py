# https://learn.microsoft.com/en-us/graph/api/resources/message?view=graph-rest-1.0

import os
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL


def main():
    load_dotenv()
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES = ["User.Read", "Mail.Read", "Mail.Send"]
    MY_EMAIL = os.getenv('MY_EMAIL')

    endpoint = f"{MS_GRAPH_BASE_URL}/me/messages"  # API endpoint to retrieve all messages

    try:
        access_token = get_access_token(APPLICATION_ID, CLIENT_SECRET, SCOPES)
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        for i in range(0,4,1):
            params = {
                '$top': 1,  # limit the number of emails to retrieve in each API
                '$select': '*',  # field
                '$skip': i,  # Skip previous emails/offset
                '$orderby': 'receivedDateTime desc'  # Order by received date descending
            }

            response = httpx.get(endpoint, headers=headers, params=params)  # get request

            if response.status_code != 200:
                raise Exception(f"Failed to retrieve emails: {response.status_code} - {response.text}")

            json_response = response.json()

            for mail_message in json_response.get('value', []):

                from_info = mail_message.get('from', {}).get('emailAddress', {})
                from_address = from_info.get('address', '').lower()

                if from_address == MY_EMAIL.lower():
                    print("📤 Sent mail     (I am sender)")
                else:
                    print("📥 Received mail (I am recipient)")

                if mail_message['isDraft']:
                    print("[Draft Email]")
                    print("Subject:", mail_message['subject'])
                    print("To:", mail_message['toRecipients'])
                    print("Is Read:", mail_message['isRead'])
                    print("Received Date:", mail_message['receivedDateTime'])
                    print()
                else:
                    print("Subject:", mail_message['subject'])
                    print("To:", mail_message['toRecipients'])
                    print("From:", mail_message['from']['emailAddress']['name'], f"({mail_message['from']['emailAddress']['address']})")
                    print("Is Read:", mail_message['isRead'])
                    print("Received Date:", mail_message['receivedDateTime'])
                    # print("Body:", mail_message['body']['content'])
                    print("Body Preview:", mail_message['bodyPreview'])
                    print()
            print("-"*100)


    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

