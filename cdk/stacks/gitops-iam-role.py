# Crear un IAM Role para GitHub Actions (Automáticamente con CDK)

from aws_cdk import App, Stack
from aws_cdk import aws_iam as iam

class GitOpsIAMRole(Stack):
    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear el rol para GitHub Actions
        github_actions_role = iam.Role(
            self, "GitHubActionsRole",
            assumed_by=iam.FederatedPrincipal(
                federated="arn:aws:iam::aws:oidc-provider/token.actions.githubusercontent.com",
                conditions={
                    "StringEquals": {
                        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                    }
                }
            ),
            description="Role for GitHub Actions to deploy with CDK"
        )

        # Asignar permisos necesarios para GitHub Actions
        github_actions_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "cloudformation:*",
                "s3:*",
                "lambda:*",
                "iam:PassRole",
                "apigateway:*",
                "dynamodb:*"
            ],
            resources=["*"]
        ))

app = App()
GitOpsIAMRole(app, "GitOpsIAMRole")
app.synth()