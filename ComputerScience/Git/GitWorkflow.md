# Git Workflow


# Git 核心区域


<img src="Pics/git03.png" width=450>

**工作区 (Working Directory)**
1. 在本地文件系统中看到的 文件夹 和 文件，进行代码开发的地方
2. 所有未被添加到 Git 版本控制的 文件 或 修改，都会出现在工作区中
3. 命令
   1. `git add` : 将 工作区 的改动 提交到 暂存区
   2. `git reset` (默认 --mixed) : 撤销从 工作区 到 暂存区 的更改，即将文件从暂存区移回工作区
      1. `git reset --soft` : 移动 HEAD 指针，保留 暂存区 & 工作区 的修改，code 在，**commit 从 git log 的历史树上被摘下**(常用于 **合并/压缩 commit**)
      2. `git reset --hard` : 重置 暂存区 和 工作区，**会丢失** 工作区的修改


**暂存区 (Staging Area)**
1. 临时的存储区域，用于保存 即将提交到 本地仓库 的改动 (准备提交的状态)
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

---

# Git 分支

分支类型
1. main/master : 主分支
2. develop : 整合 日常开发
3. feature : 开发 具体 新功能
4. hotfix : 紧急修复 bug

查看分支
1. `git branch` : 仅显示本地分支
2. `--all / -a` : 显示本地和远程所有分支
3. `-r` : 仅显示远程分支

切换分支
1. `git checkout <xxx>`
2. `git switch <xxx>`

创建分支
1. `git branch <xxx>` : 不自动切换
2. `git checkout -b <xxx>` : 创建 + 切换，`-b` 是 branch 缩写

合并分支 步骤
1. 切换到目标分支，eg : main/master
2. `git merge <branch_name>`
3. git 生成 特殊的 合并提交，连接两个分支的历史
4. 解决 **合并冲突** (通常位于 同一文件 同一位置 不同修改)
   1. 手动编辑解决 (保留 当前/合并/both 或者 重新实现)
   2. 验证/测试 解决方案
   3. add 添加到 暂存区 Staging，并 commit 提交解决方案

删除分支 (合并后的分支可以安全删除)
1. 删除本地分支
   1. 安全删除 : `git branch -d <branch_name>`，只有已合并才允许删
   2. 强制删除 : `git branch -D <branch_name>`，不管合没合并，直接删
2. 删除远程分支
   1. `git push origin --delete <branch_name>` : 告诉 origin 删除指定分支


Best Practice
1. 命名规范
   1. feature - 功能名
   2. bugfix  - 问题描述
   3. hotfix  - 紧急修复
2. 定期同步
   1. 经常拉取 主分支 最新更改
   2. 及时合并变更 到工作分支
   3. 避免分支过期，导致集成困难
3. 保持整洁
   1. 及时删除已合并分支
   2. 避免长时间分支特性开发
   3. 小步快跑迭代，频繁 & 短周期


---

# Git 团队协作 工作流

集中式工作流

功能分支流

GitHub Flow

Git Flow





---


# Git 常用命令


`git reset`
1. 作用对象 : 本地仓库 (Local Repository) 的 HEAD 指针
   1. 执行 `git reset <commit>`，Git 首先做的事就是把当前分支的 HEAD 指针(最近的 commit) 强行移动到那个 `<commit>` 上
   2. 修改 本地仓库 的状态
2. `--soft/mixed/hard`
   1. `git reset --mixed` (default) : 撤销从 工作区 到 暂存区 的更改，即将文件从暂存区移回工作区
   2. `git reset --soft` : 仅移动 HEAD 指针，保留 暂存区 & 工作区 的修改，commit (常用于 **合并/压缩 commit**)，code 在，但是 commit 从 git log 的历史树上被摘下
   3. `git reset --hard` : 重置 暂存区 和 工作区，**会丢失** 工作区的修改



# HEAD

HEAD : 最近一次的 commit

单一直线分支
1. `HEAD` : 当前提交
2. `HEAD^` = `HEAD~` = `HEAD~1` : 上一个提交（父提交）
3. `HEAD^^` = `HEAD~~` = `HEAD~2` : 上上个提交（爷爷提交）


合并提交 Merge Commit
1. 当 HEAD 指向一个 合并提交(由 两个分支 合并而来，所以 有两个父节点)
2. `~` (波浪号) 表示 第一父系世系
   1. `HEAD~1` : 第一个 父提交(通常是你合并时所在的主分支，如 `master`)
   2. `HEAD~2` : 第一个 父提交的 父提交
3. `^` (脱字符) 表示 第几个父提交 (Parent number)
   1. `HEAD^1` : 第一个 父提交(等同于 `HEAD~1`)
   2. `HEAD^2` : 第二个 父提交(通常是你合并进来的那个分支，如 feature)


