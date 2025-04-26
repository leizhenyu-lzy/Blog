# https://learn.microsoft.com/en-us/graph/api/resources/emailaddress?view=graph-rest-1.0

import os
import httpx
from dotenv import load_dotenv
import mimetypes
import base64
from ms_graph import get_access_token, MS_GRAPH_BASE_URL
from pathlib import Path


def search_folder(headers, folder_name='drafts'):
    """
    Search for a folder by name and return its ID
    """
    endpoint = f"{MS_GRAPH_BASE_URL}/me/mailFolders"
    response = httpx.get(endpoint, headers=headers)
    response.raise_for_status()
    folders = response.json().get('value', [])
    for folder in folders:
        if folder['displayName'].lower() == folder_name.lower():
            return folder
    return None


def get_sub_folders(headers, folder_id):
    """
    Get all subfolders of a given folder
    """
    endpoint = f"{MS_GRAPH_BASE_URL}/me/mailFolders/{folder_id}/childFolders"
    response = httpx.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json().get('value', [])


def get_messages(   headers, folder_id=None, fields='*', top=5,
                    order_by="receivedDateTime", order_by_desc=True, max_results=100):
    if folder_id:
        endpoint = f"{MS_GRAPH_BASE_URL}/me/mailFolders/{folder_id}/messages"
    else:
        endpoint = f"{MS_GRAPH_BASE_URL}/me/messages"

    params = {
        '$select': fields,
        '$top': min(top, max_results),
        '$orderby': f"{order_by} {'desc' if order_by_desc else 'asc'}"
    }

    messages = []  # store messages
    next_link = endpoint

    while next_link and len(messages) < max_results:
        response = httpx.get(next_link, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve emails: {response.status_code} - {response.text}")

        json_response = response.json()
        messages.extend(json_response.get('value', []))
        next_link = json_response.get('@odata.nextLink', None)  # next page link URL
        params = None  # clear params for subsequent requests

        if next_link and len(messages) + top > max_results:
            params = {
                '$top': max_results - len(messages)
            }

    return messages[:max_results]


def search_messages(headers, search_query, filter=None, folder_id=None, fileds='*', top=5, max_results=100):
    if folder_id is None:
        endpoint = f"{MS_GRAPH_BASE_URL}/me/messages"
    else:
        endpoint = f"{MS_GRAPH_BASE_URL}/me/mailFolders/{folder_id}/messages"

    params = {
        '$search': f'"{search_query}"',
        '$filter': filter,
        '$select': fileds,
        '$top': min(top, max_results)
    }

    messages = []  # store messages
    next_link = endpoint

    while next_link and len(messages) < max_results:
        response = httpx.get(next_link, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve emails: {response.status_code} - {response.text}")

        json_response = response.json()
        messages.extend(json_response.get('value', []))
        next_link = json_response.get('@odata.nextLink', None)
        params = None

        if next_link and len(messages) + top > max_results:
            params = {
                '$top': max_results - len(messages)
            }
    return messages[:max_results]









