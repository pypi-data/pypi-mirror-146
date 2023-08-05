import datetime, os, json, unidecode, git
import shutil
from git import Repo, Actor, Commit
from src import settings

def del_files():
    if not os.path.exists(settings.APP_DIR.encode("utf-8")):
        os.makedirs(settings.APP_DIR.encode("utf-8"))
        
    # delete all files and folder to make git tracking easyest
    else:
        for f in os.listdir(settings.APP_DIR):
            if not f.startswith('.'):
                if os.path.isfile("{}/{}".format(settings.APP_DIR, f)):
                    os.remove("{}/{}".format(settings.APP_DIR, f))
                else:
                    shutil.rmtree("{}/{}".format(settings.APP_DIR, f).encode("utf-8"))


def check_git_exists(self):
    if not os.path.exists(self.app_directory + "/.git"):
        # os.makedirs(self.app_directory)
        self.git_repo_obj = Repo.init(self.app_directory)
        self.git_origin = self.git_repo_obj.create_remote(
            "origin", url=self.git_repo
        )
        # self.git_repo_obj\
        #     .create_head('master', self.git_origin.refs.master)\
        #     .set_tracking_branch(self.git_origin.refs.master)\
        #     .checkout()
    else:
        self.git_repo_obj = Repo(self.app_directory)
        self.git_origin = self.git_repo_obj.remote("origin")

    self.git_repo_obj.remotes.origin.push("--all")

def git_set_branch(self, customer_id=None):
    customer_name = "master"
    if customer_id:
        file_id = json.load(open("./src/utils/customer.json"))

        for i in file_id:
            if i["id"] == int(customer_id):
                customer_name = (
                    i["name"].lower().replace(" ", "_").replace("-", "_")
                )
                break
        customer_name = unidecode.unidecode(customer_name)
    try:
        self.git_repo_obj.git.checkout(customer_name)
    except git.exc.GitCommandError:
        self.git_repo_obj.git.checkout("-b", customer_name)
    self.git_branch = customer_name

def commit_tag_push(self):
    repo = self.git_repo_obj
    # add all changes
    repo.git.add(A=True)
    # tree = repo.index.write_tree()

    # create commit with xml file's date

    # Committer and Author
    cr = repo.config_reader()
    committer = Actor.committer(cr)
    author = Actor.author(cr)

    date_creation = datetime.datetime.fromtimestamp(self.creation_date)
    date_creation_git = date_creation.replace(microsecond=0).isoformat()

    # offset = altzone
    # author_time, author_offset = date_creation, offset
    # committer_time, committer_offset = date_creation, offset

    message = "Commit automatique du " + date_creation.strftime("%d/%m/%Y")

    # os.environ["GIT_AUTHOR_DATE"] = str(date_creation)
    # os.environ["GIT_COMMITTER_DATE"] = str(date_creation)

    # Do the commit thing.
    commit = repo.index.commit(
        message,
        author=author,
        committer=committer,
        commit_date=date_creation_git,
        author_date=date_creation_git,
    )

    # Create TAG if version changed
    repo.remotes.origin.push(self.git_branch)
    tags = repo.tags
    if self.version not in tags:
        repo.create_tag(
            self.version, message='Automatic tag "{0}"'.format(self.version)
        )
        repo.remotes.origin.push(self.version)

    # Do the push
    repo.remotes.origin.push(self.git_branch)