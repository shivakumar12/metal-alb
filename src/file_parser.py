"""
All the operations related to file parser
"""
import file_operations
from github_org import GitOrgManager as OrgMgr


def update_codeowners(file_subparser):
    """Update the codeowners"""
    child_parser = file_subparser.add_parser("update-codeowners")
    child_parser.add_argument(
        "--repo-name",
        metavar="<str>",
        required=True,
        type=str,
        help="repo name to update the CODEOWNERS [--repo-name=test-repo-1]",
    )
    child_parser.add_argument(
        "--branch-name",
        metavar="<str>",
        default="master",
        type=str,
        help="branch where the file CODEOWNERS file exists",
    )
    child_parser.add_argument(
        "--content",
        metavar="<str>",
        required=True,
        type=str,
        help="content that will be updated in CODEOWNERS file",
    )
    child_parser.set_defaults(func=update_codeowners_inner)


def update_codeowners_inner(args):
    """Update the codeowners"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    file_operations.update_codeowners(
        manager,
        args.repo_name.strip(),
        args.branch_name.strip(),
        args.content.split("$"),
    )


def append_file_content(file_subparser):
    """Append the file content"""
    child_parser = file_subparser.add_parser("append-file-content")
    child_parser.add_argument(
        "--repo-name",
        metavar="<str>",
        required=True,
        type=str,
        help="repo name to append the content to the file [--repo-name=test-repo-1]",
    )
    child_parser.add_argument(
        "--branch-name",
        metavar="<str>",
        default="master",
        type=str,
        help="branch where the file exists",
    )
    child_parser.add_argument(
        "--file-path",
        metavar="<str>",
        required=True,
        type=str,
        help="location of the file in the repository",
    )
    child_parser.add_argument(
        "--content",
        metavar="<str>",
        required=True,
        type=str,
        help="content that will be appended in the file",
    )
    child_parser.add_argument(
        "--commit-message",
        metavar="<str>",
        required=True,
        type=str,
        help="commit message",
    )
    child_parser.set_defaults(func=append_file_content_inner)


def append_file_content_inner(args):
    """Append the file content"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    file_operations.append_file_content(
        manager,
        args.repo_name.strip(),
        args.branch_name.strip(),
        args.file_path.strip(),
        args.content.split("$"),
        args.commit_message.strip(),
    )


def create_repositories_file(file_subparser):
    """Create repositories file"""
    child_parser = file_subparser.add_parser("create-repositories-file")
    child_parser.add_argument(
        "--repo-name",
        metavar="<str>",
        required=True,
        type=str,
        help="repo name to append the content to the file [--repo-name=test-repo-1]",
    )
    child_parser.add_argument(
        "--branch-name",
        metavar="<str>",
        default="master",
        type=str,
        help="branch where the file exists",
    )
    child_parser.add_argument(
        "--file-path",
        metavar="<str>",
        required=True,
        type=str,
        help="location of the file in the repository",
    )
    child_parser.add_argument(
        "--repos-suffix",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.add_argument(
        "--commit-message",
        metavar="<str>",
        required=True,
        type=str,
        help="commit message",
    )
    child_parser.set_defaults(func=create_repositories_file_inner)


def create_repositories_file_inner(args):
    """Creation of repositories file"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    file_operations.create_repositories_file(
        manager,
        args.repo_name.strip(),
        args.branch_name.strip(),
        args.file_path.strip(),
        args.repos_suffix.strip(),
        args.commit_message.strip(),
    )
