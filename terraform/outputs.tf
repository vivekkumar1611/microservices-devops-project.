output "ecr_repository_urls" {
  description = "ECR repository URLs for the microservices"
  value       = { for name, repo in aws_ecr_repository.service : name => repo.repository_url }
}
