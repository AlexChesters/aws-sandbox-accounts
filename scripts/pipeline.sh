set -e

aws cloudformation deploy \
  --template-file ci/codepipeline.yml \
  --stack-name codepipeline-aws-sandbox-accounts \
  --capabilities CAPABILITY_IAM \
  --region eu-west-1 \
  --profile sandbox-administrator
