import subprocess
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
repo.git.checkout('-f', 'master')
repo.git.pull('-r')


# run scripts
subprocess.run(['python', 'scrape_graphics.py'])
subprocess.run(['python', 'scrape_pressreleases.py'])
subprocess.run(['python', 'process_municipalities_singleday.py'])


for filename in repo.git.diff(None, name_only=True).split('\n'):
    if filename == 'data/covid19_bz.csv':
        repo.git.add(filename)
        repo.git.commit('-m', commit_message('basic'))

    elif filename == 'data/covid19_bz_detailed.csv':
        repo.git.add(filename)
        repo.git.commit('-m', commit_message('detailed'))

    elif filename == 'data/covid19_bz_municipalities.csv':
        for untracked_file in repo.untracked_files:
            if 'municipalities_' in untracked_file:
                repo.git.add(untracked_file)
        repo.git.add(filename)
        repo.git.commit('-m', commit_message('municipalities'))


# git push
ssh_cmd = 'ssh -i covid19-bz-scraper-key'
with repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
    repo.remotes.origin.push()