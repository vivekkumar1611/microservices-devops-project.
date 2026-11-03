# Microservices DevOps Project

A learning-ready three-service application for practicing Git/GitHub, Docker, Docker Compose, Jenkins CI, Kubernetes manifests, and Terraform-managed AWS ECR repositories.

## Architecture

- `user-service` — user management demonstration endpoints
- `product-service` — product catalog demonstration endpoints
- `order-service` — order creation and listing

Docker Compose exposes the services on host ports 8001, 8002, and 8003 respectively.

> This is a training project. Data is stored in memory and is lost when a service restarts. It is not production-ready and does not include a persistent database, authentication, payment processing, TLS ingress, or observability stack.

## Repository layout

```text
.
├── services/
│   ├── user-service/
│   ├── product-service/
│   └── order-service/
├── tests/
├── docker-compose.yml
├── jenkins/Jenkinsfile
├── kubernetes/
├── terraform/
├── docs/
├── .github/
├── .gitignore
└── README.md
```

## Requirements

For local development:
- Git
- Docker Engine and Docker Compose plugin (or Docker Desktop)
- Optional: Python 3.12+ and `requirements-dev.txt` to run tests outside containers

For CI/CD:
- Jenkins with Git, Pipeline, and Docker Pipeline plugins
- A Jenkins agent with Docker CLI/daemon access
- GitHub webhook reachability to Jenkins (prefer HTTPS)
- Optional AWS CLI and AWS credentials for ECR publishing

For Kubernetes:
- A Kubernetes cluster and `kubectl`
- A container registry reachable by the cluster

For Terraform:
- Terraform CLI
- AWS credentials configured outside the repository
- AWS permissions to create and manage ECR repositories

## Run locally

```bash
docker compose up --build -d
docker compose ps
```

API documentation:
- User: http://localhost:8001/docs
- Product: http://localhost:8002/docs
- Order: http://localhost:8003/docs

Health endpoints:
- `GET /health` on each service

Example requests:

```bash
curl http://localhost:8001/users
curl -X POST http://localhost:8001/users \
  -H 'Content-Type: application/json' \
  -d '{"name":"Vivek","email":"vivek@example.com"}'

curl -X POST http://localhost:8002/products \
  -H 'Content-Type: application/json' \
  -d '{"name":"Keyboard","description":"Mechanical keyboard","price":499.00}'

curl -X POST http://localhost:8003/orders \
  -H 'Content-Type: application/json' \
  -d '{"user_id":1,"item":"Keyboard","quantity":1}'
```

Stop:

```bash
docker compose down
```

## Run tests

Python 3.12+:

```bash
python -m pip install -r requirements-dev.txt
pytest -q
```

## Git branch workflow

- `main`: stable/release branch
- `develop`: integration branch
- `feature/<name>`: feature work
- `hotfix/<name>`: urgent production correction

Example:

```bash
git checkout -b develop
git push -u origin develop
git checkout -b feature/add-product-endpoint
# make changes
git add .
git commit -m "feat: add product endpoint"
git push -u origin feature/add-product-endpoint
```

Open a Pull Request from `feature/...` into `develop`. Protect `main` and `develop` in GitHub with pull-request review and required CI checks where available.

## Jenkins + GitHub webhook

1. Create a Jenkins Pipeline job using this repository.
2. Configure the branch (`*/develop`) and script path (`jenkins/Jenkinsfile`).
3. Enable **GitHub hook trigger for GITScm polling**.
4. In GitHub, add a webhook pointing to `https://YOUR_JENKINS_HOST/github-webhook/`.
5. Use HTTPS and a webhook secret; restrict Jenkins network access. Do not expose an unsecured Jenkins controller to the public internet.
6. The pipeline runs tests and builds three local Docker images. ECR push is optional and requires Jenkins AWS credentials plus the ECR repository URIs.

## ECR publishing configuration

Set these Jenkins environment variables (or configure them in the job):
- `AWS_REGION` — e.g. `eu-north-1`
- `AWS_ACCOUNT_ID` — your 12-digit AWS account ID

Configure AWS credentials securely on the Jenkins agent using an IAM role or Jenkins Credentials. Never commit AWS keys.

The Jenkinsfile only pushes when `PUSH_TO_ECR=true`. Create the ECR repositories first with Terraform, then run the pipeline with `PUSH_TO_ECR=true`.

## Terraform: create ECR repositories

```bash
cd terraform
terraform init
terraform validate
terraform plan -var="aws_region=eu-north-1"
terraform apply -var="aws_region=eu-north-1"
```

Review the plan before applying. `terraform destroy` deletes the repositories and may fail if they contain images; use only in a disposable learning account.

## Kubernetes deployment

Build and push images to your registry, then edit `kubernetes/*.yaml` image fields to use your image URIs. Apply:

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/
kubectl -n microservices get deployments,services,pods
```

For local testing, you may build images locally and use `imagePullPolicy: IfNotPresent`; ensure the cluster can access those images.

## Security rules

- Never commit `.env`, credentials, access keys, private keys, kubeconfig, Terraform state, or real Kubernetes Secret values.
- Use Jenkins Credentials, AWS IAM roles, or AWS Secrets Manager for secrets.
- Rotate/revoke any credential accidentally committed. Removing a file in a later commit does not erase it from Git history.
- Keep `.env.example` files limited to placeholders.
