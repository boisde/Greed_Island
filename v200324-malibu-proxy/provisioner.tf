resource "null_resource" "scp_ansible_dir" {
  triggers = {
//    scp_ansible_dir = random_id.always.hex
  }

  provisioner "file" {
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/${local.stream_bastion_key_name}.pem")
      host        = local.stream_bastion_dns

      timeout = "3m"
    }

    # Copies the "as" folder to "~/as"
    source      = "${path.module}/../../../as"
    destination = "~"
  }

  depends_on = [null_resource.ingest_proxy_hosts]
}

resource "null_resource" "run_ansible_playbook_for_ingest_proxy" {
  triggers = {
//    run_ansible_playbook_for_ingest_proxy = random_id.always.hex
  }

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/${local.stream_bastion_key_name}.pem")
      host        = local.stream_bastion_dns
    }

    inline = [
      "cd ~/as/",
      "export ANSIBLE_HOST_KEY_CHECKING=False",

      "echo ansible-playbook -i tf_gen/${local.env}/${local.gen_file} play_ingest_proxy.yml --diff -e 'ansible_python_interpreter=/usr/bin/python3' -e 'env=${local.env}'",
      "ansible-playbook -i tf_gen/${local.env}/${local.gen_file} play_ingest_proxy.yml --diff -e 'ansible_python_interpreter=/usr/bin/python3' -e 'env=${local.env}'",
    ]
  }

  depends_on = [null_resource.scp_ansible_dir]
}
