from aws_cdk import (
    App,
    Stack,
    RemovalPolicy,
    aws_iam as iam,
    aws_s3 as s3
)

class GitOpsIAMRole(Stack):
    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear el rol para GitHub Actions
        github_actions_role = iam.Role(
            self, "GitHubActionsRole",
            assumed_by=iam.FederatedPrincipal(
                federated="token.actions.githubusercontent.com",
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

        # Crear el bucket S3 para los assets del CDK
        asset_bucket = s3.Bucket(
            self, "CDKAssetBucket",
            bucket_name="cdk-hnb659fds-assets-122610492430-us-east-1",
            removal_policy=RemovalPolicy.RETAIN,  # Corregido aquí
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True
        )

        # Definir la política del bucket para permitir acceso a GitHub Actions
        asset_bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
            resources=[asset_bucket.bucket_arn, f"{asset_bucket.bucket_arn}/*"],
            principals=[github_actions_role]
        ))

        # Añadir permisos necesarios al rol
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "cloudformation:*",
                "s3:*",
                "sts:AssumeRole",
                "ec2:Describe*",
                "iam:GetRole",
                "iam:ListRoles"
            ],
            resources=["*"]  # Note: Using '*' for broad permissions, adjust as necessary for security.
        ))

app = App()
GitOpsIAMRole(app, "GitOpsIAMRole")
app.synth()