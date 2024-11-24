"""
All the operations related to team
"""
from os import name
import team_operations
from github import GithubException, GithubObject, Repository
from github_org import GitOrgManager


def exists(manager, repo_names):
    """Check repo exists or not"""
    for repo_name in repo_names:
        assert isinstance(repo_name, str), repo_name
        assert isinstance(manager, GitOrgManager), manager
        try:
            repo = manager.organization.get_repo(repo_name)
            print(f"{repo} exists.")
        except GithubException as exception:
            raise Exception("Repository [%s] not exists" %
                            repo_name) from exception
    return repo


def not_exists(manager, repo_names):
    """Check repo exists or not"""
    for repo_name in repo_names:
        assert isinstance(repo_name, str), repo_name
        assert isinstance(manager, GitOrgManager), manager
        repo = None
        try:
            repo = manager.organization.get_repo(repo_name)
        except GithubException:
            print(f"{repo_name} not exists.")

        if repo is not None:
            raise Exception("repo [%s] already exists." % repo_name)
    return repo


def create(manager, repo_names):
    """Create a repo"""
    repo_config = manager.config["repo_config"]
    assert isinstance(manager, GitOrgManager), manager
    for repo_name in repo_names:
        assert isinstance(repo_name, str), repo_name
        try:
            repo = manager.organization.create_repo(repo_name, **repo_config)
            print(f"{repo} created.")
        except GithubException as exception:
            raise Exception("Repository [%s] not created" %
                            repo_name) from exception


def list_repos(manager):
    """List all the repos"""
    assert isinstance(manager, GitOrgManager), manager
    repos = manager.organization.get_repos()
    print("name,size,updated_at,pushed_at")
    for repo in repos:
        print(f"{repo.name},{repo.size},{repo.updated_at},{repo.pushed_at}")


def list_repos_ends_with(manager, full_details, repos_suffix):
    """Get the repos that ends with suffix"""
    assert isinstance(manager, GitOrgManager), manager
    repos_to_list = []
    for repo_suffix in repos_suffix:
        repos_to_list.extend(get_repos_ends_with(manager, repo_suffix))
    print(full_details)
    if full_details is True:
        for repo in repos_to_list:
            print(f"{repo},{repo.size},{repo.updated_at},{repo.pushed_at}")
    else:
        for repo in repos_to_list:
            print(f"{repo.name}")


def get_repos_ends_with(manager, suffix):
    """Get the repos that ends with suffix"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(suffix, str), suffix
    repos = []
    all_repos = manager.organization.get_repos()
    for repo in all_repos:
        if repo.name.endswith(suffix):
            repos.append(repo)
    return repos


def get_repos_starts_ends_with_name(manager, prefix, suffix):
    """Get the repos that ends with suffix / starts with prefix"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(suffix, str), suffix
    repos = []
    all_repos = manager.organization.get_repos()
    for repo in all_repos:
        if (repo.name.endswith(suffix) and repo.name.startswith(prefix)):
            repos.append(repo)
    return repos


def get_repos_ends_with_name(manager, suffix):
    """Get the repos that ends with suffix"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(suffix, str), suffix
    repos = []
    all_repos = manager.organization.get_repos()
    for repo in all_repos:
        if repo.name.endswith(suffix):
            repos.append(repo.name)
    return repos


def get_repos_starts_with_name(manager, prefix):
    """Get the repos that starts with prefix"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(prefix, str), prefix
    repos = []
    all_repos = manager.organization.get_repos()
    for repo in all_repos:
        if repo.name.startswith(prefix):
            repos.append(repo.name)
    return repos


def add_collaborators_to_repos(manager, collaborator_ids, repos_suffix, access):
    """Add Collaborators to the repos"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(repos_suffix, list), repos_suffix
    assert isinstance(access, str), access

    repos_to_add = []
    for repo_suffix in repos_suffix:
        repos_to_add.extend(get_repos_ends_with(manager, repo_suffix))

    print(repos_to_add)
    print(collaborator_ids)
    if len(repos_to_add) == 0:
        print(f"No repos ends with {repos_suffix}, bailing out")
        return
    for repo in repos_to_add:
        for collaborator_id in collaborator_ids:
            assert isinstance(collaborator_id, str), collaborator_id
            print(f"Adding {collaborator_id} to {repo} with {access} access.")
            repo.add_to_collaborators(collaborator_id, access)
            print("successfully added.")


def remove_collaborators_from_repos(manager, collaborator_ids, repos_suffix):
    """Remove Collaborators to the repos"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(repos_suffix, list), repos_suffix

    repos_to_remove = []
    for repo_suffix in repos_suffix:
        repos_to_remove.extend(get_repos_ends_with(manager, repo_suffix))

    print(repos_to_remove)
    print(collaborator_ids)
    if len(repos_to_remove) == 0:
        print(f"No repos ends with {repos_suffix}, bailing out")
        return
    for repo in repos_to_remove:
        for collaborator_id in collaborator_ids:
            assert isinstance(collaborator_id, str), collaborator_id
            print(f"Removing  {collaborator_id} from  {repo}.")
            repo.remove_from_collaborators(collaborator_id)
            print("successfully removed.")


