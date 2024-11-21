#!/bin/bash
AWS_KEY_ID=$(grep aws_key_id ./data/parameters.txt | awk '{print $2}')
AWS_SECRET_KEY=$(grep aws_secret_key ./data/parameters.txt | awk '{print $2}')
#echo $AWS_KEY_ID
#echo $AWS_SECRET_KEY
LOCAL_FILE=/opt/factorio/saves/$1
BUCKET_NAME=$(grep bucket_name ./data/parameters.txt | awk '{print $2}')
OBJECT_PATH=$1
result=$(curl --silent \
  --request PUT \
  --user "${AWS_KEY_ID}:${AWS_SECRET_KEY}" \
  --aws-sigv4 "aws:amz:ru-central1:s3" \
  --upload-file "${LOCAL_FILE}" \
  --verbose \
  --stderr - \
  "https://storage.yandexcloud.net/${BUCKET_NAME}/${OBJECT_PATH}")

check_file_name=$(echo $result | grep  "Can't open")

if [ "$check_file_name" = "" ]; then
   echo $result | grep -o 'HTTP/2 [0-9][0-9][0-9] '
else
   echo $check_file_name
fi
