locals {
  gen_file = "${local.v_tag}_${local.env}_stream_multi_saopaulo_ingest_proxy"
}

# For ansible
data "template_file" "part1" {
  template = file("${path.module}/templates/for_ansible_part1.tpl")

  count = 1

  vars = {
    #	ingest_proxy              = "${element(module.ingest_proxy.public_ip_list, count.index)}"
    ingest_proxy_dns          = element(module.ingest_proxy_saopaulo.dns_list, count.index)
    ingest_proxy_instance_id  = element(module.ingest_proxy_saopaulo.instance_id_list, count.index)
    ingest_proxy_eip_alloc_id = element(module.ingest_proxy_saopaulo.eip_alloc_id_list, count.index)
    ingest_proxy_private_ip   = element(module.ingest_proxy_saopaulo.private_ip_list, count.index)
    ingest_proxy_public_ip    = element(module.ingest_proxy_saopaulo.public_ip_list, count.index)
  }
}

data "template_file" "all" {
  template = file("${path.module}/templates/for_ansible_all.tpl")

  vars = {
    part1    = join("\n", data.template_file.part1.*.rendered)
    region   = "saopaulo"
    env      = local.env
    key_name = local.ingest_proxy_key_name
    v_tag    = local.v_tag
  }
}

#output "for_ansible_all" {
#  value = "${data.template_file.all.rendered}"
#}

resource "random_id" "always" {
  keepers = {
    tm = timestamp()
  }

  byte_length = 8
}

# gen file under "as/tf_gen/<env>/"
resource "null_resource" "ingest_proxy_hosts" {
  triggers = {
    template_rendered = data.template_file.all.rendered
    ren_gen_always    = random_id.always.hex
  }

  provisioner "local-exec" {
    command = "echo '${ data.template_file.all.rendered }' > '${path.module}/../../../as/tf_gen/${local.env}/${local.gen_file}'"
  }
}
