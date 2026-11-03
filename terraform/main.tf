locals {
  services = toset(["user-service", "order-service", "product-service"])
}

resource "aws_ecr_repository" "service" {
  for_each             = local.services
  name                 = "microservices-${each.key}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Project     = "microservices-devops-project"
    Environment = "learning"
    ManagedBy   = "Terraform"
  }
}
