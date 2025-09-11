set -e

rain deploy \
  ci/codepipeline.yml \
  codepipeline-aws-sandbox-accounts-common-resources \
  --yes \
  --region eu-west-1 \
  --profile sandbox-administrator
