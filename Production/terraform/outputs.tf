# Outputs for Legal Knowledge Platform Infrastructure

output "account_id" {
  description = "AWS Account ID"
  value       = data.aws_caller_identity.current.account_id
}

output "region" {
  description = "AWS Region"
  value       = var.aws_region
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value = {
    subnet_1 = aws_subnet.public_1.id
    subnet_2 = aws_subnet.public_2.id
  }
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value = {
    subnet_1 = aws_subnet.private_1.id
    subnet_2 = aws_subnet.private_2.id
  }
}

output "nat_gateway_ids" {
  description = "IDs of the NAT Gateways"
  value = {
    nat_1 = aws_nat_gateway.nat_1.id
    nat_2 = aws_nat_gateway.nat_2.id
  }
}

output "elastic_ip_addresses" {
  description = "Elastic IP addresses for NAT Gateways"
  value = {
    nat_1 = aws_eip.nat_1.public_ip
    nat_2 = aws_eip.nat_2.public_ip
  }
}

output "security_group_ids" {
  description = "Security Group IDs"
  value = {
    alb_sg = aws_security_group.alb.id
    ec2_sg = aws_security_group.ec2.id
  }
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "alb_arn" {
  description = "ARN of the Application Load Balancer"
  value       = aws_lb.main.arn
}

output "alb_zone_id" {
  description = "Zone ID of the Application Load Balancer"
  value       = aws_lb.main.zone_id
}

output "key_pair_name" {
  description = "Name of the EC2 Key Pair"
  value       = aws_key_pair.main.key_name
}

output "ami_id" {
  description = "AMI ID for EC2 instances"
  value       = local.ami_id
}

output "availability_zones" {
  description = "Availability zones used"
  value = {
    az_1 = local.az_1
    az_2 = local.az_2
  }
}

# Helpful commands for next steps
output "ec2_launch_command" {
  description = "Command to launch EC2 instance"
  value = <<-EOT
aws ec2 run-instances \
  --image-id ${local.ami_id} \
  --instance-type ${var.instance_type} \
  --key-name ${aws_key_pair.main.key_name} \
  --security-group-ids ${aws_security_group.ec2.id} \
  --subnet-id ${aws_subnet.private_1.id} \
  --no-associate-public-ip-address \
  --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":100,"VolumeType":"gp3"}}]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=${var.project_name}-instance},{Key=Project,Value=${var.project_name}}]'
EOT
}

output "ssh_command_template" {
  description = "Template for SSH command (replace INSTANCE_IP)"
  value       = "ssh -i ${aws_key_pair.main.key_name}.pem ubuntu@INSTANCE_PRIVATE_IP"
}

output "cost_estimate" {
  description = "Monthly cost estimate"
  value = {
    nat_gateways = "$45/month (2 x $22.50)"
    alb         = "$17/month"
    data_transfer = "$5/month"
    total_vpc   = "$67/month"
    ec2_instance = "$144/month (g4dn.xlarge Spot) or $360/month (On-Demand)"
  }
}

# Add data source for account ID
data "aws_caller_identity" "current" {}