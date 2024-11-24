"""
All the operations related to repo parser
"""
import github_constants
import github_utilities
import repo_operations
from github_org import GitOrgManager as OrgMgr


def create_pull_request(repo_subparser):
    """Parser to create pull request"""
    child_parser = repo_subparser.add_parser("create-pull-request")
    child_parser.add_argument(
        "--repo-name",
        metavar="<str>",
        required=True,
        type=str,
        help="repository name [--repo-name=pfs-uxr-card-dev-config ]",
    )
    child_parser.add_argument(
        "--head",
        metavar="<str>",
        required=True,
        type=str,
        help="branch name",
    )
    child_parser.add_argument(
        "--base",
        metavar="<str>",
        required=True,
        type=str,
        help="base",
    )
    child_parser.add_argument(
        "--title",
        metavar="<str>",
        required=True,
        type=str,
        help="title message",
    )
    child_parser.set_defaults(func=create_pull_request_inner)


def delete_branch_on_merge(repo_subparser):
    """Parser to add topics to the repos"""
    child_parser = repo_subparser.add_parser("delete-branch-on-merge")
    child_parser.add_argument(
        "--repos-suffix",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.set_defaults(func=delete_branch_on_merge_inner)


def has_access(repo_subparser):
    """Parser to check access to the repos"""
    child_parser = repo_subparser.add_parser("has-access")
    child_parser.add_argument(
        "--ID",
        type=str,
        metavar="<str> ",
        required=True,
        help="collaborator ID [--ID=IXXXXXX]",
    )
    child_parser.add_argument(
        "--names",
        type=str,
        metavar="<str> ",
        required=True,
        help="comma separated names [write,admin,read]",
    )
    child_parser.add_argument(
        "--repo-name",
        metavar="<str>",
        required=True,
        type=str,
        help="repository name [--repo-name=pfs-uxr-card-dev-config].",
    )
    child_parser.set_defaults(func=has_access_inner)


def list_repos_with_topics(repo_subparser):
    """Parser to add topics to the repos"""
    child_parser = repo_subparser.add_parser("list-repos-with-topics")
    child_parser.add_argument(
        "--topics",
        type=str,
        metavar="<str> ",
        required=True,
        help="comma separated collaborator topics [kustomize,helm]",
    )
    child_parser.add_argument(
        "--repos-suffix",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.set_defaults(func=list_repos_with_topics_inner)


def add_topics_to_repos(repo_subparser):
    """Parser to add topics to the repos"""
    child_parser = repo_subparser.add_parser("add-topics-to-repos")
    child_parser.add_argument(
        "--topics",
        type=str,
        metavar="<str> ",
        required=True,
        help="comma separated collaborator topics [kustomize,helm]",
    )
    child_parser.add_argument(
        "--repos-suffix",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.set_defaults(func=add_topics_to_repos_inner)


def tag_exists(repo_subparser):
    """Parser to check tag exists or not"""
    child_parser = repo_subparser.add_parser("tag-exists")
    child_parser.add_argument(
        "--ID",
        type=str,
        metavar="<str> ",
        required=True,
        help="tag ID [--ID=v1.1.0-cf3f705-148]",
    )
    child_parser.add_argument(
        "--repo-name",
        metavar="<str>",
        required=True,
        type=str,
        help="repository name [--repo-name=pfs-uxr-card-dev-config ]",
    )
    child_parser.set_defaults(func=tag_exists_inner)


def is_admin(repo_subparser):
    """Parser to check is admin or not"""
    child_parser = repo_subparser.add_parser("is-admin")
    child_parser.add_argument(
        "--ID",
        type=str,
        metavar="<str> ",
        required=True,
        help="collaborator ID [--ID=IXXXXXX]",
    )
    child_parser.add_argument(
        "--repo-name",
        metavar="<str>",
        required=True,
        type=str,
        help="repository name [--repo-name=pfs-uxr-card-dev-config]",
    )
    child_parser.set_defaults(func=is_admin_inner)


def add_collaborators_to_repos(repo_subparser):
    """Parser to add collaborators to the given repos"""
    child_parser = repo_subparser.add_parser("add-collaborators")
    child_parser.add_argument(
        "--ID",
        type=str,
        metavar="<str> ",
        required=True,
        help="comma separated collaborator ID's [--ID=IXXXXXX,IXXXXXX,IXXXXXX]",
    )
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
        help="push/pull/admin  [--access=push] ",
    )
    child_parser.set_defaults(func=add_collaborators_to_repos_inner)


def remove_collaborators_from_repos(repo_subparser):
    """Parser to remove collaborators from the given repos"""
    child_parser = repo_subparser.add_parser("remove-collaborators")
    child_parser.add_argument(
        "--ID",
        type=str,
        metavar="<str>",
        required=True,
        help="comma separated collaborator ID's [--ID=IXXXXXX,IXXXXXX,IXXXXXX]",
    )
    child_parser.add_argument(
        "--repos-suffix",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.set_defaults(func=remove_collaborators_from_repos_inner)


def add_teams_to_repo(repo_subparser):
    """Parser to add teams to the repos"""
    child_parser = repo_subparser.add_parser("add-teams")
    child_parser.add_argument(
        "--name",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated team name's [--name=exp-digital-assistant-prod-config,ayt-reporting-prod-config]",
    )
    child_parser.add_argument(
        "--repos-suffix",
        metavar="<str>",
        required=False,
        default="",
        type=str,
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.add_argument(
        "--repos-prefix",
        metavar="<str>",
        required=False,
        default="",
        type=str,
        help="comma separated repos suffix [--repos-suffix=pfs-,pfw-,exp-,tal-], multiple repositories will be processed if matches.",
    )
    child_parser.add_argument(
        "--access", type=str, metavar="<str>", required=True, help="pull/push/admin"
    )
    child_parser.set_defaults(func=add_teams_to_repos_inner)


def remove_teams_from_repo(repo_subparser):
    """Parser to remove the teams from the repos"""
    child_parser = repo_subparser.add_parser("remove-teams")
    child_parser.add_argument(
        "--name",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated team name's [--name=exp-digital-assistant-prod-config,ayt-reporting-prod-config]",
    )
    child_parser.add_argument(
        "--repos-suffix",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.set_defaults(func=remove_teams_from_repos_inner)


def list_repos(repo_subparser):
    """Parser to list the repos"""
    child_parser = repo_subparser.add_parser("list")
    child_parser.set_defaults(func=list_repos_inner)


def list_repos_ends_with(repo_subparser):
    """Parser to list the repos that ends with suffix"""
    child_parser = repo_subparser.add_parser("list-repos-ends-with")
    child_parser.add_argument(
        "--repos-suffix",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if matches.",
    )
    child_parser.add_argument(
        "--full-details",
        metavar="<str>",
        required=True,
        type=github_utilities.str2bool,
        default=False,
        help="if true list all the details else only names.",
    )
    child_parser.set_defaults(func=list_repos_ends_with_inner)


def exists(repo_subparser):
    """Parser to check the repo exists for not"""
    child_parser = repo_subparser.add_parser("exists")
    child_parser.add_argument(
        "--repo-names",
        metavar="<str>",
        required=True,
        type=str,
        help="checks whether the repo's exists or not.e.g comma separated repo name's [--repo-names=test-repo-1,test-repo-2,test-repo-3]",
    )
    child_parser.set_defaults(func=exists_inner)


def not_exists(repo_subparser):
    """Parser to check the repo exists for not"""
    child_parser = repo_subparser.add_parser("not-exists")
    child_parser.add_argument(
        "--repo-names",
        metavar="<str>",
        required=True,
        type=str,
        help="checks whether the repo's notexists or not.e.g comma separated repo name's [--repo-names=test-repo-1,test-repo-2,test-repo-3]",
    )
    child_parser.set_defaults(func=not_exists_inner)


def create(repo_subparser):
    """Parser to create the repo"""
    child_parser = repo_subparser.add_parser("create")
    child_parser.add_argument(
        "--repo-names",
        metavar="<str>",
        required=True,
        type=str,
        help="creates the repos",
    )
    child_parser.set_defaults(func=create_inner)


def create_from_template(repo_subparser):
    """Parser to create the repo from template"""
    child_parser = repo_subparser.add_parser("create-from-template")
    child_parser.add_argument(
        "--template-repo-name",
        metavar="<str>",
        required=True,
        type=str,
        help="creates the repos from template [--template-repo-name=ms-template-kustomize-prod-config]",
    )
    child_parser.add_argument(
        "--repo-names",
        metavar="<str>",
        required=True,
        type=str,
        help="comma separated repos that needs to be created [--repo-names=test-repo-1,test-repo-2,test-repo-3]",
    )
    child_parser.set_defaults(func=create_from_template_inner)


def exists_inner(args):
    """Parser to check the repo exists or not"""
    manager = OrgMgr(args.org_name, args.org_token)
    repo_operations.exists(
        manager,
        github_utilities.split_strip_list(
            args.repo_names.strip(), github_constants.comma()
        ),
    )


def not_exists_inner(args):
    """Parser to check the repo exists or not"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.not_exists(
        manager,
        github_utilities.split_strip_list(
            args.repo_names.strip(), github_constants.comma()
        ),
    )


def create_inner(args):
    """Parser to create the repo"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.create(
        manager,
        github_utilities.split_strip_list(
            args.repo_names.strip(), github_constants.comma()
        ),
    )


def create_from_template_inner(args):
    """Parser to create the repo from template"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.create_from_template(
        manager,
        args.template_repo_name.strip(),
        github_utilities.split_strip_list(
            args.repo_names.strip(), github_constants.comma()
        ),
    )


def list_repos_inner(args):
    """Parser to list the repos"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.list_repos(manager)


def list_repos_ends_with_inner(args):
    """Parser to list the repos that ends with"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.list_repos_ends_with(
        manager,
        args.full_details,
        github_utilities.split_strip_list(
            args.repos_suffix.strip(), github_constants.comma()
        ),
    )


def add_collaborators_to_repos_inner(args):
    """Parser to add the collaborators to the repo"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    if args.access == github_constants.push():
        repo_operations.add_collaborators_to_repos(
            manager,
            github_utilities.split_strip_list(
                args.ID.strip(), github_constants.comma()
            ),
            github_utilities.split_strip_list(
                args.repos_suffix.strip(), github_constants.comma()
            ),
            github_constants.push(),
        )
    elif args.access == github_constants.pull():
        repo_operations.add_collaborators_to_repos(
            manager,
            github_utilities.split_strip_list(
                args.ID.strip(), github_constants.comma()
            ),
            github_utilities.split_strip_list(
                args.repos_suffix.strip(), github_constants.comma()
            ),
            github_constants.pull(),
        )
    elif args.access == github_constants.admin():
        repo_operations.add_collaborators_to_repos(
            manager,
            github_utilities.split_strip_list(
                args.ID.strip(), github_constants.comma()
            ),
            github_utilities.split_strip_list(
                args.repos_suffix.strip(), github_constants.comma()
            ),
            github_constants.admin(),
        )
    else:
        raise Exception(
            "Invalid access specified [%s] and should be in one of them [push/pull/admin]"
            % args.access
        )


def remove_collaborators_from_repos_inner(args):
    """Parser to remote the collobarators from the repo"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.remove_collaborators_from_repos(
        manager,
        github_utilities.split_strip_list(
            args.ID.strip(), github_constants.comma()),
        github_utilities.split_strip_list(
            args.repos_suffix.strip(), github_constants.comma()
        ),
    )


def add_teams_to_repos_inner(args):
    """Parser to add the teams to the repos"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    if args.access == github_constants.push():
        repo_operations.add_teams_to_repos(
            manager,
            github_utilities.split_strip_list(
                args.name.strip(), github_constants.comma()
            ),
            github_utilities.split_strip_list(
                args.repos_prefix.strip(), github_constants.comma()
            ),
            github_utilities.split_strip_list(
                args.repos_suffix.strip(), github_constants.comma()
            ),
            github_constants.push(),
        )
    elif args.access == github_constants.pull():
        repo_operations.add_teams_to_repos(
            manager,
            github_utilities.split_strip_list(
                args.name.strip(), github_constants.comma()
            ),
            github_utilities.split_strip_list(
                args.repos_prefix.strip(), github_constants.comma()
            ),
            github_utilities.split_strip_list(
                args.repos_suffix.strip(), github_constants.comma()
            ),
            github_constants.pull(),
        )
    elif args.access == github_constants.admin():
        repo_operations.add_teams_to_repos(
            manager,
            github_utilities.split_strip_list(
                args.name.strip(), github_constants.comma()
            ),
            github_utilities.split_strip_list(
                args.repos_prefix.strip(), github_constants.comma()
            ),
            github_utilities.split_strip_list(
                args.repos_suffix.strip(), github_constants.comma()
            ),
            github_constants.admin(),
        )
    else:
        raise Exception(
            "Invalid access specified[%s] and should in one of them [pull/push/admin]"
            % args.access
        )


def remove_teams_from_repos_inner(args):
    """Parser to remove the teams from the repos"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.remove_teams_from_repos(
        manager,
        github_utilities.split_strip_list(
            args.name.strip(), github_constants.comma()),
        github_utilities.split_strip_list(
            args.repos_suffix.strip(), github_constants.comma()
        ),
    )


def tag_exists_inner(args):
    """Parser to check the tag exists or not for the given repo"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.tag_exists(
        manager,
        args.ID.strip(),
        args.repo_name.strip(),
    )


def is_admin_inner(args):
    """Parser to check admin or not"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.is_admin(
        manager,
        args.ID.strip(),
        args.repo_name.strip(),
    )


def add_topics_to_repos_inner(args):
    """Parser to add topics to the repos"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.add_topics_to_repos(
        manager,
        github_utilities.split_strip_list(
            args.topics.strip(), github_constants.comma()
        ),
        github_utilities.split_strip_list(
            args.repos_suffix.strip(), github_constants.comma()
        ),
    )


def list_repos_with_topics_inner(args):
    """Parser to list the repos having topics"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.list_repos_with_topics(
        manager,
        github_utilities.split_strip_list(
            args.topics.strip(), github_constants.comma()
        ),
        github_utilities.split_strip_list(
            args.repos_suffix.strip(), github_constants.comma()
        ),
    )


def has_access_inner(args):
    """Parser to check the permissions for the repos"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.has_access(
        manager,
        args.ID.strip(),
        github_utilities.split_strip_list(
            args.names.strip(), github_constants.comma()),
        args.repo_name.strip(),
    )


def delete_branch_on_merge_inner(args):
    """Parser to add topics to the repos"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.delete_branch_on_merge(
        manager,
        github_utilities.split_strip_list(
            args.repos_suffix.strip(), github_constants.comma()
        ),
    )


def create_pull_request_inner(args):
    """Parser to create pull request"""
    manager = OrgMgr(args.org_name.strip(), args.org_token.strip())
    repo_operations.create_pull_request(
        manager,
        args.repo_name.strip(),
        args.head.strip(),
        args.base.strip(),
        args.title.strip()
    )
