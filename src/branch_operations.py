"""
All the operations related to branch
"""
import repo_operations
from github import GithubException
from github_org import GitOrgManager


def protect(manager, branch_names, repos_suffix):
    """Protect the branch"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(branch_names, list), branch_names
    assert isinstance(repos_suffix, list), repos_suffix
    branch_protection_config = manager.config["branch_protection_config"]
    repos_to_protect = []
    for repo_suffix in repos_suffix:
        repos_to_protect = repo_operations.get_repos_ends_with(
            manager, repo_suffix)
        for repo in repos_to_protect:
            if not repo.archived:
                for branch_name in branch_names:
                    try:
                        repo.get_branch(branch_name).edit_protection(
                            **branch_protection_config
                        )
                    except GithubException as exception:
                        if exception.status != 404:
                            raise
