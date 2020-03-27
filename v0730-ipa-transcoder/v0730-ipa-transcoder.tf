locals {
  v_tag                         = "v0730"
  env                           = "prd"
  domain_name                   = "${local.env}.dlive.tv"

  aws_iam_instance_profile_arn  = "arn:aws:iam::726332586568:instance-profile/v1111-prd-stream-core-uploader-2018111219382952310000000c"
  aws_iam_instance_profile_name = "v1111-prd-stream-core-uploader-2018111219382952310000000c"

  key_name                      = "prd-stream"
  office_cidr                   = "${module.workstation.workstation_ip_cidr}"
  inner_cidr                    = "10.0.0.0/8"

  transcoder_name_tag           = "ipa-transcoder"

  transcoder_instance_type      = "c5.4xlarge"
  transcoder_desired_capacity   = 30
  transcoder_ami                = "ami-0356b6770b4e7be59"
}

module "workstation" {
  source = "../../modules/http-workstation-ip"
}
# ==================================================[v0730]ff-transcoder================================================

# 1. placement_group for transcoders
resource "aws_placement_group" "placement_group" {
  name     = "${local.v_tag}-${local.transcoder_name_tag}-placementgroup"
  strategy = "cluster"
  provider = "aws.core"
}

# 2. transcoder
module "transcoder" {
  source                        = "../../modules/aws-ec2-nlb-asg-transcoder"

  # Global
  v_tag                         = "${local.v_tag}"
  aws_iam_instance_profile_name = "${local.aws_iam_instance_profile_arn}"

  # Networking
  availability_zones            = ["eu-central-1b"] #["eu-central-1a", "eu-central-1b", "eu-central-1c"]
  placement_group_id            = "${aws_placement_group.placement_group.id}"
  vpc_id                        = "vpc-0e69ca109fd8fd88b"
  subnets                       = ["subnet-0feef7a097cd5c205"] # ["subnet-0cbcba12e7e2f0b52", "subnet-0feef7a097cd5c205", "subnet-0610011f42066577b"]

  # sg
  ingress_cidrs                 = [
    {
      from_port   = "80"
      to_port     = "80"
      protocol    = "TCP"
      cidr_blocks = "10.0.0.0/8"
      description = "Open to Inner"
    },
    {
      from_port   = "9000"
      to_port     = "9000"
      protocol    = "TCP"
      cidr_blocks = "10.0.0.0/8"
      description = "Open to Inner"
    },
    {
      rule        = "ssh-tcp"
      cidr_blocks = "10.0.0.0/8"
      description = "SSH"
    },
  ]

  # Auto Scaling
  name                          = "${local.transcoder_name_tag}"
  ami                           = "${local.transcoder_ami}"
  instance_type                 = "${local.transcoder_instance_type}"
  key_name                      = "${local.key_name}"
  desired_capacity              = "${local.transcoder_desired_capacity}"
  associate_public_ip_address   = false
  providers                     = {
    aws = "aws.core"
  }
}