$branch = git branch --show-current
git fetch --all --prune
git status -sb
git merge origin/main
git push -u origin HEAD
git switch main
git pull --ff-only origin main
git merge --ff-only $branch
git push origin main