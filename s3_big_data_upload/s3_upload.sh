#!/usr/bin/env bash
FOLDER=$1
BUCKET_NAME=$2 #test-bucket-kms
THREADS=$3 #60

echo "Folder:$FOLDER"
echo "S3 Bucket:$BUCKET_NAME"
echo "Thread:$THREADS"

ls -1 $FOLDER | time parallel -j$THREADS -I % aws s3 cp $FOLDER/% s3://$BUCKET_NAME
