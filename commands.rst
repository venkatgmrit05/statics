# setup a dev environment
python -m pip install -e .

#to merge with master
$ git checkout master
$ git pull
$ git merge my-feature-branch
$ git log