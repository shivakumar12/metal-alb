"""
Initialize GitOrgManager with organization details.
"""
import yaml
from github import Github


class GitOrgManager:
    """
    Initialize GitOrgManager with organization name and token.
    """

    def __init__(self, organization_name, organization_token):
        self.organization_name = organization_name
        self.config = self.read_config()
        self.github = Github(
            base_url=self.config["github_url"],
            login_or_token=organization_token,
        )
        self.organization = self.github.get_organization(
            self.organization_name)

    def read_config(self):
        """Read the github org configuration"""
        config_file_name = self.organization_name + "-conf.yml"
        try:
            with open(config_file_name) as config_file:
                config = yaml.load(config_file, yaml.FullLoader)
                return config
        except IOError as exception:
            print(
                "Couldn't load configuration file ‘%s’. "
                "Maybe you should create it?\n"
                "See e.g. org-conf.yml.example"
            ) % config_file_name
            raise SystemExit from exception
