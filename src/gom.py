"""
The python API to perform git operations
"""
import argparse

import branch_parser
import file_parser
import repo_parser
import team_parser
import user_parser
import custom_parser


def add_custom_parser(subparsers, shared_parent):
    """Parser for custom operations"""
    custom = subparsers.add_parser("custom", parents=[shared_parent])
    custom_subparser = custom.add_subparsers()
    custom_parser.add_dev_teams_to_prod_config_repos(custom_subparser)
    custom_parser.add_dev_teams_to_dev_config_repos(custom_subparser)
    custom_parser.create_teams_using_repo_names(custom_subparser)
    custom_parser.add_collaborators_from_repos_to_teams(custom_subparser)
    custom_parser.list_suspended_org_members(custom_subparser)


def add_repo_parser(subparsers, shared_parent):
    """Parser for repo operations"""
    repo = subparsers.add_parser("repo", parents=[shared_parent])
    repo_subparser = repo.add_subparsers()
    repo_parser.exists(repo_subparser)
    repo_parser.not_exists(repo_subparser)
    repo_parser.create(repo_subparser)
    repo_parser.create_from_template(repo_subparser)
    repo_parser.list_repos(repo_subparser)
    repo_parser.add_collaborators_to_repos(repo_subparser)
    repo_parser.remove_collaborators_from_repos(repo_subparser)
    repo_parser.add_teams_to_repo(repo_subparser)
    repo_parser.remove_teams_from_repo(repo_subparser)
    repo_parser.tag_exists(repo_subparser)
    repo_parser.is_admin(repo_subparser)
    repo_parser.list_repos_ends_with(repo_subparser)
    repo_parser.add_topics_to_repos(repo_subparser)
    repo_parser.list_repos_with_topics(repo_subparser)
    repo_parser.has_access(repo_subparser)
    repo_parser.delete_branch_on_merge(repo_subparser)
    repo_parser.create_pull_request(repo_subparser)


def add_team_parser(subparsers, shared_parent):
    """Parser for team operations"""
    team = subparsers.add_parser("team", parents=[shared_parent])
    team_subparser = team.add_subparsers()
    team_parser.list_teams(team_subparser)
    team_parser.create_teams(team_subparser)
    team_parser.add_members_to_team(team_subparser)
    team_parser.remove_members_from_team(team_subparser)


def add_user_parser(subparsers, shared_parent):
    """Parser for user operations"""
    user = subparsers.add_parser("user", parents=[shared_parent])
    user_subparser = user.add_subparsers()
    user_parser.exists(user_subparser)
    user_parser.is_part_of_team(user_subparser)
    user_parser.convert_outside_collaborators_to_members(user_subparser)
    user_parser.check_rate_limit(user_subparser)
    user_parser.remove_members_from_org(user_subparser)


def add_branch_parser(subparsers, shared_parent):
    """Parser for branch operations"""
    branch = subparsers.add_parser("branch", parents=[shared_parent])
    branch_subparser = branch.add_subparsers()
    branch_parser.protect(branch_subparser)


def add_file_parser(subparsers, shared_parent):
    """Parser for file operations"""
    file = subparsers.add_parser("file", parents=[shared_parent])
    file_subparser = file.add_subparsers()
    file_parser.update_codeowners(file_subparser)
    file_parser.append_file_content(file_subparser)
    file_parser.create_repositories_file(file_subparser)


def get_parser():
    """Parser for with generic arguments"""
    parser = argparse.ArgumentParser(prog="gom.py", allow_abbrev=False)
    shared_parent = argparse.ArgumentParser(add_help=False)
    shared_parent.add_argument(
        "--org-name",
        type=str,
        metavar="<str>",
        required=True,
        help="name of the organization",
    )
    shared_parent.add_argument(
        "--org-token",
        type=str,
        metavar="<str>",
        required=True,
        help="security token of the organization",
    )
    shared_parent.add_argument(
        "--triggered-by",
        type=str,
        metavar="<str>",
        required=True,
        help="collaborator/user-id who is running this framework (IXXXXXX)",
    )
    subparsers = parser.add_subparsers()
    add_team_parser(subparsers, shared_parent)
    add_repo_parser(subparsers, shared_parent)
    add_user_parser(subparsers, shared_parent)
    add_branch_parser(subparsers, shared_parent)
    add_file_parser(subparsers, shared_parent)
    add_custom_parser(subparsers, shared_parent)
    return parser


def main():
    """Handle cli arguments."""
    args = get_parser().parse_args()
    print(f"API Call triggered by [{args.triggered_by}].")
    args.func(args)


if __name__ == "__main__":
    main()
