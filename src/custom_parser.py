"""
All the operations related to custom parser
"""
import custom_operations
import github_constants
import github_utilities
from github_org import GitOrgManager as OrgMgr


def add_collaborators_from_repos_to_teams(custom_subparser):
    """Parser to add collaborators from repos to teams"""
    child_parser = custom_subparser.add_parser(
        "add-collaborators-from-repos-to-teams")
    child_parser.add_argument(
        "--repos-suffix",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.add_argument(
        "--access",
        type=str,
        metavar="<str>",
        required=True,
        help="comma separated [--access=write,admin,read] ",
    )
    child_parser.add_argument(
        "--exclude-collaborators",
        type=str,
        metavar="<str>",
        required=True,
        help="comma separated collaborator ID's [--ID=IXXXXXX,IXXXXXX,IXXXXXX]",
    )
    child_parser.set_defaults(func=add_collaborators_from_repos_to_teams_inner)


def create_teams_using_repo_names(team_subparser):
    """Add members to the teams"""
    child_parser = team_subparser.add_parser("create-teams-using-repo-names")
    child_parser.add_argument(
        "--repos-suffix",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.add_argument(
        "--exclude-repos-prefix",
        metavar="<str>",
        required=False,
        type=str,
        default="",
        help="comma separated repos prefix [--repos-prefix=pfs-cockpit], multiple repositories will be processed if matches.",
    )
    child_parser.add_argument(
        "--exclude-repos-suffix",
        metavar="<str>",
        required=False,
        type=str,
        default="",
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.set_defaults(func=create_teams_using_repo_names_inner)


def add_dev_teams_to_dev_config_repos(custom_subparser):
    """Parser to add dev teams to -dev-config repos"""
    child_parser = custom_subparser.add_parser(
        "add-dev-teams-to-dev-config-repos")
    child_parser.add_argument(
        "--access",
        type=str,
        metavar="<str>",
        required=True,
        help="push/pull/admin  [--access=push] ",
    )
    child_parser.set_defaults(func=add_dev_teams_to_dev_config_repos_inner)


def add_dev_teams_to_prod_config_repos(custom_subparser):
    """Parser to add dev teams to -prod-config repos"""
    child_parser = custom_subparser.add_parser(
        "add-dev-teams-to-prod-config-repos")
    child_parser.add_argument(
        "--access",
        type=str,
        metavar="<str>",
        required=True,
        help="push/pull/admin  [--access=push] ",
    )
    child_parser.set_defaults(func=add_dev_teams_to_prod_config_repos_inner)


def add_dev_teams_to_dev_config_repos_inner(args):
    """Parser to add dev teams to -dev-config repos"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    custom_operations.add_dev_teams_to_dev_config_repos(
        manager,
        args.access,
    )


def add_dev_teams_to_prod_config_repos_inner(args):
    """Parser to add dev teams to -prod-config repos"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    custom_operations.add_dev_teams_to_prod_config_repos(
        manager,
        args.access,
    )


def create_teams_using_repo_names_inner(args):
    """Create teams using repo names"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    custom_operations.create_teams_using_repo_names(
        manager,
        github_utilities.split_strip_list(
            args.repos_suffix.strip(), github_constants.comma()
        ),
        github_utilities.split_strip_list(
            args.exclude_repos_suffix.strip(), github_constants.comma()
        ),
        github_utilities.split_strip_list(
            args.exclude_repos_prefix.strip(), github_constants.comma()
        ),
    )


def add_collaborators_from_repos_to_teams_inner(args):
    """Add collaborators from repos to teams"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    custom_operations.add_collaborators_from_repos_to_teams(
        manager,
        github_utilities.split_strip_list(
            args.repos_suffix.strip(), github_constants.comma()
        ),
        github_utilities.split_strip_list(
            args.access.strip(), github_constants.comma()
        ),
        github_utilities.split_strip_list(
            args.exclude_collaborators.strip(), github_constants.comma()
        ),
    )


def list_suspended_org_members(custom_subparser):
    """List the suspended org members"""
    child_parser = custom_subparser.add_parser(
        "list_suspended_org_members")

    child_parser.add_argument(
        "--exclude-collaborators",
        type=str,
        metavar="<str>",
        required=False,
        default="",
        help="comma separated collaborator ID's [--ID=IXXXXXX,IXXXXXX,IXXXXXX]",
    )
    child_parser.set_defaults(func=list_suspended_org_members_inner)

def list_suspended_org_members_inner(args):
    """List the suspended org members"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    custom_operations.list_suspended_org_members(
        manager,
        github_utilities.split_strip_list(
            args.exclude_collaborators.strip(), github_constants.comma()
        ),
    )
