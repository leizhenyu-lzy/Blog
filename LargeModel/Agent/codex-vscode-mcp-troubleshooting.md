# Codex 在 VS Code 终端中 MCP 超时的排查记录

记录日期：2026-09-06（Asia/Shanghai）。状态：已配置显式代理，等待用户在新终端验证 MCP 初始化。

## 现象与证据

系统终端运行正常，VS Code 集成终端出现：

```text
MCP client for `codex_apps` timed out after 30 seconds
MCP startup incomplete (failed: codex_apps)
```

早期还出现 `Reconnecting...`；它与 MCP 初始化是不同的连接现象，不能仅凭同时出现断定相互因果。

两个终端的 Codex 均为 `0.153.4`，可执行文件为 `~/.local/bin/codex`，有效配置目录均为 `~/.codex`。用户提供的环境变量对比显示：正常系统终端有大小写 HTTP_PROXY、HTTPS_PROXY、ALL_PROXY、NO_PROXY；失败的 VS Code 终端当时没有这些变量。

VS Code 用户设置原为 `terminal.integrated.inheritEnv: false`，后来改为 `true`。用户反馈重启后仍有 MCP 超时；当时未取得重启后的终端环境输出，因此不能认定代理已成功继承。

本机日志位于 `~/.codex/logs_2.sqlite` 的 `logs` 表。排查时使用只读连接。日志显示向 `https://chatgpt.com/backend-api/ps/mcp` 发送 `initialize` 请求失败，并在 30 秒后握手超时；日志本身没有给出足以确定 DNS、TLS、代理或认证根因的细节。

正常终端的 shell 快照记录 HTTP/HTTPS 代理为 `http://127.0.0.1:7897`，ALL_PROXY 为同端口 SOCKS 地址。代理环境差异是主要线索，尚未完成最终因果验证。

## 为什么排查中出现 sandbox

沙箱是 AI 执行工具命令的受限环境，用于限制文件访问、网络访问等。它与用户亲自运行 Codex 的 VS Code 终端不是同一个执行环境。具体隔离方式取决于运行平台；不能把沙箱测试结果直接当成宿主机结果。

此次在默认沙箱内 curl 连接 `127.0.0.1:7897` 立即失败。经用户批准，在宿主环境执行相同的无凭据请求后，约一秒收到 HTTP 451，正文为：

```json
{"message":"no_biscuit_no_service"}
```

这证明在该次宿主测试中，经过代理能够获得 HTTP 响应；不证明带认证的 MCP 握手成功。也不能仅凭 451 就认定地区限制。沙箱中 localhost 的可达性与宿主可能不同，本次没有进一步确定沙箱失败的具体网络隔离机制。

## 已实施的修改

在 `~/.config/Code/User/settings.json` 中保留 `inheritEnv: true`，新增：

```json
"terminal.integrated.env.linux": {
    "HTTP_PROXY": "http://127.0.0.1:7897",
    "HTTPS_PROXY": "http://127.0.0.1:7897",
    "http_proxy": "http://127.0.0.1:7897",
    "https_proxy": "http://127.0.0.1:7897",
    "ALL_PROXY": "http://127.0.0.1:7897",
    "all_proxy": "http://127.0.0.1:7897"
}
```

这里将 ALL_PROXY 也明确设为已验证能连接的 HTTP 代理地址。配置作用于新建的 VS Code Linux 集成终端及其子进程，依赖本机代理在该端口运行；代理端口变化后需要同步修改。没有改动 NO_PROXY。

修改前备份：`~/.config/Code/User/settings.json.before-codex-proxy`。已检查差异，只有上述配置块新增。没有修改 Codex 的启动超时时间。

## 可执行的配置修改代码

下面脚本用于复现本次修改。它保留文件中的 JSONC 注释和其他设置，自动备份；重复执行不会重复插入配置。如果已有不同的 `terminal.integrated.env.linux` 配置，脚本会停止，避免覆盖自定义变量。适用于本记录中的 VS Code 用户配置格式。

```bash
python3 - <<'PYCONFIG'
from datetime import datetime
from pathlib import Path
import re
import shutil

settings = Path.home() / ".config/Code/User/settings.json"
original = settings.read_text()
proxy = "http://127.0.0.1:7897"  # 本机代理地址，端口改变时同步修改
keys = ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
        "ALL_PROXY", "all_proxy")
block = '    "terminal.integrated.env.linux": {\n'
block += ",\n".join(f'        "{key}": "{proxy}"' for key in keys)
block += '\n    },'

# 针对本次已知配置，要求继承设置恰好出现一次。
pattern = r'(?m)^    "terminal\.integrated\.inheritEnv": (?:true|false),$'
if len(re.findall(pattern, original)) != 1:
    raise SystemExit("配置格式不同：请在设置编辑器中手动合并本文的 JSON 配置。")
updated = re.sub(pattern, '    "terminal.integrated.inheritEnv": true,', original)

# 已有其他终端变量时不自动替换整个对象。
if '"terminal.integrated.env.linux"' in updated:
    if updated.count('"terminal.integrated.env.linux"') != 1 or block not in updated:
        raise SystemExit("已有不同的 Linux 终端环境配置，请手动合并代理变量。")
else:
    anchor = '    "terminal.integrated.inheritEnv": true,'
    updated = updated.replace(anchor, anchor + "\n" + block, 1)

if updated == original:
    print("配置已一致，无需修改。")
else:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = settings.with_name(settings.name + ".before-codex-proxy-" + stamp)
    shutil.copy2(settings, backup)
    settings.write_text(updated)
    print(f"已更新：{settings}\n备份：{backup}")
PYCONFIG
```

执行后结束旧终端、新建终端，再验证（不要只在旧终端重启 Codex）：

```bash
printenv | cut -d= -f1 | grep -i proxy
codex
```

只想临时验证时，可在目标终端运行下面两行；设置仅影响该 shell 及其后续子进程，不写配置文件：

```bash
export HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 http_proxy=http://127.0.0.1:7897 https_proxy=http://127.0.0.1:7897 ALL_PROXY=http://127.0.0.1:7897 all_proxy=http://127.0.0.1:7897
codex
```

## 待验证及下一步

1. 使用终端垃圾桶结束旧终端，创建新终端；旧终端不会自动取得新环境。
2. 检查代理变量，再运行 Codex：

```bash
printenv | cut -d= -f1 | grep -i proxy
codex
```

3. 确认 `codex_apps` 成功初始化，并实际调用一个只读连接器工具。若仍失败，对照新日志和新终端代理值继续排查；变量名存在不代表值正确。
4. 不把增大 `startup_timeout_sec` 当作连接失败的通用修复；只有证据支持启动较慢时再考虑。

回滚时可移除新增的 `terminal.integrated.env.linux` 块。完整恢复备份前先检查是否存在后续设置修改，避免覆盖。

## 与 Lark skills 的关系

`codex_apps` 的 MCP 启动告警本身不能证明 Lark skill 失败。此前当前环境未找到 Lark skills 和 `lark-cli`，相关业务查询使用的是本地项目快照。MCP 连通性、Lark 工具安装和 Lark 认证应分别验证。

参考：[官方 MCP 配置说明](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)。上述具体诊断来自本次用户提供的输出、本地日志和无凭据网络测试。
