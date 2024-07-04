set -e

aws cloudformation deploy \
  --template-file ci/codepipeline.yml \
  --stack-name codepipeline-aws-sandbox-accounts \
  --capabilities CAPABILITY_IAM \
  --region eu-west-1 \
  --profile sandbox-administrator

aws cloudformation deploy \
  --template-file ci/lambda-build-image/codepipeline.yml \
  --stack-name codepipeline-aws-sandbox-accounts-lambda-build-image \
  --capabilities CAPABILITY_IAM \
  --region eu-west-1 \
  --profile sandbox-administrator
