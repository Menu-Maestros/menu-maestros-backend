# AWS region
variable "aws_region" {
  description = "The AWS region where resources will be created."
  type        = string
  default     = "us-east-2"
}

# Project name for naming resources
variable "project_name" {
  description = "The name of the project, used for naming resources."
  type        = string
  default     = "menu-maestros-backend"
}

# Docker image and container port
variable "container_image" {
  description = "The Docker image URL to deploy on ECS."
  type        = string
}

variable "container_port" {
  description = "The port the container will expose."
  type        = number
  default     = 8000
}

# SSM Parameters for environment variables
variable "database_url" {
  description = "The database URL used by the application."
  type        = string
}

variable "secret_key" {
  description = "The secret key for the application."
  type        = string
}

# VPC configuration variables
variable "vpc_cidr_block" {
  description = "The CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr_block" {
  description = "The CIDR block for the subnet."
  type        = string
  default     = "10.0.1.0/24"
}

variable "key_pair_name" {
  description = "The EC2 Key Pair for SSH access (if needed)."
  type        = string
}
