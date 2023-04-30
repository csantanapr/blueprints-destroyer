"""

Remove VPCs except default.

"""

import sys
import boto3
from botocore.exceptions import ClientError


def delete_igw(ec2, vpc_id):
  """
  Detach and delete the internet gateway
  """

  args = {
    'Filters' : [
      {
        'Name' : 'attachment.vpc-id',
        'Values' : [ vpc_id ]
      }
    ]
  }

  try:
    igw = ec2.describe_internet_gateways(**args)['InternetGateways']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if igw:
    igw_id = igw[0]['InternetGatewayId']

    try:
      result = ec2.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    except ClientError as e:
      print(e.response['Error']['Message'])

    try:
      result = ec2.delete_internet_gateway(InternetGatewayId=igw_id)
    except ClientError as e:
      print(e.response['Error']['Message'])

  return


def delete_subs(ec2, args):
  """
  Delete the subnets
  """

  try:
    subs = ec2.describe_subnets(**args)['Subnets']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if subs:
    for sub in subs:
      sub_id = sub['SubnetId']

      try:
        result = ec2.delete_subnet(SubnetId=sub_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return


def delete_rtbs(ec2, args):
  """
  Delete the route tables
  """

  try:
    rtbs = ec2.describe_route_tables(**args)['RouteTables']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if rtbs:
    for rtb in rtbs:
      main = 'false'
      for assoc in rtb['Associations']:
        main = assoc['Main']
      if main == True:
        continue
      rtb_id = rtb['RouteTableId']

      try:
        result = ec2.delete_route_table(RouteTableId=rtb_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return


def delete_acls(ec2, args):
  """
  Delete the network access lists (NACLs)
  """

  try:
    acls = ec2.describe_network_acls(**args)['NetworkAcls']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if acls:
    for acl in acls:
      default = acl['IsDefault']
      if default == True:
        continue
      acl_id = acl['NetworkAclId']

      try:
        result = ec2.delete_network_acl(NetworkAclId=acl_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return


def delete_sgps(ec2, args):
  """
  Delete any security groups
  """

  sg_rules = []

  try:
    sgps = ec2.describe_security_groups(**args)['SecurityGroups']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if sgps:
    for sgp in sgps:
      default = sgp['GroupName']
      if default == 'default':
        continue
      sg_id = sgp['GroupId']
      aws_sg_rules = ec2.describe_security_group_rules(Filters=[{'Name': 'group-id','Values': [sg_id,]}])['SecurityGroupRules']

      for sg_rule in aws_sg_rules:
        try:
          print("Deleting security group id "+sg_rule['SecurityGroupRuleId'])
          result = ec2.revoke_security_group_ingress(GroupId=sg_rule['GroupId'],SecurityGroupRuleIds=[sg_rule['SecurityGroupRuleId']])
        except ClientError as e:
          print(e.response['Error']['Message'])

      try:
        result = ec2.delete_security_group(GroupId=sg_id)
      except ClientError as e:
        print("error deleting security group")
        print(e)
        print(e.response['Error']['Message'])

  return

def delete_sgps_rules(ec2, args):
  """
  Delete any security groups rules
  """

  sg_rules = []

  try:
    sgps = ec2.describe_security_groups(**args)['SecurityGroups']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if sgps:
    for sgp in sgps:
      default = sgp['GroupName']
      if default == 'default':
        continue
      sg_id = sgp['GroupId']
      aws_sg_rules = ec2.describe_security_group_rules(Filters=[{'Name': 'group-id','Values': [sg_id,]}])['SecurityGroupRules']

      for sg_rule in aws_sg_rules:
        try:
          if sg_rule['IsEgress'] == False:
            print("Deleting Ingress security group id "+sg_rule['SecurityGroupRuleId'])
            result = ec2.revoke_security_group_ingress(GroupId=sg_rule['GroupId'],SecurityGroupRuleIds=[sg_rule['SecurityGroupRuleId']])
          else:
            print("Deleting Egress security group id "+sg_rule['SecurityGroupRuleId'])
            result = ec2.revoke_security_group_egress(GroupId=sg_rule['GroupId'],SecurityGroupRuleIds=[sg_rule['SecurityGroupRuleId']])
        except ClientError as e:
          print(e.response['Error']['Message'])

  return


def delete_vpc(ec2, vpc_id, region):
  """
  Delete the VPC
  """

  try:
    result = ec2.delete_vpc(VpcId=vpc_id)
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    print('VPC {} has been deleted from the {} region.'.format(vpc_id, region))

  return


def get_regions(ec2):
  """
  Return all AWS regions
  """

  regions = []

  try:
    aws_regions = ec2.describe_regions()['Regions']
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    for region in aws_regions:
      regions.append(region['RegionName'])

  return regions

def get_vpcs(ec2):
  """
  Return all AWS regions
  """

  vpcs = []

  try:
    aws_vpcs = ec2.describe_vpcs()['Vpcs']
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    for vpc in aws_vpcs:
      vpcs.append(vpc['VpcId'])

  return vpcs



def delete_nat_gateways(ec2, args):
  """
  Delete any NAT gateways
  """

  nat_gateways = []

  try:
    nat_gateways = ec2.describe_nat_gateways(**args)['NatGateways']
  except ClientError as e:
    print(e.response['Error']['Message'])

  if nat_gateways:
    for nat_gateway in nat_gateways:
      nat_gateway_id = nat_gateway['NatGatewayId']

      try:
        print("Deleting NAT gateway id "+nat_gateway_id)
        result = ec2.delete_nat_gateway(NatGatewayId=nat_gateway_id)
      except ClientError as e:
        print(e.response['Error']['Message'])

  return

def delete_internet_gateways(ec2, vpc_id):
    """
    Delete any internet gateways
    """

    internet_gateways = []

    try:
        internet_gateways = ec2.describe_internet_gateways(Filters=[
            {
                'Name': 'attachment.vpc-id',
                'Values': [
                    vpc_id,
                ]
            },
        ])['InternetGateways']
    except ClientError as e:
        print(e.response['Error']['Message'])

    if internet_gateways:
        for internet_gateway in internet_gateways:
            internet_gateway_id = internet_gateway['InternetGatewayId']

            try:
                print("Detaching and deleting internet gateway id "+internet_gateway_id)
                result = ec2.detach_internet_gateway(InternetGatewayId=internet_gateway_id, VpcId=vpc_id)
                print("Deleting internet gateway id "+internet_gateway_id)
                result = ec2.delete_internet_gateway(InternetGatewayId=internet_gateway_id)
            except ClientError as e:
                print(e.response['Error']['Message'])

    return


def main(profile, region):
  """
  Do the work..

  Order of operation:

  - Delete NAT gateways
  - Delete the internet gateway
  - Delete subnets
  - Delete route tables
  - Delete network access lists
  - Delete security group rules (ie ingress and egress)
  - Delete security groups
  - Delete the VPC
  """

  # AWS Credentials
  # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

  session = boto3.Session(profile_name=profile)
  ec2 = session.client('ec2', region_name=region)

  vpcs = get_vpcs(ec2)
  print(vpcs)


  for vpc_id in vpcs:

    # get vpc info
    try:
      vpc = ec2.describe_vpcs(VpcIds=[vpc_id])['Vpcs'][0]
    except ClientError as e:
      print(e.response['Error']['Message'])

    #check if vpc is the default
    if vpc['IsDefault']:
      print('VPC {} is the default VPC in the {} region. Skipping it'.format(vpc_id, region))
      continue



    args = {
      'Filters' : [
        {
          'Name' : 'vpc-id',
          'Values' : [ vpc_id ]
        }
      ]
    }
    result = delete_nat_gateways(ec2, args)

    try:
      eni = ec2.describe_network_interfaces(**args)['NetworkInterfaces']
    except ClientError as e:
      print(e.response['Error']['Message'])
      return

    if eni:
      print('VPC {} has existing resources in the {} region.'.format(vpc_id, region))
      continue

    print("Starting to delete VPC "+vpc_id)

    result = delete_internet_gateways(ec2, vpc_id)
    #result = delete_igw(ec2, vpc_id)
    result = delete_subs(ec2, args)
    result = delete_rtbs(ec2, args)
    result = delete_acls(ec2, args)
    result = delete_sgps_rules(ec2, args)
    result = delete_sgps(ec2, args)
    result = delete_vpc(ec2, vpc_id, region)

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

