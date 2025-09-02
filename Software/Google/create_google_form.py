import os
from typing import List, Tuple

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as UserCredentials
from googleapiclient.http import MediaFileUpload


def read_triplets_from_excel(xlsx_path: str) -> List[Tuple[str, str, str]]:
    """读取包含三列的数据：标准答案、候选1、候选2。

    要求表头至少包含下列任一命名组合（不区分大小写、忽略前后空格）：
    - [ground truth, candidate 1, candidate 2]
    - [标准答案, 模型答案1, 模型答案2]


    返回：[(标准, 候选1, 候选2), ...]
    """
    if not os.path.exists(xlsx_path):
        raise FileNotFoundError(f"Excel Not Found: {xlsx_path}")

    df = pd.read_excel(xlsx_path)
    if df.empty:
        raise ValueError("Empty Excel")

    # 规范化列名
    def norm(col: str) -> str:
        return str(col).strip().lower()

    col_map = {norm(c): c for c in df.columns}

    # 可能的列名集合
    possible_gt = ["ground truth", "ground_truth", "标准答案"]
    possible_c1 = ["candidate 1", "candidate1", "模型答案1"]
    possible_c2 = ["candidate 2", "candidate2", "模型答案2"]

    def pick(possible: List[str]) -> str:
        for p in possible:
            if norm(p) in col_map:
                return col_map[norm(p)]
        raise KeyError(f"Excel Missing Required Columns: {possible}")

    gt_col = pick(possible_gt)
    c1_col = pick(possible_c1)
    c2_col = pick(possible_c2)

    triplets: List[Tuple[str, str, str]] = []
    for _, row in df[[gt_col, c1_col, c2_col]].iterrows():
        gt = str(row[gt_col]).strip()
        c1 = str(row[c1_col]).strip()
        c2 = str(row[c2_col]).strip()
        if not (gt and c1 and c2) or gt.lower() == "nan":
            continue
        triplets.append((gt, c1, c2))

    if not triplets:
        raise ValueError("No Valid Triplets")

    return triplets




