"""

Remove Customer KMS.

"""

import sys
import boto3



def main(profile, region):
  """
  Do the work..

  Order of operation:

  - Delete log groups
  """

  # AWS Credentials
  # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

  session = boto3.Session(profile_name=profile)
  # KMS client
  kms_client = session.client('kms', region_name=region)


  # Delete customer keys
  # response = kms_client.list_keys()['Keys']
  # for key in response:
  #   key_description = kms_client.describe_key(KeyId=key['KeyId'])['KeyMetadata']
  #   #print("Key description: ",key_description)
  #   if key_description['KeyManager'] == 'CUSTOMER' and key_description['Enabled']:
  #     print("Key description Manager: ",key_description['KeyManager'])
  #     print("Key description Enabled: ",key_description['Enabled'])
  #     print("Deleting key: ",key)
  #     #kms_client.schedule_key_deletion(KeyId=key['KeyId'], PendingWindowInDays=1)


  # Delete all key aliases with eks in name
  response = kms_client.list_aliases()['Aliases']
  for key in response:
    if 'eks' in key['AliasName']:
      print("Deleting key alias: ",key)
      kms_client.delete_alias(AliasName=key['AliasName'])




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


