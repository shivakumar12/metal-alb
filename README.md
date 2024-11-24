# Git Organization Manager (GOM)

<a href='https://jenkis.com/job/application-operations/job/git-operations/job/build-gom-image/'><img src='https://jenkins.com/buildStatus/icon?job=application-operations%2Fgit-operations%2Fbuild-gom-image'></a>

 ***The python API to perform git operations***


## Usage 
```sh
$ gom.py --help
usage: gom.py [-h] {team,repo,user} ...

positional arguments:
  {team,repo,user}

optional arguments:
  -h, --help        show this help message and exit
```

# Repository

## Usage
```sh
$ gom.py repo --help
usage: gom.py repo [-h] --org-name <str> --org-token <str> --triggered-by <str>
                   {exists,create,create-from-template,list,add-collaborators,remove-collaborators,add-teams,remove-teams} ...

positional arguments:
  {exists,create,create-from-template,list,add-collaborators,remove-collaborators,add-teams,remove-teams}

optional arguments:
  -h, --help            show this help message and exit
  --org-name <str>      name of the organization
  --org-token <str>     security token of the organization
  --triggered-by <str>  collaborator/user-id who is running this framework (IXXXXXX)
```
## List

The below command will ***LIST*** all the repos in ***sf-k8s*** organization

```sh
$ gom.py repo --org-name=sf-k8s --org-token=<YOUR_TOKEN> --triggered-by=IXXXXXX list
```

## Exists

### Usage
```sh
λ gom.py repo exists --help
usage: gom.py repo exists [-h] --repo-names <str>

optional arguments:
  -h, --help          show this help message and exit
  --repo-names <str>  checks whether the repo's exists or not.e.g comma separated repo name's [--repo-names=test-repo-1,test-repo-2,test-    
                      repo-3]
```
### Check repo exists or not
The below command will  check ***EXISTS*** of the ***repos (comma separated)***  from template for the repo names ***--repo-names***
```sh
$ gom.py repo --org-name=sf-k8s --org-token=<YOUR_TOKEN> --triggered-by=IXXXXXX exists --repo-names=test-repo-1,test-repo-2,test-repo-3
```

## Create-Repo

### Usage
```sh
$ gom.py repo create-from-template --help
usage: gom.py repo create-from-template [-h] --template-repo-name <str> --repo-names <str>

optional arguments:
  -h, --help            show this help message and exit
  --template-repo-name <str>
                        creates the repos from template [--template-repo-name=ms-template-kustomize-prod-config]
  --repo-names <str>    comma separated repos that needs to be created [--repo-names=test-repo-1,test-repo-2,test-repo-3]
```
### Creating Repo from template

The below command will ***CREATES*** the ***repos (comma separated)***  from template for the repo names ***--repo-names***
```sh
$ gom.py repo --org-name=sf-k8s --org-token=<YOUR_TOKEN> --triggered-by=IXXXXXX create-from-template --template-repo-name=ms-template-kustomize-dev-config --repo-names=test-repo-1,test-repo-2,test-repo-3
```

## Add-Collaborators

### Usage
```sh
$ gom.py repo add-collaborators --help
usage: gom.py repo add-collaborators [-h] --ID <str>  --repo-suffix <str> --access <str>

optional arguments:
  -h, --help           show this help message and exit
  --ID <str>           e.g comma separated collaborator ID's [ID=IXXXXXX,IXXXXXX,IXXXXXX]
  --repos-suffix <str>  suffix of the repository, multiple repositories will be processed if matches.
  --access <str>       push/pull/admin
```
### Adding collaborator
The below command will ***ADDS*** the ***collaborators (comma separated)***  to all the repos that ends with ***--repos-suffix*** with ***specific access(pull/push/admin)***
```sh
λ gom.py repo --org-name=org --org-token=<YOUR_TOKEN> --triggered-by=IXXXXXX add-collaborators --ID=IXXXXXX,IXXXXXX --repos-suffix=-prod-config,-dev-config  --access=push
```

## Remove-Collaborators

### Usage
```sh
$ gom.py repo remove-collaborators --help
usage: gom.py repo remove-collaborators [-h] --ID <str> --repos-suffix <str>

optional arguments:
  -h, --help            show this help message and exit
  --ID <str>            comma separated collaborator ID's [--ID=IXXXXXX,IXXXXXX,IXXXXXX]
  --repos-suffix <str>  comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if
                        matches.
```
### Remove collaborator
The below command will ***REMOVES*** the ***collaborators (comma separated)***  to all the repos that ends with ***--repos-suffix*** 
```sh
$ gom.py repo --org-name=org --org-token=<YOUR_TOKEN> --triggered-by=IXXXXXX remove-collaborators --ID=IXXXXXX,IXXXXXX --repos-suffix=-prod-config,-dev-config
```
## Add-Teams
```sh
$ gom.py repo add-teams --help
usage: gom.py repo add-teams [-h] --name <str> --repos-suffix <str> --access <str>

optional arguments:
  -h, --help            show this help message and exit
  --name <str>          comma separated team name's [--name=exp-digital-assistant-prod-config,ayt-reporting-prod-config]
  --repos-suffix <str>  comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if
                        matches.
  --access <str>        read/write/admin
```
The below command will ***ADDS*** the ***teams (comma separated)*** to all the repos that ends with ***--repos-suffix*** with ***specific access(read/write/admin)***
```sh
$ ./gom.py repo add-teams --org-name=org --org-token=<YOUR_TOKEN> --triggered-by=IXXXXXX --name=recruiting-prod-config,rewarding-prod-config  --repo-suffix=-dev-config.-prod-config --access=write
```

## Remove-Teams
```sh
$ gom.py repo remove-teams --help
usage: gom.py repo remove-teams [-h] --name <str> --repos-suffix <str> --access <str>

optional arguments:
  -h, --help            show this help message and exit
  --name <str>          comma separated team name's [--name=exp-digital-assistant-prod-config,ayt-reporting-prod-config]
  --repos-suffix <str>  comma separated repos suffix [--repos-suffix=-prod-config,-dev-config], multiple repositories will be processed if
                        matches.
  --access <str>        read/write/admin
```
The below command will ***REMOVES*** the ***teams (comma separated)*** to all the repos that ends with ***--repos-suffix*** with ***specific access(read/write/admin)***
```sh
$ ./gom.py repo remove-teams --org-name=sf-k8s --org-token=<YOUR_TOKEN> --triggered-by=IXXXXXX --name=recruiting-prod-config,rewarding-prod-config  --repo-suffix=-dev-config.-prod-config
```
# Team


## List

The below command will ***LIST*** all the teams in ***sf-k8s*** organization
```sh
$ gom.py team --org-name=sf-k8s --org-token=<YOUR_TOKEN> --triggered-by=IXXXXXX list
```

# Docker Image

### Prerequisite
https://skaffold.dev/docs/install/

### Build Image
```sh
$ git clone https://github.com/org/git-org-manager.git
$ cd git-org-manager
$ skaffold build
```
