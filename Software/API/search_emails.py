import os
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL
from outlook import get_messages, search_folder, search_messages


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
        search_query = "👋"
        messages = search_messages(headers, search_query)

        for index, message in enumerate(messages):
            print(f"Email {index + 1}:")
            print("Subject:", message['subject'])
            print("To:", message['toRecipients'])
            print("Is Read:", message['isRead'])
            print("Received Date:", message['receivedDateTime'])
            print("-" * 50)

    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()