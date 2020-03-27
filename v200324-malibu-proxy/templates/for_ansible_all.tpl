[balancer]
${part1}

[all:vars]
ansible_ssh_private_key_file=~/${key_name}.pem
ansible_user=ubuntu
region=${region}
env_region_tag=${env}_${region}
v_tag=${v_tag}