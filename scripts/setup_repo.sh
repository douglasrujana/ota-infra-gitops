#!/bin/bash

# Nombre del repositorio
REPO_NAME="ota-infra-gitops"

# Crear directorio del repositorio
mkdir $REPO_NAME && cd $REPO_NAME

# Inicializar Git
git init
echo "# $REPO_NAME" > README.md

# Crear carpetas base
mkdir -p .github/workflows cdk/stacks environments/{dev,staging,production} scripts docs

# Crear archivos base
touch .gitignore .pre-commit-config.yaml CODEOWNERS
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore

# Inicializar entorno virtual de Python
python -m venv .venv
source .venv/Scripts/activate

# Instalar AWS CDK en Python
pip install aws-cdk-lib constructs

# Inicializar CDK
cd cdk
cdk init app --language python
cd ..

# Crear workflow de GitHub Actions
cat <<EOF > .github/workflows/deploy.yaml
name: Deploy Infra with GitOps

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install AWS CDK and dependencies
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install -r cdk/requirements.txt
          npm install -g aws-cdk

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: \${{ secrets.AWS_ROLE_TO_ASSUME }}
          aws-region: us-east-1

      - name: Synthesize CDK template
        run: |
          source .venv/bin/activate
          cdk synth

      - name: Deploy infrastructure
        run: |
          source .venv/bin/activate
          cdk deploy --require-approval never
EOF

# Commit inicial
git add .
git commit -m "Inicialización del repositorio GitOps"

echo "✅ Repositorio $REPO_NAME creado y listo para GitOps 🚀"
