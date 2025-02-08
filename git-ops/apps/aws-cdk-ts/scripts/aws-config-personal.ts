import * as cdk from 'aws-cdk-lib';

const app = new cdk.App();

const awsConfig = {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT, // Se obtiene automáticamente
    region: process.env.CDK_DEFAULT_REGION    // Se obtiene automáticamente
  },
  github: {
    username: '',
    repoName: ''
  }
};

new GitOpsDeploymentStack(app, 'GitOpsStack', {
  env: awsConfig.env,
  description: `Stack de despliegue GitOps para ${awsConfig.github.username}/${awsConfig.github.repoName}`
});

app.synth();
