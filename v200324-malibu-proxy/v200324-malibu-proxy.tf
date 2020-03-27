locals {
  v_tag               = "v200324"
  env                 = "prd"
  ingest_proxy_domain = "${local.env}.dlive.tv"

  aws_iam_instance_profile_arn  = "arn:aws:iam::726332586568:instance-profile/v1111-prd-stream-core-uploader-2018111219382952310000000c"
  aws_iam_instance_profile_name = "v1111-prd-stream-core-uploader-2018111219382952310000000c"

  ingest_proxy_key_name   = "prd-stream-v20200324"
  stream_bastion_key_name = "prd-stream"
  office_cidr             = module.workstation.workstation_ip_cidr
  inner_cidr              = "10.0.0.0/8"
  stream_bastion_dns      = "ec2-3-127-107-78.eu-central-1.compute.amazonaws.com"

  proxy_name_tag = "malibu-proxy"
}

module "workstation" {
  source = "../../modules/http-workstation-ip"
}
# ==================================================[v200324]各个区proxy=================================================

# 5. ingest-proxy @sao paulo
# vpc for multi(if enabled).
module "vpc_saopaulo" {
  source = "../../modules/aws-networking-latest"
  create = true

  cidr = "10.6.0.0/16"
  name = "prd-stream-multi-saopaulo"

  providers = {
    aws = aws.proxy_saopaulo
  }
}

# peer vpc_saopaulo to vpc_frankfurt
# Can't peer when vpc is NOT ready, use `terraform plan -target=module.vpc_saopaulo` to make vpc ready first.
module "vpc_peering_saopaulo_to_frankfurt" {
  source = "github.com/grem11n/terraform-aws-vpc-peering"

  providers   = {
    aws.this = aws.proxy_saopaulo
    aws.peer = aws.core
  }
  this_vpc_id = module.vpc_saopaulo.vpc_id
  peer_vpc_id = "vpc-0e69ca109fd8fd88b"

  auto_accept_peering = true

  tags = {
    Name      = "${local.v_tag}-vpc-peering-saopaulo-to-frankfurt"
    terraform = "true"
  }

}

module "ingest_proxy_saopaulo" {
  # up-stream: Ingest Proxy
  source = "../../modules/stream-multi-rtmp-proxy-v0324"

  # Global
  enabled                       = true
  v_tag                         = local.v_tag
  env                           = local.env
  key_name                      = local.ingest_proxy_key_name
  aws_iam_instance_profile_name = local.aws_iam_instance_profile_name
  monitoring                    = true

  # Networking
  vpc_id           = module.vpc_saopaulo.vpc_id
  subnets          = module.vpc_saopaulo.subnet_public_ids
  workstation_cidr = module.workstation.workstation_ip_cidr
  inner_cidr       = local.inner_cidr

  # Proxy
  name             = local.proxy_name_tag
  domain_name      = local.ingest_proxy_domain
  desired_capacity = 1
  instance_type    = "t2.medium"
  region           = "saopaulo"
  //  user_data        = data.template_file.ingest_proxy_user_data.rendered


  providers = {
    aws = aws.proxy_saopaulo
  }
}
