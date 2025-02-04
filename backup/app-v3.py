from aws_cdk import (
    App,
    Stack,
    aws_iam as iam,
    aws_s3 as s3
)

class GitOpsIAMRole(Stack):
    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Referenciar el bucket de assets existente en CDK Bootstrap
        existing_bucket_arn = "arn:aws:s3:::cdk-hnb659fds-assets-122610492430-us-east-1"
        asset_bucket = s3.Bucket.from_bucket_arn(self, "CDKAssetBucket", existing_bucket_arn)

        # Rol para GitHub Actions
        github_actions_role = iam.Role(
            self, "GitHubActionsRole",
            assumed_by=iam.FederatedPrincipal(
                "arn:aws:iam::122610492430:oidc-provider/token.actions.githubusercontent.com",
                conditions={
                    "StringEquals": {
                        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                        "token.actions.githubusercontent.com:sub": "repo:douglasrujana/ota-infra-gitops:ref:refs/heads/main"
                    }
                }
            ),
            description="Role for GitHub Actions to deploy with CDK"
        )

        # Política para acceder al bucket de assets
        asset_bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
            resources=[asset_bucket.bucket_arn, f"{asset_bucket.bucket_arn}/*"],
            principals=[github_actions_role]
        ))

        # Permisos necesarios para despliegue con CDK
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "cloudformation:*",
                "s3:*",
                "sts:AssumeRole",
                "ec2:Describe*",
                "iam:GetRole",
                "iam:ListRoles",
                "iam:PassRole"  # Permite delegar roles necesarios para CDK
            ],
            resources=[
                "*"
            ]
        ))

        # Permitir `iam:PassRole` específicamente para el rol de ejecución de CloudFormation
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=["iam:PassRole"],
            resources=["arn:aws:iam::122610492430:role/cdk-hnb659fds-cfn-exec-role-*-us-east-1"]
        ))

app = App()
GitOpsIAMRole(app, "GitOpsIAMRole")
app.synth()
