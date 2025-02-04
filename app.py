from aws_cdk import (
    App,
    Stack,
    aws_iam as iam,
    aws_s3 as s3
)

class GitOpsIAMRole(Stack):
    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # ARN del bucket de assets de CDK (debe existir previamente)
        existing_bucket_arn = "arn:aws:s3:::cdk-hnb659fds-assets-122610492430-us-east-1"
        asset_bucket = s3.Bucket.from_bucket_arn(self, "CDKAssetBucket", existing_bucket_arn)

        # Crear el rol para GitHub Actions
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

        # Permitir acceso al bucket de assets de CDK
        asset_bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
            resources=[asset_bucket.bucket_arn, f"{asset_bucket.bucket_arn}/*"],
            principals=[github_actions_role]
        ))

        # Permisos para `iam:PassRole` sobre el `cfn-exec-role`
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=["iam:PassRole"],
            resources=["arn:aws:iam::122610492430:role/cdk-hnb659fds-cfn-exec-role-*"]
        ))

        # Permisos adicionales requeridos para despliegue con CDK
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "cloudformation:*",
                "s3:*",
                "sts:AssumeRole",
                "ec2:Describe*",
                "iam:GetRole",
                "iam:ListRoles"
            ],
            resources=["*"]
        ))

        # Permisos adicionales para CloudFormation
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "cloudformation:GetTemplate",
                "cloudformation:DescribeStacks",
                "cloudformation:CreateStack",
                "cloudformation:UpdateStack",
                "cloudformation:DeleteStack",
                "cloudformation:ListStacks",
                "cloudformation:ValidateTemplate"
            ],
            resources=["*"]
        ))

        # Permisos adicionales para IAM
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:AttachRolePolicy",
                "iam:DetachRolePolicy",
                "iam:PutRolePolicy",
                "iam:DeleteRolePolicy",
                "iam:GetRole",
                "iam:ListRoles",
                "iam:PassRole"
            ],
            resources=["*"]
        ))

        # Permisos adicionales para STS
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "sts:AssumeRole",
                "sts:GetCallerIdentity"
            ],
            resources=["*"]
        ))

        # Permisos adicionales para EC2 (opcional)
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "ec2:Describe*",
                "ec2:CreateSecurityGroup",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupIngress"
            ],
            resources=["*"]
        ))

app = App()
GitOpsIAMRole(app, "GitOpsIAMRole")
app.synth()