"""
All the operations related to user
"""
import team_operations
from github import GithubException
from github_org import GitOrgManager


def check_rate_limit(manager):
    """List all the repos"""
    assert isinstance(manager, GitOrgManager), manager
    print('  rate_limiting:', manager.github.rate_limiting)
    print('  rate_limiting_resettime:', manager.github.rate_limiting_resettime)
    print('  gh.get_rate_limit():', manager.github.get_rate_limit())


def exists(manager, org_user_id):
    """Check user exists or not"""
    try:
        user = manager.github.get_user(org_user_id)
        print(f"{user} exists.")
    except GithubException as exception:
        error_message = (
            "Not a valid user [{}] and he is not a part of [{}] organization.".format(
                org_user_id, manager.organization_name
            )
        )
        raise Exception(error_message) from exception
    return user


def is_part_of_team(manager, collaborator_id, team_names):
    """Check collaborator_id is part of team"""
    user = exists(manager, collaborator_id)
    found = False
    for team_name in team_names:
        team = team_operations.get_team_by_name(manager, team_name.strip())
        if team.has_in_members(user):
            found = True
            print(f"{user} is part of {team}.")
            break
    if found is False:
        error_message = "[{}] is not a part of {}.".format(
            collaborator_id, team_names)
        raise Exception(error_message)


def convert_outside_collaborators_to_members(manager):
    """Converts outside collaborators to members"""
    outside_collaborators = manager.organization.get_outside_collaborators()
    count = 0
    for user in outside_collaborators:
        if (
            user.login.startswith("I")
            or user.login.startswith("C")
            or user.login.startswith("D")
        ):
            count = count + 1
            user = manager.github.get_user(user.login)
            manager.organization.add_to_members(user, role="member")
            print(f"{user} is added as member from outside collaborator.")
    print(f"[{count}] outside collaborators converted to members.")


def remove_members_from_org(manager, user_names):
    """
    Removes the specified users from the specified org
    :param team: :class:`github.Team`
    :param user_names: list of str
    :type: None
    """
    for user_name in user_names:
        try:
            user = manager.github.get_user(user_name)
            remove_member_from_org(manager, user)
        except GithubException:
            print(f"{user_name}\tuser not found")


def remove_member_from_org(manager, member):
    """
    Remove the specified member, a NamedUser, from the org
    """
    if manager.organization.has_in_members(member):
        manager.organization.remove_from_members(member)
        print(f"{member.login}\tremoved from org")
    else:
        print(f"{member.login}\t is not a member of org")
