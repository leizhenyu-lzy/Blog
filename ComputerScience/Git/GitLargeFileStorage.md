<img src="Pics/glfs001.png" width=400>

# Git Large File Storage

<img src="Pics/glfs002.gif" width=500>

---

[Git Large File Storage - Official Website](https://git-lfs.com/)

[Managing large files - Github Docs](https://docs.github.com/en/repositories/working-with-files/managing-large-files)

[管理大型文件(简体中文) - Github Docs](https://docs.github.com/zh/repositories/working-with-files/managing-large-files)

---

# Get Started

```bash
sudo apt install git-lfs

git lfs install  # set up Git LFS for user account

git lfs track "*.pdf"  # select the file types Git LFS to manage (or directly edit your .gitattributes)
git add .gitattributes  # make sure .gitattributes is tracked
git add/commit/push # 像往常一样使用 git add、git commit 和 git push 进行提交和推送


git lfs untrack "*.pdf"
```

仅仅通过 `git lfs track` 命令来定义 Git LFS 应该跟踪的文件类型，并不会自动将你仓库中已经存在的大文件(比如在其他分支上或旧的提交历史中的文件) 转换为 Git LFS 管理，需要使用 `git lfs migrate` 命令


工作原理
1. 用指针文件代替大文件
   1. Git LFS 不会将大文件的实际内容直接存储在 Git 仓库中
   2. 用一个很小的 **指针文件**(pointer file) 来代替这些大文件，指针文件是一个文本文件，里面包含了大文件的唯一标识符(例如 SHA-256 哈希值) & 大小
2. 文件存储在 LFS 服务器
   1. 当 提交 & 推送 包含 Git LFS 跟踪的文件的更改时，实际的大文件内容会被上传到一个独立的 Git LFS 服务器，而不是常规的 Git 远程仓库
3. Git 仓库只存储指针
   1. Git 仓库(包括远程仓库) 只会存储这些轻量级的指针文件，而不是庞大的二进制文件
   2. 使得克隆和拉取操作变得非常快，因为您只下载了包含代码和指针文件的轻量级仓库
4. 按需下载
   1. 当检出一个包含 Git LFS 文件的分支时，Git LFS 会自动根据指针文件中的信息，从 LFS 服务器下载对应的实际大文件到您的本地工作目录
   2. 对于用户来说，过程是透明的，在本地看到和使用的仍然是完整的大文件



Git LFS **减小下载量**，解决 **仓库体积膨胀** 问题
1. `git clone` 或 `git pull` 时，Git 只会下载包含代码和轻量级指针文件的仓库，这部分数据量非常小
2. Git LFS 客户端会等到 `checkout` 某个 branch 或 commit 时，才去 LFS 服务器下载 该提交所需要的具体大文件版本
3. 传统 Git 每次操作都下载所有历史版本的所有大文件 ； Git LFS 只有在需要时 才下载当前正在使用的大文件版本
4. 只关注最新代码，不关心历史大文件版本
5. Git LFS 实际上 还是会在其服务器上存储大文件的多个版本，修改并提交一个被 LFS 跟踪的文件时，Git LFS 都会将这个新版本的文件内容作为独立的 对象 上传到 LFS 服务器
   1. 如果一个 100MB 的文件被修改了 10 次，Git LFS 服务器上会存储 10 个 100MB 的文件对象
   2. 从 LFS 服务器的角度看，会因为文件的修改而 膨胀，就像传统的 Git 仓库一样
6. Git LFS 的关键作用 是 **隔离膨胀**(没有减少 总体的 数据存储量)，让其不影响 Git 的核心功能，让 Git 核心保持轻量 (Git 负责管理代码和文件的版本历史，但只通过指针来引用大文件)






