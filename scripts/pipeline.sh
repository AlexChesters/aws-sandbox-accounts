set -e

rain deploy \
  ci/codepipeline.yml \
  codepipeline-aws-sandbox-accounts-apps \
  --yes \
  --region eu-west-1 \
  --profile sandbox-administrator
