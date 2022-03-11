#!/bin/bash

# build html documents
jupyter-book build /Users/ethan/Documents/GitHub/pythonbook/Chapters/ --path-output /Users/ethan/Documents/GitHub/pythonbook/Book --config /Users/ethan/Documents/GitHub/pythonbook/yaml/_config.yml --toc /Users/ethan/Documents/GitHub/pythonbook/yaml/_toc.yml

# push to GitHub

ghp-import -n -p -f Book/_build/html

git add -A
git commit -m "auto-updated with build.sh"
git push origin main