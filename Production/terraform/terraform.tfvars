# Terraform Variables for Legal Knowledge Platform
# Account: Sandbox (021891619621)
# Region: us-east-2

aws_region     = "us-east-2"
environment    = "sandbox"
project_name   = "legal-knowledge-platform"

# Network Configuration
vpc_cidr                = "10.1.0.0/16"
public_subnet_1_cidr    = "10.1.1.0/24"
public_subnet_2_cidr    = "10.1.2.0/24"
private_subnet_1_cidr   = "10.1.10.0/24"
private_subnet_2_cidr   = "10.1.20.0/24"

# Your IP for SSH access
your_ip_address = "107.197.112.114"

# EC2 Configuration
instance_type = "g4dn.large"

# SSH Key - You need to provide your public key content
# Generate with: ssh-keygen -t rsa -b 4096 -f ~/.ssh/legal-knowledge-platform
# Then copy content of ~/.ssh/legal-knowledge-platform.pub to the line below
public_key_content = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDRWdZboIxt2l6eBn2yrFOCmmcEmYtc+drLF5tiw0ahmVS+Bj0YhljILycxevXewPNJze0KZOTqNug8MILFhvedc/ssG8dQrahFCPVH/auzzbzh0WvwUiBPV7/xXn9CwcLZV/7xqHd7BCwcVLqBetKnkYnHRfQytiM3bkoHPdZUvQytg5LEITpNweQRlu03/xBXZx4RFZSmPoUUjJXoUjz11VPcb2ujlRgIZz+PVKJYmvDQZV8FXuBLs2csHBwcZnRpXwW4cJG9+O8JN9BS6GBlXHOfUDkqzH60oxAhZVutnT2zv//o2C5zdjNywKpqgmU8Ma5CU5PMLOpIOQ3JS3V7KhzE7o48k9asxw55NPPvdwZARSoTEGOVe6ektAyFduX3U9Azg1ioLzZMgI2GqoiDBBc+1mEHag1mwUHZGwe46BRNXoJvjDp/7ekhePj1kXX+w7lcqaZoW/lxUw0bZfHqTeZhhw6lbtx+PekFBBoBgTUBUoZ427Nc/YRxdEW21Qhf+x7xK1GnxkpnVI/5GJxQcQeNkcc3wKeCpzwp7d3rMX2Nxom+vqgCdPp8c+1zhMICWiFpcgpzq8WzeP22udHO4L/MxHs27G2axphhocHZWglZH6FWgCnPzzg5NXuNC3yN9nrAQt+eh7EBuHfUUzel2IduwrWiqZqRklh0e6w2xQ== johnfly@MacBookPro.attlocal.net"
