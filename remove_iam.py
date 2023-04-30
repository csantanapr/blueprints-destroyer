"""

Remove EKS Clusters.

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



def main(profile, region):
  """
  Do the work..

  Order of operation:

  1.) Delete Node Groups of EKS Cluster
  2.) Delete EKS Cluster
  """

  # AWS Credentials
  # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

  session = boto3.Session(profile_name=profile)
  iam = session.client('iam', region_name=region)



  return

def parse_command_line_option(argv):

  if len(argv) != 3:
    print("Usage: python remove_eks.py <profile> <region>")
    sys.exit(2)

  profile = argv[1]
  region = argv[2]

  print("Profile="+profile+", Region="+region)

  main(profile, region)


if __name__ == "__main__":
  parse_command_line_option(sys.argv)


