# Encryption using AWS SDK + Big data upload to S3

## Encryption using AWS KMS (/encryption)

### Introduction
https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/introduction.html

### How AWS SDK encryption works:
https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/how-it-works.html

### Encrypt data:

`python encrypt.py <KEY_ARN> <PLAIN_FILE> <ENCRYPTED_FILE>`
Plain file to be encrypted: <PLAIN_FILE>
Details: posix.stat_result(st_mode=33188, st_ino=45816020, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=102400000, st_atime=1544399373, st_mtime=1544397779, st_ctime=1544398900)
Starting at 2018-12-09 18:53:05.402926
File encrypted: <ENCRYPTED_FILE>
Details: posix.stat_result(st_mode=33188, st_ino=45816135, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=103200574, st_atime=1544399214, st_mtime=1544399589, st_ctime=1544399589)
Ending at 2018-12-09 18:53:09.349755
Total elapsed time: 0:00:03.946829

### Decrypt data:

`$ python decrypt.py <KEY_ARN> <ENCRYPTED_FILE> <DECRYPTED_FILE>`
Encrypted file to be decrypted: <ENCRYPTED_FILE>
Details: posix.stat_result(st_mode=33188, st_ino=45816135, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=103200574, st_atime=1544399214, st_mtime=1544399589, st_ctime=1544399589)
Starting at 2018-12-09 18:53:18.329322
File decrypted: <DECRYPTED_FILE>
Details: posix.stat_result(st_mode=33188, st_ino=45816195, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=102400000, st_atime=1544399012, st_mtime=1544399602, st_ctime=1544399602)
Ending at 2018-12-09 18:53:22.924382

### Comparing files after decryption

```
cmp --silent <PLAIN_FILE> <DECRYPTED_FILE> && echo '### SUCCESS: Files Are Identical! ###' || echo '### WARNING: Files Are Different! ###'
### SUCCESS: Files Are Identical! ###
```

## Secure S3 bucket creation (/secure_bucket_creation)

Details:
If

Command:
`python create_restricted_bucket.py account_id s3_user region bucket_name ip_range`

## S3 Big data upload (s3_big_data_upload)

### Prepare + Split files

Using linux split command: `split -b 5000k --numeric-suffixes <BIG_FILE> <PREFIX>`

Example: `split -b 5000k --numeric-suffixes FILE.txt segment-`

### Upload to S3 in parallel

Permissions:
`chmod +x s3_upload.sh`

Upload in parallel processes to S3:
`s3_upload.sh <FULL_PATH_TO_FOLDER> <S3_BUCKET_NAME> <N_PROCESSES>`

### References:

Encryption: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html
Allow by IP: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_deny-ip.html

Uploading multiple files to AWS S3 in parallel:
https://netdevops.me/2018/uploading-multiple-files-to-aws-s3-in-parallel/
https://aws.amazon.com/blogs/apn/getting-the-most-out-of-the-amazon-s3-cli/

Other tools:
https://s3tools.org/usage
http://s3browser.com/
