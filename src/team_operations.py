"""
All the operations related to team
"""
from github import GithubException, GithubObject
from github_org import GitOrgManager
import repo_operations


def list_teams(manager):
    """
    List teams in the organization.
    """
    teams = manager.organization.get_teams()
    print("team,id,members_count,repos_count")

    for team in teams:
        print(f"{team.name},{team.id},{team.members_count},{team.repos_count}")


def create_teams(manager, team_names):
    """
    Create teams in the organization.
    """
    for team_name in team_names:
        team = None
        try:
            team = get_team_by_name(manager, team_name)
            print(f"Ignoring {team} already exists")
        except Exception:
            print(f"{team_name} not found and will be created.")
            manager.organization.create_team(
                team_name, GithubObject.NotSet, GithubObject.NotSet, "closed"
            )


def remove_members_from_team(manager, team_name, user_names):
    """
    Removes the specified users to the specified team
    :param team: :class:`github.Team`
    :param user_names: list of str
    :type: None
    """
    for user_name in user_names:
        try:
            user = manager.github.get_user(user_name)
            team = get_team_by_name(manager, team_name)
            remove_member_from_team(manager, team, user)
        except GithubException:
            print(f"{user_name}\tuser not found")


def add_members_to_team(manager, team_name, user_names):
    """
    Add the specified users to the specified team
    :param team: :class:`github.Team`
    :param user_names: list of str
    :type: None
    """
    for user_name in user_names:
        try:
            user = manager.github.get_user(user_name)
            team = get_team_by_name(manager, team_name)
            add_member_to_team(manager, team, user)
        except GithubException:
            print(f"{user_name}\tuser not found")


def add_member_to_team(manager, team, member):
    """
    Adds the specified member, a NamedUser, to the team
    """
    if team.has_in_members(member):
        print(f"{member.login}\talready had access")
    elif not manager.organization.has_in_members(member):
        manager.organization.add_to_members(member, "member")
        print(f"{member.login}\tinvited")
    else:
        print(f"{member.login}\tgiven access")
        team.add_to_members(member)


def remove_member_from_team(manager, team, member):
    """
    Removes the specified member, a NamedUser, to the team
    """
    if team.has_in_members(member):
        print(f"{member.login}/{team}\twill be removed.")
        team.remove_from_members(member)
        print(f"{member.login}/{team}\tremoved.")


def get_teams_starting_with(manager, prefix):
    """
    Get the teams that starting with some prefixs
    """
    teams = []
    for team in manager.organization.get_teams():
        if team.name.startswith(prefix):
            teams.append(team)
    return teams


def get_team_by_name_supress(manager, team_name):
    """
    Get the team by the team name
    """
    for team in manager.organization.get_teams():
        if team.name == team_name:
            return team


def get_team_by_name(manager, team_name):
    """
    Get the team by the team name
    """
    for team in manager.organization.get_teams():
        if team.name == team_name:
            return team
    raise Exception("Team {%s} not found" % team_name)
