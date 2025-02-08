import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

export class GitOpsDeploymentStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Crear rol de IAM para GitHub Actions
    const gitopsRole = new iam.Role(this, 'GitOpsDeploymentRole', {
      assumedBy: new iam.AccountPrincipal(this.account),
      description: 'Rol para despliegues de GitOps desde GitHub Actions'
    });

    // Políticas para despliegue de CloudFormation
    gitopsRole.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        // Permisos para despliegue de CloudFormation
        'cloudformation:CreateStack',
        'cloudformation:UpdateStack',
        'cloudformation:DeleteStack',
        'cloudformation:DescribeStacks',
        'cloudformation:ListStacks',
        
        // Permisos para gestión de recursos
        'cloudformation:CreateChangeSet',
        'cloudformation:ExecuteChangeSet',
        'cloudformation:GetTemplateSummary',

        // Permisos para servicios adicionales
        's3:GetObject',
        's3:PutObject',
        'iam:PassRole'
      ],
      resources: ['*']
    }));

    // Política de acceso mínimo para implementaciones
    const gitopsManagedPolicy = new iam.ManagedPolicy(this, 'GitOpsManagedPolicy', {
      description: 'Política de permisos mínimos para despliegues de GitOps'
    });

    gitopsManagedPolicy.addStatements(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          'cloudformation:ValidateTemplate',
          'cloudformation:ListStackResources',
          'cloudformation:GetStackPolicy'
        ],
        resources: ['*']
      })
    );

    gitopsRole.addManagedPolicy(gitopsManagedPolicy);

    // Exportar el ARN del rol para uso en GitHub Actions
    new cdk.CfnOutput(this, 'GitOpsRoleArn', {
      value: gitopsRole.roleArn,
      description: 'ARN del rol de GitOps para despliegues de GitHub Actions'
    });
  }
}
