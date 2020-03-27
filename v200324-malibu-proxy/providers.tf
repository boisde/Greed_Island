provider "aws" {
  alias = "proxy_london"
  region = "eu-west-2"
}

provider "aws" {
  alias = "core"
  region = "eu-central-1"
}

provider "aws" {
  alias = "proxy_virginia"
  region = "us-east-1"
}

provider "aws" {
  alias = "proxy_oregon"
  region = "us-west-2"
}

provider "aws" {
  alias = "proxy_saopaulo"
  region = "sa-east-1"
}