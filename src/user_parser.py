"""
All the operations related to user parser
"""
import github_constants
import github_utilities
import user_operations
from github_org import GitOrgManager as OrgMgr


def remove_members_from_org(user_subparser):
    """Remove members from teams"""
    child_parser = user_subparser.add_parser("remove-members-from-org")
    child_parser.add_argument(
        "--members",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated members that needs to be removed from org [--members=IXXXXXX,IXXXXXX]",
    )
    child_parser.set_defaults(func=remove_members_from_org_inner)


def check_rate_limit(user_subparser):
    """Check the rate limit"""
    child_parser = user_subparser.add_parser("check-rate-limit")
    child_parser.set_defaults(func=check_rate_limit_inner)


def convert_outside_collaborators_to_members(user_subparser):
    """Parser to convert outside collaborators to members"""
    child_parser = user_subparser.add_parser(
        "convert-outside-collaborators-to-members")
    child_parser.set_defaults(
        func=convert_outside_collaborators_to_members_inner)


def is_part_of_team(user_subparser):
    """Parser to check is part of team"""
    child_parser = user_subparser.add_parser("is-part-of-team")
    child_parser.add_argument(
        "--ID",
        metavar="<str>",
        required=True,
        type=str,
        help="ID [--ID=IXXXXXX]",
    )
    child_parser.add_argument(
        "--team-names",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated team names that needs to be created [--repo-names=exp-prod-config,ayt-prod-config]",
    )
    child_parser.set_defaults(func=is_part_of_team_inner)


def exists(user_subparser):
    """Parser to check user exists or not"""
    child_parser = user_subparser.add_parser("exists")
    child_parser.add_argument(
        "--ID",
        metavar="<str>",
        required=True,
        type=str,
        help="checks whether the user's exists in the org",
    )
    child_parser.set_defaults(func=exists_inner)


def exists_inner(args):
    """Parser to check user exists or not"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    user_operations.exists(manager, args.ID.strip())


def remove_members_from_org_inner(args):
    """Remove members from org"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    user_operations.remove_members_from_org(
        manager,
        github_utilities.split_strip_list(
            args.members.strip(), github_constants.comma()
        ),
    )


def is_part_of_team_inner(args):
    """Parser to check is part of team"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    user_operations.is_part_of_team(
        manager,
        args.ID.strip(),
        github_utilities.split_strip_list(
            args.team_names.strip(), github_constants.comma()
        ),
    )


def convert_outside_collaborators_to_members_inner(args):
    """Parser to convert outside collaborators to members"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    user_operations.convert_outside_collaborators_to_members(manager)


def check_rate_limit_inner(args):
    """Check rate limit"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    user_operations.check_rate_limit(manager)
