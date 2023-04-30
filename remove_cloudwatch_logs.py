"""

Remove EKS Clusters.

"""

import sys
import boto3


def get_log_groups(logs):
  """
  Get log groups.
  """

  log_groups = []

  # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_log_groups
  # https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DescribeLogGroups.html

  response = logs.describe_log_groups()

  for log_group in response['logGroups']:
    log_groups.append(log_group['logGroupName'])

  return log_groups

def delete_log_groups(logs, log_groups):
    """
    Delete log groups.
    """

    for log_group in log_groups:
      print("Deleting log group="+log_group)

      # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_log_group
      # https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DeleteLogGroup.html

      logs.delete_log_group(logGroupName=log_group)


def main(profile, region):
  """
  Do the work..

  Order of operation:

  - Delete log groups
  """

  # AWS Credentials
  # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

  session = boto3.Session(profile_name=profile)
  logs = session.client('logs', region_name=region)

  log_group_names = get_log_groups(logs)
  print(log_group_names)
  delete_log_groups(logs, log_group_names)

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


