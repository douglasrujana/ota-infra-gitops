import * as cdk from 'aws-cdk-lib';

const app = new cdk.App();

// Reemplaza estos valores con tus datos
const awsConfig = {
  env: {
    account: '123456789012', // Tu ID de cuenta AWS
    region: 'us-east-1'      // Tu región preferida
  },
  github: {
    orgName: 'tu-organizacion',    // Nombre de tu organización en GitHub
    repoName: 'tu-repositorio'     // Nombre de tu repositorio
  }
};

new GitOpsDeploymentStack(app, 'GitOpsStack', {
  env: awsConfig.env,
  description: `Stack de despliegue GitOps para ${awsConfig.github.orgName}/${awsConfig.github.repoName}`
});

app.synth();
