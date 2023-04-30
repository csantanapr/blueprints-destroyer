"""

Remove IAM Resources

This script removes IAM Resources for EKS Cluster.

"""

import sys
import boto3
from botocore.exceptions import ClientError
import time

def delete_open_id_connect_providers(iam, open_id_connect_provider_arns):
  """
  Delete OpenID Connect Providers.

  :param iam: AWS IAM Client
  :param open_id_connect_provider_arns: OpenID Connect Provider ARNs
  """

  for open_id_connect_provider_arn in open_id_connect_provider_arns:
    try:
      print("Deleting OpenID Connect Provider: " + open_id_connect_provider_arn)
      iam.delete_open_id_connect_provider(
        OpenIDConnectProviderArn=open_id_connect_provider_arn
      )
    except ClientError as e:
      print(e)

  return


def get_open_id_connect_providers(iam):
  """
  Get OpenID Connect Providers.

  :param iam: AWS IAM Client
  :return: OpenID Connect Provider ARNs
  """

  open_id_connect_provider_arns = []

  try:
    open_id_connect_providers = iam.list_open_id_connect_providers()
    for open_id_connect_provider in open_id_connect_providers['OpenIDConnectProviderList']:
      open_id_connect_provider_arns.append(open_id_connect_provider['Arn'])
  except ClientError as e:
    print(e)

  return open_id_connect_provider_arns



def main(profile):
  """
  Do the work..

  - Delete OIDC providers
  """

  # AWS Credentials
  # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

  session = boto3.Session(profile_name=profile)
  # Initialize IAM Client
  iam = session.client('iam')

  open_id_connect_provider_arns = get_open_id_connect_providers(iam)

  for open_id_connect_provider_arn in open_id_connect_provider_arns:
    # Get the open id connect provider and print details
    open_id_connect_provider = iam.get_open_id_connect_provider(
      OpenIDConnectProviderArn=open_id_connect_provider_arn
    )
    delete_open_id_connect_providers(iam, [open_id_connect_provider_arn])

  return

def parse_command_line_option(argv):

  if len(argv) != 2:
    print("Usage: python remove_oidc.py <profile>")
    sys.exit(2)

  profile = argv[1]

  print("Profile="+profile)

  main(profile)


if __name__ == "__main__":
  parse_command_line_option(sys.argv)


