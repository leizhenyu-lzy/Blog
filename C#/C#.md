# C#

## 目录

[toc]

# 【唐老狮】Unity系列之C#四部曲—C#入门

[【唐老狮】Unity系列之C#四部曲—C#入门](https://www.bilibili.com/video/BV1PA411p7A6/)















# 安装 .NET Core SDK

Ubuntu 下使用 snap 应用商店 进行下载

```bash
lzy@legion:~/Project/Blog$ snap install dotnet-sdk --classic
dotnet-sdk 7.0.304 from Microsoft .NET Core (dotnetcore✓) installed
```

查看版本

```bash
lzy@legion:~$ dotnet --version
7.0.304
```

创建工程 "**dotnet new console**"

运行 "**dotnet run**"

```text
lzy@legion:~/Project/Blog/C#/TestInstall$ dotnet new console

Welcome to .NET 7.0!
---------------------
SDK Version: 7.0.304

Telemetry
---------
The .NET tools collect usage data in order to help us improve your experience. It is collected by Microsoft and shared with the community. You can opt-out of telemetry by setting the DOTNET_CLI_TELEMETRY_OPTOUT environment variable to '1' or 'true' using your favorite shell.

Read more about .NET CLI Tools telemetry: https://aka.ms/dotnet-cli-telemetry

----------------
Installed an ASP.NET Core HTTPS development certificate.
To trust the certificate run 'dotnet dev-certs https --trust' (Windows and macOS only).
Learn about HTTPS: https://aka.ms/dotnet-https
----------------
Write your first app: https://aka.ms/dotnet-hello-world
Find out what's new: https://aka.ms/dotnet-whats-new
Explore documentation: https://aka.ms/dotnet-docs
Report issues and find source on GitHub: https://github.com/dotnet/core
Use 'dotnet --help' to see available commands or visit: https://aka.ms/dotnet-cli
--------------------------------------------------------------------------------------
The template "Console App" was created successfully.

Processing post-creation actions...
Restoring /home/lzy/Project/Blog/C#/TestInstall/TestInstall.csproj:
  Determining projects to restore...
  Restored /home/lzy/Project/Blog/C#/TestInstall/TestInstall.csproj (in 114 ms).
Restore succeeded.
```
# vscode 配置 C# 开发环境

Ubuntu也基本适用，可以使用 code runner

[【教程】VSCODE中配置C#的运行环境（Windows）](https://www.bilibili.com/video/BV19Y4y1G78u/)











