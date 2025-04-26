import os
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL
from outlook import search_folder, get_messages, get_sub_folders

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
        folder_name = 'Inbox'
        target_folder = search_folder(headers, folder_name)
        folder_id = target_folder['id']

        print(folder_id)

        messages = get_messages(
            headers,
            folder_id=folder_id,
        )

        for message in messages:
            print("Subject:", message['subject'])
            print("-"*50)

        sub_folders = get_sub_folders(headers, folder_id)
        for sub_folder in sub_folders:
            if sub_folder['displayName'].lower() == 'SubFolder'.lower():
                sub_folder_id = sub_folder['id']
                messages = get_messages(
                    headers,
                    folder_id=sub_folder_id,
                )
                for message in messages:
                    print(f"Sub Folder Name: {sub_folder['displayName']}")
                    print("Subject:", message['subject'])
                    print("-"*50)

    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    main()



