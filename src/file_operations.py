"""
All the operations related to file
"""
from github import GithubException
from datetime import datetime


def update_codeowners(manager, repo_name, branch_name, content):
    """Update the codeowners with the content"""
    try:
        repo = manager.organization.get_repo(repo_name)
        print(f"{repo} exists.")
    except GithubException as exception:
        raise Exception("Repository [%s] not exists" %
                        repo_name) from exception

    # Remove the whitespaces
    content = [x.strip(" ") for x in content]

    file_to_be_updated = "CODEOWNERS"
    sha = repo.get_contents(file_to_be_updated, ref=branch_name).sha
    repo.update_file(
        path=file_to_be_updated,
        message="Initial Commit",
        content="\n".join(content),
        sha=sha,
        branch=branch_name,
    )
    print(f"CODEOWNERS updated {repo} branch {branch_name}.")


def append_file_content(
    manager, repo_name, branch_name, file_path, content, commit_message
):
    """Append the file content"""
    try:
        repo = manager.organization.get_repo(repo_name)
        print(f"{repo} exists.")
    except GithubException as exception:
        raise Exception("Repository [%s] not exists" %
                        repo_name) from exception

    # Remove the whitespaces
    content = [x.strip(" ") for x in content]
    content = "".join(content)
    new_content = []
    new_content.append(content)
    existing_contents = repo.get_contents(file_path, ref=branch_name)
    for line in existing_contents.decoded_content.decode("utf8").split("\n"):
        new_content.append(line)

    sha = repo.get_contents(file_path, ref=branch_name).sha
    repo.update_file(
        path=file_path,
        message=commit_message,
        content="\n".join(new_content),
        sha=sha,
        branch=branch_name,
    )
    print(f"file updated {repo} branch {branch_name}.")


def create_repositories_file(
    manager, repo_name, branch_name, file_path, repos_suffix, commit_message
):
    """Create the repositories file"""
    new_content = []
    for repo in manager.organization.get_repos():
        if repo.name.endswith(repos_suffix):
            original_repo_name = repo.name.replace(repos_suffix, "")
            tags = repo.get_topics()
            if (len(tags) == 0):
                print(
                    f"{repo} doesn't have either of the topic [kustomize] or [helm].")
                continue

            for tag in tags:
                if (tag == "kustomize"):
                    original_repo_name = original_repo_name+","+"kustomize"
                    new_content.append(original_repo_name)
                    print(
                        f"{repo} has the topic [kustomize].")
                    break
                elif (tag == "helm"):
                    original_repo_name = original_repo_name+","+"helm"
                    new_content.append(original_repo_name)
                    print(
                        f"{repo} has the topic [helm].")
                    break
                else:
                    print(
                        f"{repo} doesn't have either of the topic [kustomize] or [helm].")

    repo = manager.organization.get_repo(repo_name)
    sha = repo.get_contents(file_path, ref=branch_name).sha
    repo.update_file(
        path=file_path,
        message=commit_message,
        content="\n".join(new_content),
        sha=sha,
        branch=branch_name,
    )
    release_titles = []
    for release in repo.get_releases():
        release_titles.append(release.title)

    release_version = 1
    release_title = ""
    while True:
        release_title = "{0}.{1}.{2}.{3}".format(
            datetime.now().year,
            datetime.now().month,
            datetime.now().day,
            release_version
        )
        if release_title in release_titles:
            release_version += 1
        else:
            break
    print(f" Creating release {release_title}.")
    release = repo.create_git_tag_and_release(
        release_title,
        "Updated Repository Inventory",
        release_title,
        "Updated Repository Inventory",
        repo.get_commits()[0].sha,
        "commit"
    )
