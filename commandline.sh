echo -e '# Blog\n\n---\n' > README.md

echo -e 'Record What I Learned\n' >> README.md

echo -e '![](GithubCat.gif)\n\n---\n' >> README.md

echo -e '**Table of Content**' >> README.md

echo -e '```text' >> README.md

tree -d -L 2 >> README.md

echo -e '```\n' >> README.md