if __name__ == "__main__":
    # 默认读取当前目录下的 sourse.xlsx
    xlsx_path = os.environ.get(
        "XLSX_PATH", os.path.join(os.path.dirname(__file__), "sourse.xlsx")
    )
    items = read_triplets_from_excel(xlsx_path)

    # 构建 Google Forms 客户端
    auth_mode = os.environ.get("AUTH_MODE", "oauth").lower()  # service | oauth

    scopes = [
        "https://www.googleapis.com/auth/forms.body",
        "https://www.googleapis.com/auth/drive.file",
    ]

    if auth_mode == "oauth":
        # 用户 OAuth：优先读取已有 token.json，否则走浏览器授权
        token_path = os.path.join(os.path.dirname(__file__), "token.json")
        creds = None
        if os.path.exists(token_path):
            creds = UserCredentials.from_authorized_user_file(token_path, scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                client_secret_path = os.environ.get(
                    "OAUTH_CLIENT_SECRET",
                    os.path.join(os.path.dirname(__file__), "client_secret.json"),
                )
                if not os.path.exists(client_secret_path):
                    raise FileNotFoundError(
                        "OAuth 模式需要 client_secret.json。请设置 OAUTH_CLIENT_SECRET 或放置到脚本同目录。"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, scopes)
                creds = flow.run_local_server(port=0)
            with open(token_path, "w") as token:
                token.write(creds.to_json())
    else:
        # 服务账号
        credentials_path = os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS",
            os.path.join(os.path.dirname(__file__), "medgen-credential.json"),
        )
        if not os.path.exists(credentials_path):
            raise FileNotFoundError("credential not found")
        creds = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=scopes
        )

    forms = build("forms", "v1", credentials=creds)
    drive = build("drive", "v3", credentials=creds)

    # 如果提供了本地图片路径，则先上传到 Drive 并开放“任何人可查看”，获取直链
    image_uri_global: str | None = None
    image_local = os.path.join(os.path.dirname(__file__), "cell.png")
    if image_local and os.path.exists(image_local):
        file_meta = {"name": os.path.basename(image_local), "mimeType": None}
        media = MediaFileUpload(image_local, resumable=False)
        uploaded = drive.files().create(body=file_meta, media_body=media, fields="id").execute()
        file_id = uploaded["id"]
        # 公开为任何人可读
        drive.permissions().create(fileId=file_id, body={"type": "anyone", "role": "reader"}).execute()
        # 构造可直接访问的链接
        image_uri_global = f"https://drive.google.com/uc?export=download&id={file_id}"

    # 为每个三元组创建一个独立表单（每个表单仅一道题）
    links: List[str] = []
    for idx, (gt, c1, c2) in enumerate(items):
        form_body = {
            "info": {
                "title": f"MedGen Project : Evaluation Q{idx + 1}",
                "documentTitle": f"MedGen Project : Evaluation Q{idx + 1}",
            }
        }
        created = forms.forms().create(body=form_body).execute()
        form_id = created["formId"]

        # 清理换行，Forms API 不允许 displayed text 含换行
        def oneline(text: str) -> str:
            return " ".join(str(text).splitlines()).strip()

        requests = []

        if image_uri_global:
            requests.append({
                "createItem": {
                    "item": {
                        "imageItem": {
                            "image": {
                                "sourceUri": image_uri_global,
                                "altText": "illustration"
                            }
                        }
                    },
                    "location": {"index": 0}
                }
            })

        requests.append({
            "createItem": {
                "item": {
                    "title": f"Question {idx + 1}: Choose the closer option",
                    "description": f"Standard Answer: {oneline(gt)}",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": f"Candidate 1: {oneline(c1)}"},
                                    {"value": f"Candidate 2: {oneline(c2)}"},
                                ],
                                "shuffle": True,
                            },
                        }
                    },
                },
                "location": {"index": 0},
            }
        })

        forms.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()
        form_url = f"https://docs.google.com/forms/d/{form_id}/viewform"
        links.append(form_url)
        print(f"Q{idx + 1} link: {form_url}")

    # 写入链接到文本文件
    out_path = os.environ.get(
        "LINKS_OUT", os.path.join(os.path.dirname(__file__), "form_links.txt")
    )
    with open(out_path, "w", encoding="utf-8") as f:
        for i, url in enumerate(links, 1):
            f.write(f"Q{i}\t{url}\n")
    print(f"Created {len(items)} standalone forms. Links saved to: {out_path}")


"""
启用 API
1. 顶部选择你的项目 MedGen
2. 左侧 菜单 → API 和服务 → 库
3. 搜索并启用：Google Forms API、Google Drive API

创建服务账号并下载 JSON
1. 左侧 菜单 → IAM 和管理 → 服务帐号
2. 点击 创建服务帐号 → 填名称 → 创建并继续
3. 角色可先跳过（默认即可）；点 完成
4. 回到服务帐号列表，点刚创建的那一行 → 标签页“密钥”
5. 点 添加密钥 → 创建新密钥 → 选择 JSON → 创建（会自动下载）
6. 把下载的文件保存为： /home/lzy/Projects/Blog/Software/Google/credentials.json

在 GCP 创建“桌面应用”OAuth 客户端，并下载 client_secret.json：
1. 控制台 → API 和服务 → 凭据 → 创建凭据 → OAuth 客户端ID → 应用类型选“桌面应用”

OAuth 权限请求页面 → 目标对象 → 测试用户

forms.google.com

export XLSX_PATH=/home/lzy/Projects/Blog/Software/Google/sourse.xlsx
export GOOGLE_APPLICATION_CREDENTIALS=/home/lzy/Projects/Blog/Software/Google/medgen-credential.json
echo $GOOGLE_APPLICATION_CREDENTIALS
"""
