from aws_cdk import core
from stacks.gitops_iam_role import GitOpsIAMRole

app = core.App()
GitOpsIAMRole(app, "GitOpsIAMRoleStack")
app.synth()
