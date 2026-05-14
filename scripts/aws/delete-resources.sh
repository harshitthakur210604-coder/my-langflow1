# aws cloudformation delete-stack --stack-name HarxitFlowAppStack
aws ecr delete-repository --repository-name harxitflow-backend-repository --force
# aws ecr delete-repository --repository-name harxitflow-frontend-repository --force
# aws ecr describe-repositories --output json | jq -re ".repositories[].repositoryName"