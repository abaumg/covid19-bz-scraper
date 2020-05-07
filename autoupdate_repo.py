from datetime import datetime
from git import Repo

def commit_message(type_of_data):
    message = 'added {type} data for {date}'.format(
        date=datetime.today().strftime('%Y-%m-%d'),
        type=type_of_data
    )
    return message

repo = Repo()

# pull remote repo
repo.git.pull('-r')


for filename in repo.git.diff(None, name_only=True).split('\n'):
    if filename == 'data/covid19_bz.csv':
        repo.git.add(filename)
        repo.git.commit('-m', commit_message('basic'))

    elif filename == 'data/covid19_bz_detailed.csv':
        repo.git.add(filename)
        repo.git.commit('-m', commit_message('detailed'))

    elif filename == 'data/covid19_municipalities.csv':
        for untracked_file in repo.untracked_files:
            if 'municipalities_' in filename:
                repo.git.add(untracked_file)
        repo.git.add(filename)
        repo.git.commit('-m', commit_message('municipalities'))


# git push
ssh_cmd = 'ssh -i covid19-bz-scraper-key'
with repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
    repo.remotes.origin.push()