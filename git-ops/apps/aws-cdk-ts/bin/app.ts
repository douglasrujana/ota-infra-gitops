import * as cdk from 'aws-cdk-lib';
import { GitOpsDeploymentStack } from '../lib/gitops-stack';
import * as dotenv from 'dotenv'; // Importa dotenv

// Carga las variables de entorno desde el archivo .env
dotenv.config();

const app = new cdk.App();

const awsConfig = {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION
  },
  github: {
    // Usa process.env para acceder a las variables definidas en .env
    username: process.env.GITHUB_USERNAME || 'pinkfloyd', // Default value if not set
    repoName: process.env.GITHUB_REPO_NAME || 'dark_side_of_the_moon' // Default value if not set
  }
};

new GitOpsDeploymentStack(app, 'GitOpsStack', {
  env: awsConfig.env,
  description: `Stack de despliegue GitOps para ${awsConfig.github.username}/${awsConfig.github.repoName}`
});

app.synth();