# --------------------------
# Provider Configuration
# --------------------------
provider "aws" {
  region = var.aws_region
}

# --------------------------
# Networking - VPC and Subnet
# --------------------------
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr_block

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_subnet" "main" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet_cidr_block
  availability_zone = "${var.aws_region}"

  tags = {
    Name = "${var.project_name}-subnet"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-route-table"
  }
}

resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}

# --------------------------
# ECS Cluster
# --------------------------
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
}

# --------------------------
# ECR Repository
# --------------------------
resource "aws_ecr_repository" "main" {
  name = "${var.project_name}-ecr"
}

# --------------------------
# SSM Parameters
# --------------------------
resource "aws_ssm_parameter" "database_url" {
  name  = "/${var.project_name}/DATABASE_URL"
  type  = "SecureString"
  value = var.database_url
}

resource "aws_ssm_parameter" "secret_key" {
  name  = "/${var.project_name}/SECRET_KEY"
  type  = "SecureString"
  value = var.secret_key
}

# --------------------------
# IAM Role for ECS Task
# --------------------------
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.project_name}-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
      Effect = "Allow"
      Sid = ""
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "ecs_task_execution_role_ssm_read" {
  name = "${var.project_name}-task-execution-role-ssm-read"
  role = aws_iam_role.ecs_task_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = "*"
      }
    ]
  })
}

# --------------------------
# ECS Task Definition
# --------------------------
resource "aws_ecs_task_definition" "main" {
  family                   = "${var.project_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name  = var.project_name
      image = "${aws_ecr_repository.main.repository_url}:latest"
      essential = true

      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
        }
      ]

      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_ssm_parameter.database_url.arn
        },
        {
          name      = "SECRET_KEY"
          valueFrom = aws_ssm_parameter.secret_key.arn
        }
      ]
    }
  ])
}


# --------------------------
# ECS Service
# --------------------------
resource "aws_ecs_service" "main" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.main.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets          = [aws_subnet.main.id]
    assign_public_ip = true
    security_groups  = [aws_security_group.main.id]
  }

  depends_on = [
    aws_iam_role_policy_attachment.ecs_task_execution_role_policy
  ]
}

# --------------------------
# Security Group
# --------------------------
resource "aws_security_group" "main" {
  name        = "${var.project_name}-sg"
  description = "Allow inbound traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow HTTP"
    from_port   = var.container_port
    to_port     = var.container_port
    protocol    = "tcp"
    cidr_blocks = ["192.168.0.7/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
