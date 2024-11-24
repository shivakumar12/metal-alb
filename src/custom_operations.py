"""
All the operations related to custom
"""
import team_operations
import repo_operations
from github_org import GitOrgManager
from github import GithubException, GithubObject, Repository


def add_dev_teams_to_dev_config_repos(manager, access):
    """Add dev teams to dev config repos"""
    assert isinstance(manager, GitOrgManager), manager
    dev_config_repos = repo_operations.get_repos_ends_with(
        manager, "-dev-config")

    team_names = []
    for team in manager.organization.get_teams():
        team_names.append(team.name)

    for repo in dev_config_repos:
        if repo.name in team_names:
            team = team_operations.get_team_by_name(manager, repo.name)
            try:
                dev_config_repo = manager.organization.get_repo(
                    repo.name)
                print(f"{dev_config_repo} exists.")
                team.add_to_repos(dev_config_repo)
                team.set_repo_permission(dev_config_repo, access)
                print(
                    f"Added {team} to {dev_config_repo} with {access} access.")
            except GithubException as exception:
                print(f"{repo.name} not exists.")


def add_dev_teams_to_prod_config_repos(manager, access):
    """Add dev teams to prod config repos"""
    assert isinstance(manager, GitOrgManager), manager
    dev_config_repos = repo_operations.get_repos_ends_with(
        manager, "-dev-config")

    team_names = []
    for team in manager.organization.get_teams():
        team_names.append(team.name)

    for repo in dev_config_repos:
        if repo.name in team_names:
            team = team_operations.get_team_by_name(manager, repo.name)
            try:
                dev_config_repo_name = repo.name
                prod_config_repo_name = dev_config_repo_name.removesuffix(
                    "-dev-config") + "-prod-config"
                prod_config_repo = manager.organization.get_repo(
                    prod_config_repo_name)
                print(f"{prod_config_repo} exists.")
                team.add_to_repos(prod_config_repo)
                team.set_repo_permission(prod_config_repo, access)
                print(
                    f"Added {team} to {prod_config_repo} with {access} access.")
            except GithubException as exception:
                print(f"{repo.name} not exists.")


def create_teams_using_repo_names(manager, repos_suffix, exclude_repos_suffix, exclude_repos_prefix):
    """
    Create teams using repo names.
    """
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(repos_suffix, list), repos_suffix

    repos_suffix_list = []
    exclude_repos_suffix_list = []
    exclude_repos_prefix_list = []

    for repo_suffix in repos_suffix:
        repos_suffix_list.extend(repo_operations.get_repos_ends_with_name(
            manager, repo_suffix))

    if len(repos_suffix_list) == 0:
        print(f"No repos ends with {repos_suffix}, bailing out")
        return

    repos_prefix_set = set(repos_suffix_list)

    for exclude_repo_prefix in exclude_repos_prefix:
        if len(exclude_repo_prefix) > 0:
            exclude_repos_prefix_list.extend(repo_operations.get_repos_starts_with_name(
                manager, exclude_repo_prefix))

    print(f"[{len(exclude_repos_prefix_list)}] {exclude_repos_prefix_list} list that needs to be excluded with prefix")

    for exclude_repo_suffix in exclude_repos_suffix:
        if len(exclude_repo_suffix) > 0:
            exclude_repos_suffix_list.extend(repo_operations.get_repos_ends_with_name(
                manager, exclude_repo_suffix))

    print(f"[{len(exclude_repos_suffix_list)}] {exclude_repos_suffix_list} list that needs to be excluded with suffix")

    repos_prefix_set = set(repos_suffix_list)
    exclude_repos_prefix_set = set(exclude_repos_prefix_list)
    exclude_repos_suffix_set = set(exclude_repos_suffix_list)

    teams_to_create = []

    print(f"{len(repos_prefix_set)} list that needs to be converted to teams")
    if len(exclude_repos_prefix_list) == 0 and len(exclude_repos_suffix_list) == 0:
        teams_to_create = repos_suffix_list

    if len(exclude_repos_prefix_list) == 0 and len(exclude_repos_suffix_list) != 0:
        teams_to_create = list(repos_prefix_set - exclude_repos_suffix_set)

    if len(exclude_repos_prefix_list) != 0 and len(exclude_repos_suffix_list) == 0:
        teams_to_create = list(repos_prefix_set - exclude_repos_prefix_set)

    if len(exclude_repos_prefix_list) != 0 and len(exclude_repos_suffix_list) != 0:
        teams_to_create = list(
            repos_prefix_set - exclude_repos_prefix_set - exclude_repos_suffix_set)

    print(f"{len(teams_to_create)} final list that needs to be converted to teams")

    existing_team_names = []
    for team in manager.organization.get_teams():
        existing_team_names.append(team.name)

    for team_name in teams_to_create:
        if team_name in existing_team_names:
            print(f"{team_name} already exists. Skipping creation.")
        else:
            team = manager.organization.create_team(
                team_name, GithubObject.NotSet, GithubObject.NotSet, "closed"
            )
            print(f"{team} created.")


def add_collaborators_from_repos_to_teams(manager, repos_suffix, access, exclude_collaborators):
    """Add collaborators from repos to teams"""
    assert isinstance(manager, GitOrgManager), manager
    repos_list = []
    for repo_suffix in repos_suffix:
        repos_list.extend(repo_operations.get_repos_ends_with(
            manager, repo_suffix))

    teams_dict = {}
    teams = manager.organization.get_teams()
    for team in teams:
        teams_dict[team.name] = team

    for repo in repos_list:
        team = teams_dict[repo.name]
        print("****************************************************************")
        print(f"Processing {repo}")
        if team is None:
            print(f"team doesn't exist with {repo}. Please create team.")
            print("****************************************************************")
            continue
        collaborators_list = repo.get_collaborators()
        for collaborator in collaborators_list:
            if collaborator.name is None:
                continue
            permission = repo.get_collaborator_permission(collaborator.login)
            if permission in (access) and collaborator.login not in (exclude_collaborators):
                print(f"{collaborator.login} - {collaborator.name} - {permission}")
                user = manager.github.get_user(collaborator.login)
                team_operations.add_member_to_team(
                    manager, team, user)
        print("****************************************************************")

def list_suspended_org_members(manager, exclude_collaborators):
    """List the suspended org members"""
    assert isinstance(manager, GitOrgManager), manager

    members = manager.organization.get_members()

    print("****************************************************************")
    print("**** List of the suspended org members *************************")
    print("****************************************************************")
    print("login, name, suspended_at")

    for member in members:
        if member.suspended_at is not None and member.login not in (exclude_collaborators) :
            print(f"{member.login}, '{member.name}', '{member.suspended_at}'")

    print("****************************************************************")
