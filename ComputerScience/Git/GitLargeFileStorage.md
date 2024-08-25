![](Pics/glfs001.png)

![](Pics/glfs002.gif)

[Git Large File Storage - Official Website](https://git-lfs.com/)

[Managing large files - Github Docs](https://docs.github.com/en/repositories/working-with-files/managing-large-files)

```bash
sudo apt install git-lfs

git lfs install  # 初始化 Git LFS
git lfs track "*.pdf"
git add .gitattributes
git add "*.pdf"


git lfs untrack "*.pdf"

```