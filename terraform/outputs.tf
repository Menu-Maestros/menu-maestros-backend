output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "ID of the created Subnet"
  value       = aws_subnet.main.id
}

output "ecr_repository_url" {
  description = "URL of the ECR repository to push the Docker image"
  value       = aws_ecr_repository.main.repository_url
}

output "ecs_cluster_name" {
  description = "Name of the ECS Cluster"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "Name of the ECS Service"
  value       = aws_ecs_service.main.name
}