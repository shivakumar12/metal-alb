"""
All the operations related to branch parser
"""
import branch_operations
import github_constants
import github_utilities
from github_org import GitOrgManager as OrgMgr


def protect(branch_subparser):
    """Protect the branch"""
    child_parser = branch_subparser.add_parser("protect")
    child_parser.add_argument(
        "--branch-names",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated branch names that needs protection [--branch-names=master,bugfix]",
    )
    child_parser.add_argument(
        "--repos-suffix",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.set_defaults(func=protect_inner)


def protect_inner(args):
    """Protect the branch"""
    manager = OrgMgr(args.org_name, args.org_token)
    branch_operations.protect(
        manager,
        github_utilities.split_strip_list(
            args.branch_names.strip(), github_constants.comma()
        ),
        github_utilities.split_strip_list(
            args.repos_suffix.strip(), github_constants.comma()
        ),
    )
