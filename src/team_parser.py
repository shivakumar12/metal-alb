"""
All the operations related to team parser
"""
import github_constants
import github_utilities
import team_operations
from github_org import GitOrgManager as OrgMgr


def list_teams(team_subparser):
    """List the teams"""
    child_parser = team_subparser.add_parser("list")
    child_parser.set_defaults(func=list_teams_inner)


def create_teams(team_subparser):
    """Create the teams"""
    child_parser = team_subparser.add_parser("create-teams")
    child_parser.add_argument(
        "--team-names",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated team names that needs to be created [--repo-names=exp-prod-config,ayt-prod-config]",
    )
    child_parser.set_defaults(func=create_teams_inner)


def add_members_to_team(team_subparser):
    """Add members to the teams"""
    child_parser = team_subparser.add_parser("add-members-to-team")
    child_parser.add_argument(
        "--team-name",
        metavar="<str>",
        required=True,
        type=str,
        help="team name in which the members will be added [--team-name=exp-prod-config]",
    )
    child_parser.add_argument(
        "--members",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated members that needs to be added to team [--members=IXXXXXX,IXXXXXX]",
    )
    child_parser.set_defaults(func=add_members_to_team_inner)


def remove_members_from_team(team_subparser):
    """Remove members from teams"""
    child_parser = team_subparser.add_parser("remove-members-from-team")
    child_parser.add_argument(
        "--team-name",
        metavar="<str>",
        required=True,
        type=str,
        help="team name in which the members to be removed [--team-name=exp-prod-config]",
    )
    child_parser.add_argument(
        "--members",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated members that needs to be removed from team [--members=IXXXXXX,IXXXXXX]",
    )
    child_parser.set_defaults(func=remove_members_from_team_inner)


def list_teams_inner(args):
    """List the teams"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    team_operations.list_teams(manager)


def create_teams_inner(args):
    """Create the teams"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    team_operations.create_teams(
        manager,
        github_utilities.split_strip_list(
            args.team_names.strip(), github_constants.comma()
        ),
    )


def add_members_to_team_inner(args):
    """Add the members to the teams"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    team_operations.add_members_to_team(
        manager,
        args.team_name.strip(),
        github_utilities.split_strip_list(
            args.members.strip(), github_constants.comma()
        ),
    )


def remove_members_from_team_inner(args):
    """Remove members from teams"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    team_operations.remove_members_from_team(
        manager,
        args.team_name.strip(),
        github_utilities.split_strip_list(
            args.members.strip(), github_constants.comma()
        ),
    )
