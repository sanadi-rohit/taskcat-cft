# cfn_ci_cd
CloudFormation CI/CD pipeline.

Full description of implementation can be found in the Medium website on the following [Link](https://medium.com/@nursultanbekenov/awsome-devops-projects-validation-pipeline-for-cloudformation-templates-d26ae5416078)

## Requirements

| Name | Version |
|------|---------|
| python | 3.X |
| aws-cli | 1.X|
| taskcat | 0.9.X |

## Usage
Submit pull-requests to `master` branch.

```
# install python env
virtualenv -p /usr/local/bin/python3.7 .env 
source .env/bin/activate
pip install -r requirements.txt

# install cfn-nag - security checks and advices
brew install ruby brew-gem
brew gem install cfn-nag

# configure aws profile
pip install --upgrade awscli
aws configure

# run lint test
cfn-lint templates/*

# run CFN-Nag to pinpoint security problems
cfn_nag_scan --input-path  templates/* 

# run taskcat test
taskcat test run

```