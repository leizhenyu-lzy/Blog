import os
import re
from typing import List, Tuple, Dict

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as UserCredentials


SCOPES = [
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/forms.body.readonly",
]


def load_links(txt_path: str) -> List[Tuple[str, str]]:
    links: List[Tuple[str, str]] = []
    if not os.path.exists(txt_path):
        raise FileNotFoundError(f"Links file not found: {txt_path}")
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")  # 格式: Q{n}\tURL
            if len(parts) != 2:
                continue
            label, url = parts
            links.append((label, url))
    return links


def extract_form_id(url: str) -> str:
    m = re.search(r"/d/([a-zA-Z0-9_-]+)/", url)
    if not m:
        raise ValueError(f"Cannot extract formId from url: {url}")
    return m.group(1)


def get_credentials() -> UserCredentials:
    token_path = os.path.join(os.path.dirname(__file__), "token.json")
    creds = None
    if os.path.exists(token_path):
        creds = UserCredentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_secret_path = os.environ.get(
                "OAUTH_CLIENT_SECRET",
                os.path.join(os.path.dirname(__file__), "client_secret.json"),
            )
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return creds


def summarize_responses(forms_service, form_id: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    next_page_token = None
    while True:
        resp = forms_service.forms().responses().list(formId=form_id, pageToken=next_page_token).execute()
        for ans in resp.get("responses", []):
            answers = ans.get("answers", {})
            if not answers:
                continue
            first_key = next(iter(answers.keys()))
            choice = (
                answers[first_key]
                .get("textAnswers", {})
                .get("answers", [{}])[0]
                .get("value", "")
            )
            if choice:
                counts[choice] = counts.get(choice, 0) + 1
        next_page_token = resp.get("nextPageToken")
        if not next_page_token:
            break
    return counts


def main():
    links_path = os.path.join(os.path.dirname(__file__), "form_links.txt")
    links = load_links(links_path)

    creds = get_credentials()
    forms = build("forms", "v1", credentials=creds)

    for label, url in links:
        form_id = extract_form_id(url)
        counts = summarize_responses(forms, form_id)
        total = sum(counts.values())
        print(f"=== {label} | formId={form_id} | total={total} ===")
        if not counts:
            print("(no responses)")
            continue
        for option, cnt in counts.items():
            pct = (cnt / total * 100.0) if total else 0.0
            print(f"{option}: {cnt} ({pct:.1f}%)")


if __name__ == "__main__":
    main()
