# Git Workflow


# Git 核心区域


<img src="Pics/git03.png" width=450>

**工作区 (Working Directory)**
1. 在本地文件系统中看到的 文件夹 和 文件，也是你进行代码开发的地方
2. 所有未被添加到 Git 版本控制的 文件 或 修改，都会出现在工作区中
3. 命令
   1. `git add` : 将 工作区 的改动 提交到 暂存区
   2. `git reset` (默认 --mixed) : 撤销从 工作区 到 暂存区 的更改，即将文件从暂存区移回工作区
      1. `git reset --soft` : 仅移动 HEAD 指针，保留 暂存区 & 工作区 的修改，commit  (常用于 **合并/压缩 commit**)，code 在，但是 commit 从 git log 的历史树上被摘下
      2. `git reset --hard` : 重置 暂存区 和 工作区，**会丢失** 工作区的修改


**暂存区 (Staging Area)**
1. 临时的存储区域，用于保存 即将提交到本地仓库的改动 (准备提交的状态)
2. 命令
   1. `git commit` : 将 暂存区 的所有改动 提交 本地仓库，生成一次新的提交(commit)

**储藏区 (Stash)**
1. 储藏区是一个临时存储空间，用于保存未完成的工作
2. 命令
   1. `git stash` : 保存当前未 commit 的工作
   2. `git stash pop` : 恢复最新的进度，并 **删除** 暂存记录
   3. `git stash apply` : 恢复最新的进度，**保留** 暂存记录 (适用于需要多次应用同一处修改)

**本地仓库 (Local Repository)**
1. 本地仓库保存的是 **整个项目** 的 **所有分支的历史提交记录**(commits)
2. 命令
   1. `git push` : 将 本地仓库的改动 上传 远程仓库
   2. `git reset` : 撤销本地仓库的提交 (HEAD 指针移动)，并将改动返回到工作区或暂存区 (取决于 --soft/mixed/hard)

**远程仓库 (Remote Repository)**
1. 存储在 服务器 的代码库，用于 团队协作
2. 命令
   1. `git remote add <name> <url>` : 将一个远程仓库添加到本地，并起一个别名 `<name>` (通常叫 `origin`)，让本地知道往哪里推送
   2. `git fetch` : 从远程仓库下载最新改动，**更新远程跟踪分支** (`origin/master`)，但 **不合并** 到本地工作分支
   3. `git pull` : = `git fetch` + `git merge`
      1. 先执行 `fetch` 更新 远程跟踪分支
      2. 再将 远程跟踪分支 的内容 `merge` 到 当前本地分支

**远程跟踪分支 (Remote Branch Tracking)**
1. 远程跟踪分支 是 本地 对 远程分支 的 引用， 追踪远程分支 最新状态



# Git 常用命令


`git reset`
1. 作用对象 : 本地仓库 (Local Repository) 的 HEAD 指针
   1. 执行 `git reset <commit>`，Git 首先做的事就是把当前分支的 HEAD 指针强行移动到那个 `<commit>` 上
   2. 修改 本地仓库 的状态
2. `--soft/mixed/hard`
   1. `git reset --mixed` (default) : 撤销从 工作区 到 暂存区 的更改，即将文件从暂存区移回工作区
   2. `git reset --soft` : 仅移动 HEAD 指针，保留 暂存区 & 工作区 的修改，commit (常用于 **合并/压缩 commit**)，code 在，但是 commit 从 git log 的历史树上被摘下
   3. `git reset --hard` : 重置 暂存区 和 工作区，**会丢失** 工作区的修改

