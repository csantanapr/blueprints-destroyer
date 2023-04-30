"""

Remove EKS Clusters.

"""

import sys
import boto3
from botocore.exceptions import ClientError
import time


def get_eks_clusters(client):
  """
  Return all EKS Clusters
  """
  try:
    response = client.list_clusters()['clusters']
  except ClientError as e:
    print(e.response['Error']['Message'])

  return response

def get_eks_cluster_nodegroups(client, cluster):
  """
  Return all EKS Cluster NodeGroups
  """
  try:
    response = client.list_nodegroups(clusterName=cluster)['nodegroups']
  except ClientError as e:
    print(e.response['Error']['Message'])

  return response

def delete_eks_cluster_nodegroups(client, cluster):
  """
  Delete EKS Cluster NodeGroups
  """

  try:
    response = client.list_nodegroups(clusterName=cluster)['nodegroups']
  except ClientError as e:
    print(e.response['Error']['Message'])

  for node_group in response:
    delete_eks_cluster_nodegroup(client, cluster, node_group)

  return

def delete_eks_cluster_nodegroup(client, cluster, node_group):
  """
  Delete EKS Cluster NodeGroups
  """

  try:
    print("Deleting nodegroup="+node_group+", In cluster="+cluster)
    result = client.delete_nodegroup(clusterName=cluster, nodegroupName=node_group)
  except ClientError as e:
    print(e.response['Error']['Message'])

  return

def wait_node_group_deleted(client, cluster, node_group):
  """
  Wait for node group to be deleted
  """
  while (True):
    try:
      response = client.describe_nodegroup(clusterName=cluster,nodegroupName=node_group)['nodegroup']
    except ClientError as e:
      print("Node group deleted")
      break
    else:
      print("Node group still exists")
      time.sleep( 30 )

  return

# Delete all eks cluster for specific region
def delete_eks_clusters(client):
  """
  Delete all EKS Clusters
  """
  # get all clusters to delete
  clusters = client.list_clusters()['clusters']
  for c in clusters:
    delete_eks_cluster(client, c)

  return

def delete_eks_cluster(client, cluster):
    """
    Delete EKS Cluster
    """
    try:
      print("Deleting cluster="+cluster)
      result = client.delete_cluster(name=cluster)
    except ClientError as e:
      print(e.response['Error']['Message'])

    return


def wait_cluster_deleted(client, cluster):
    """
    Wait for cluster to be deleted
    """
    while (True):
      try:
        response = client.describe_cluster(name=cluster)['cluster']
      except ClientError as e:
        print("Cluster deleted")
        break
      else:
        print("Cluster still exists")
        time.sleep( 30 )

    return

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
  eks = session.client('eks', region_name=region)

  # Delete eks node groups
  for c in get_eks_clusters(eks):
    delete_eks_cluster_nodegroups(eks, c)

  # Wait for all node groups to be deleted
  for c in get_eks_clusters(eks):
    for n in get_eks_cluster_nodegroups(eks, c):
      wait_node_group_deleted(eks, c, n)

  # Delete eks clusters
  delete_eks_clusters(eks)

  # Wait for all clusters to be deleted
  for c in get_eks_clusters(eks):
    wait_cluster_deleted(eks, c)

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


