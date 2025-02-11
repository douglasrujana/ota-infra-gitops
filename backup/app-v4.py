from aws_cdk import (
    App,
    Stack,
    aws_iam as iam,
    aws_s3 as s3
)

class GitOpsIAMRole(Stack):
    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        github_actions_role = iam.Role(
            self, "GitHubActionsRole",
            assumed_by=iam.FederatedPrincipal(
                federated="arn:aws:iam::122610492430:oidc-provider/token.actions.githubusercontent.com",
                assume_role_action="sts:AssumeRoleWithWebIdentity",
                conditions={
                    "StringEquals": {
                        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                        "token.actions.githubusercontent.com:sub": "repo:douglasrujana/ota-infra-gitops:ref:refs/heads/main"
                    }
                }
            ),
            description="Role for GitHub Actions to deploy with CDK"
        )

        # 🔹 Permisos para CloudFormation
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "cloudformation:GetTemplate",
                "cloudformation:DescribeStacks",
                "cloudformation:CreateStack",
                "cloudformation:UpdateStack",
                "cloudformation:DeleteStack",
                "cloudformation:ListStackResources"
            ],
            resources=["*"]
        ))

        # 🔹 Permisos para IAM y PassRole
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=["iam:PassRole"],
            resources=["arn:aws:iam::122610492430:role/cdk-hnb659fds-cfn-exec-role-*"]
        ))

        # 🔹 Permisos para S3
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:GetObject", "s3:ListBucket", "s3:PutObject"],
            resources=["arn:aws:s3:::cdk-hnb659fds-assets-122610492430-us-east-1", "arn:aws:s3:::cdk-hnb659fds-assets-122610492430-us-east-1/*"]
        ))

        # 🔹 Configurar el bucket de assets sin eliminarlo
        existing_bucket_arn = "arn:aws:s3:::cdk-hnb659fds-assets-122610492430-us-east-1"
        asset_bucket = s3.Bucket.from_bucket_arn(self, "CDKAssetBucket", existing_bucket_arn)

app = App()
GitOpsIAMRole(app, "GitOpsIAMRole")
app.synth()
