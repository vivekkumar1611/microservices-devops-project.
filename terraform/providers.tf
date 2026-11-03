variable "aws_region" {
  description = "AWS region for ECR repositories"
  type        = string
  default     = "eu-north-1"
}

provider "aws" {
  region = var.aws_region
}