def add_teams_to_repos(manager, team_names, repos_prefix, repos_suffix, access):
    """Add teams to the repos"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(access, str), access
    assert isinstance(repos_suffix, list), repos_suffix
    assert isinstance(repos_prefix, list), repos_prefix

    repos_to_add = []
    if (len(repos_suffix) != 0 and len(repos_prefix) != 0):
        for repo_prefix in repos_prefix:
            for repo_suffix in repos_suffix:
                repos_to_add.extend(get_repos_starts_ends_with_name(
                    manager, repo_prefix, repo_suffix))
        if len(repos_to_add) == 0:
            print(
                f"No repos ends with {repos_prefix}/{repos_suffix}, bailing out")
    elif(len(repos_suffix)):
        for repo_suffix in repos_suffix:
            repos_to_add.extend(get_repos_ends_with_name(
                manager, repo_suffix))
        if len(repos_to_add) == 0:
            print(f"No repos ends with {repos_suffix}, bailing out")
    elif(len(repos_prefix)):
        for repo_prefix in repos_prefix:
            repos_to_add.extend(get_repos_starts_with_name(
                manager, repo_prefix))
        if len(repos_to_add) == 0:
            print(f"No repos ends with {repos_prefix}, bailing out")

    print(repos_to_add)
    print(team_names)

    for repo in repos_to_add:
        for team_name in team_names:
            assert isinstance(team_name, str), team_name
            team = team_operations.get_team_by_name(manager, team_name)
            print(f"Adding {team_name} to {repo} with {access} access.")
            team.add_to_repos(repo)
            status = team.update_team_repository(repo, access)
            print(f"status : {status}")
            if status:
                print(
                    f"successfully added {team_name} to {repo} with {access} access.")
            else:
                raise Exception(
                    "Error while adding [%s} to [%s] with [%s] access"
                    % team_name % repo % access
                )


def remove_teams_from_repos(manager, team_names, repos_suffix):
    """Remove teams from  the repos"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(repos_suffix, list), repos_suffix

    repos_to_remove = []
    for repo_suffix in repos_suffix:
        repos_to_remove.extend(get_repos_ends_with(manager, repo_suffix))

    print(repos_to_remove)
    print(team_names)
    if len(repos_to_remove) == 0:
        print(f"No repos ends with {repos_suffix}, bailing out")
        return
    for repo in repos_to_remove:
        for team_name in team_names:
            assert isinstance(team_name, str), team_name
            team = team_operations.get_team_by_name(manager, team_name)
            print(f"Removing {team} from {repo}")
            team.remove_from_repos(repo)
            print("successfully removed.")


