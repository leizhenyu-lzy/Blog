import re

asset_path = "*abc*"

print(re.match(r"^[a-zA-Z0-9/_]+$", asset_path))

print(re.match(r"^[a-zA-Z0-9/_]+$", asset_path) is None)

asset_path = "abc"

print(re.match(r"^[a-zA-Z0-9/_]+$", asset_path))

print(re.match(r"^[a-zA-Z0-9/_]+$", asset_path) is None)

