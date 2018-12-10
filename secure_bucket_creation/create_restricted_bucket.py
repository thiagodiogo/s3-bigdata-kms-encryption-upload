import boto3, sys, os

def create_cloud_trail(self, trail_name, bucket_name, prefix):
    ''' Create a cloud trail to keep all bucket access '''
    trail_client = boto3.client('cloudtrail')
    trail_client.create_trail(Name=trail_name, S3BucketName=bucket_name, S3KeyPrefix=prefix)

def locate_key(alias, region_name):
    ''' Retrieve and describe a key from KMS '''
    kms_client = boto3.client('kms', region_name=region_name)

    print("Locating the key with alias: %s" % alias)
    response = kms_client.describe_key(KeyId="alias/" + alias)
    return response

def create_kms_key(s3_key_name, region_name, policy, create_alias=False):
    ''' Create a KMS key and a alias based on a policy '''
    kms_client = boto3.client('kms', region_name=region_name)

    if policy:
        response = kms_client.create_key(
            Policy=policy,
            Tags=[{'TagKey': 's3-bucket-key','TagValue': s3_key_name},]
        )
    else:
        response = kms_client.create_key(
            Tags=[{'TagKey': 's3-bucket-key','TagValue': s3_key_name},]
        )
    if create_alias:
        alias_key = "alias/%s" % s3_key_name
        kms_client.create_alias(
            AliasName=alias_key, TargetKeyId=response['KeyMetadata']['KeyId']
        )
    return response['KeyMetadata']['KeyId']

account_id = sys.argv[1]
s3_user = sys.argv[2]
region = sys.argv[3]
bucket_name = sys.argv[4]
ip_range = sys.argv[5]

try:
    key = locate_key(bucket_name, region)
    key_id = key['KeyMetadata']['KeyId']
    print("Key located: %s" % key_id)
except Exception as e:
    print(e)
    print("Inexistent key, creating a new one")
    key_policy = open("key_policy.json").read()
    key_policy = key_policy.replace("{{ACC_ID}}", account_id)
    key_policy = key_policy.replace("{{S3_USER}}", s3_user)
    key_id = create_kms_key(bucket_name, region, key_policy, True)
    print("Key created: %s" % key_id)

bucket_policy = open("bucket_restrict_policy.json").read()
bucket_policy = bucket_policy.replace("{{BUCKET_NAME}}", bucket_name)
bucket_policy = bucket_policy.replace("{{IP_RANGE}}", ip_range)
bucket_policy = bucket_policy.replace("{{REGION}}", region)
bucket_policy = bucket_policy.replace("{{ACC_ID}}", account_id)
bucket_policy = bucket_policy.replace("{{KEY_ID}}", key_id)

s3 = boto3.client('s3', region_name=region)
s3.create_bucket(Bucket=bucket_name, ACL='private',
    CreateBucketConfiguration={'LocationConstraint': region})

s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
s3.put_bucket_encryption(Bucket=bucket_name,
    ServerSideEncryptionConfiguration={
        'Rules': [
            {
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'aws:kms',
                    'KMSMasterKeyID': key_id
                }
            },
        ]})

# kw_args = {
#     'Bucket': bucket_name,
#     'BucketLoggingStatus': {
#         'LoggingEnabled': {
#             'TargetBucket': 'trail-s3-bucket-logging',
#             'TargetPrefix': 'usda-s3-audit/'
#         }
#     }
# }
# s3.put_bucket_logging(**kw_args)

s3 = boto3.resource('s3')
bucket_versioning = s3.BucketVersioning(bucket_name)
bucket_versioning.enable()

print("Bucket '%s' created with success" % bucket_name)