def create_from_template(manager, template_repo_name, repo_names):
    """Create repo from template"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(template_repo_name, str), template_repo_name
    template_repo = exists(manager, template_repo_name.split(" "))
    for repo_name in repo_names:
        assert isinstance(repo_name, str), repo_name
        repo = None
        try:
            repo = exists(manager, repo_name.split(" "))
        except Exception:
            print(f"Repository {repo_name} not exists and will be created.")

        if repo is not None:
            raise Exception(
                "repo [%s]  already exists and cannot be created." % repo_name
            )

        private = True
        description = "Repo created from template %s " % template_repo_name
        create_from_template_inner(
            manager, repo_name, template_repo, description, private
        )


def create_from_template_inner(
    manager,
    repo_name,
    template_repo,
    description=GithubObject.NotSet,
    private=GithubObject.NotSet,
):
    """Create repo from template"""
    media_type_templates_preview = "application/vnd.github.baptiste-preview json"
    assert isinstance(repo_name, str), repo_name
    assert isinstance(template_repo, Repository.Repository), template_repo
    assert description is GithubObject.NotSet or isinstance(
        description, str
    ), description
    assert private is GithubObject.NotSet or isinstance(private, bool), private
    post_parameters = {
        "name": repo_name,
        "owner": manager.organization_name,
    }
    if description is not GithubObject.NotSet:
        post_parameters["description"] = description
    if private is not GithubObject.NotSet:
        post_parameters["private"] = private
        headers, data = manager.organization._requester.requestJsonAndCheck(
            "POST",
            "/repos/"
            + template_repo.owner.login
            + "/"
            + template_repo.name
            + "/generate",
            input=post_parameters,
            headers={"Accept": media_type_templates_preview},
        )
        new_repo = Repository.Repository(
            manager.organization._requester, headers, data, completed=True
        )
        print(f"{new_repo} created from {template_repo}")
        return new_repo


def tag_exists(manager, tag_id, repo_name):
    """Check tag exists or not for the given repo"""
    assert isinstance(repo_name, str), repo_name
    assert isinstance(tag_id, str), tag_id
    assert isinstance(manager, GitOrgManager), manager
    repo = exists(manager, repo_name.split())
    tags = repo.get_tags()
    for tag in tags:
        if tag.name == tag_id:
            print(f"valid tag !!! [{tag_id}] for the repo [{repo}].")
            return tag_id
    error_message = "invalid tag !!! [{}] for the repo [{}].".format(
        tag_id, repo)
    raise Exception(error_message)


def is_admin(manager, collaborator_id, repo_name):
    """Check the given collaborator is admin or not"""
    assert isinstance(repo_name, str), repo_name
    assert isinstance(collaborator_id, str), collaborator_id
    assert isinstance(manager, GitOrgManager), manager
    exists(manager, repo_name.split())
    repo = exists(manager, repo_name.split())
    permission = repo.get_collaborator_permission(collaborator_id)
    if permission == "admin":
        print(f"[{collaborator_id}] is a valid admin for the repo [{repo}].")
        return True
    error_message = "[{}] not an admin for the repo [{}].".format(
        collaborator_id, repo)
    raise Exception(error_message)


def add_topics_to_repos(manager, topics, repos_suffix):
    """Add topics to the repos"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(repos_suffix, list), repos_suffix
    repos_to_add = []
    for repo_suffix in repos_suffix:
        repos_to_add.extend(get_repos_ends_with(manager, repo_suffix))

    if len(repos_to_add) == 0:
        print(f"No repos ends with {repos_suffix}, bailing out")
        return

    new_topics = set(topics)
    for repo in repos_to_add:
        original_topics = set(repo.get_topics())
        missing = new_topics - original_topics
        if len(missing) > 0:
            print(f"Adding topics {missing} to {repo}.")
            repo.replace_topics(list(missing))


def list_repos_with_topics(manager, topics, repos_suffix):
    """list topics to the repos"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(repos_suffix, list), repos_suffix
    repos_to_add = []
    for repo_suffix in repos_suffix:
        repos_to_add.extend(get_repos_ends_with(manager, repo_suffix))

    if len(repos_to_add) == 0:
        print(f"No repos ends with {repos_suffix}, bailing out")
        return

    for repo in repos_to_add:
        check = any(item in repo.get_topics() for item in topics)
        if check is True:
            print(f"{repo.name}")


def has_access(manager, collaborator_id, names, repo_name):
    """has given permissions or not"""
    assert isinstance(repo_name, str), repo_name
    assert isinstance(collaborator_id, str), collaborator_id
    assert isinstance(manager, GitOrgManager), manager
    exists(manager, repo_name.split())
    repo = exists(manager, repo_name.split())
    original_permission = repo.get_collaborator_permission(collaborator_id)
    for permission_name in names:
        if permission_name == original_permission:
            return True
    error_message = (
        "[{}] not having any one of the {} access for the repo [{}].".format(
            collaborator_id, names, repo
        )
    )
    raise Exception(error_message)


def delete_branch_on_merge(manager, repos_suffix):
    """Add topics to the repos"""
    assert isinstance(manager, GitOrgManager), manager
    assert isinstance(repos_suffix, list), repos_suffix
    repos_to_edit = []
    for repo_suffix in repos_suffix:
        repos_to_edit.extend(get_repos_ends_with(manager, repo_suffix))

    if len(repos_to_edit) == 0:
        print(f"No repos ends with {repos_suffix}, bailing out")
        return

    for repo in repos_to_edit:
        if not repo.archived:
            print(f"Processing {repo}")
            repo.edit(
                delete_branch_on_merge=True
            )


def create_pull_request(manager, repo_name, head, base, title):
    """Create pull request"""
    assert isinstance(repo_name, str), repo_name
    assert isinstance(head, str), head
    assert isinstance(base, str), base
    repo = exists(manager, repo_name.split())
    created_pull = repo.create_pull(
        title=title, body=title, head=head, base=base)
    if created_pull:
        print(f"created pull request {created_pull.html_url}")
