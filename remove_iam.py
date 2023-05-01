"""

Remove IAM resources

"""

import sys
import boto3



def main(profile):
  """
  Do the work..

  Order of operation:

  - Delete iam roles and policies
  """

  # AWS Credentials
  # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

  session = boto3.Session(profile_name=profile)

  # create an IAM client
  iam = session.client('iam')

  # set the tag key and value to filter by
  tag_key = 'GithubRepo'
  tag_value = 'github.com/aws-ia/terraform-aws-eks-blueprints'
  delete_roles(iam, tag_key, tag_value)

  delete_policies(iam, tag_key, tag_value)


def delete_policies(iam, tag_key,tag_value):
  # get a list of all IAM roles
  response = iam.list_policies()

  # iterate through the roles and filter by tag
  for policy in response['Policies']:
      # get the tags for the role
      policy_tags = iam.list_policy_tags(PolicyArn=policy['Arn'],MaxItems=1000)['Tags']
      # check if the role has the desired tag
      if any(tag['Key'] == tag_key and tag['Value'] == tag_value for tag in policy_tags):
        # delete the policy
        print(f"Deleting policy {policy['PolicyName']}")
        iam.delete_policy(PolicyArn=policy['Arn'])



def delete_roles(iam, tag_key,tag_value):
  # get a list of all IAM roles
  response = iam.list_roles()

  # iterate through the roles and filter by tag
  for role in response['Roles']:
      # check if role starts with 'cluster-'
      if role['RoleName'].startswith('cluster-'):
        detach_policies_from_role(iam, role)
        # delete the role
        print(f"Deleting role {role['RoleName']}")
        iam.delete_role(RoleName=role['RoleName'])
        continue

      # get the tags for the role
      role_tags = iam.list_role_tags(RoleName=role['RoleName'])['Tags']
      # check if the role has the desired tag
      if any(tag['Key'] == tag_key and tag['Value'] == tag_value for tag in role_tags):
        detach_policies_from_role(iam, role)
        # delete the role
        print(f"Deleting role {role['RoleName']}")
        iam.delete_role(RoleName=role['RoleName'])

def detach_policies_from_role(iam, role):
  policies = iam.list_attached_role_policies(RoleName=role['RoleName'],MaxItems=1000)['AttachedPolicies']
  # print the policies
  print(f"Policies attached to role {role['RoleName']}:")
  for policy in policies:
      # detach the policy
      iam.detach_role_policy(RoleName=role['RoleName'], PolicyArn=policy['PolicyArn'])
      # delete the policy if not AWS managed
      # print details of policy
      policy = iam.get_policy(PolicyArn=policy['PolicyArn'])
      if 'arn:aws:iam::aws:policy' not in policy['Policy']['Arn']:
          print("Deleting policy", policy['Policy']['Arn'])
          try:
            iam.delete_policy(PolicyArn=policy['PolicyArn'])
          except:
             print("Failed to delete policy", policy['Policy']['Arn'])


  # list role policies
  role_policies = iam.list_role_policies(RoleName=role['RoleName'])['PolicyNames']
  # print the role policies
  print(f"Role policies attached to role {role['RoleName']}:")
  # iterate through the role policies and delete them
  for role_policy in role_policies:
      print(role_policy)
      # delete the role policy
      iam.delete_role_policy(RoleName=role['RoleName'], PolicyName=role_policy)


def parse_command_line_option(argv):

  if len(argv) != 2:
    print("Usage: python remove_iam.py <profile>")
    sys.exit(2)

  profile = argv[1]

  print("Profile="+profile)

  main(profile)


if __name__ == "__main__":
  parse_command_line_option(sys.argv)


