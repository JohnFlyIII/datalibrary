# Temporary version without NAT Gateways
# This puts EC2 instances in public subnets temporarily

# Comment out NAT Gateway related resources by adding this file
# and renaming main.tf to main.tf.backup

# Then run: terraform plan
# This will show it wants to destroy the failed EIPs and create instances in public subnets instead