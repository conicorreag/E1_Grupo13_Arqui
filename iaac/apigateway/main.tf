terraform {
  # All providers: https://registry.terraform.io/browse/providers?product_intent=terraform
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-1"
}

data "terraform_remote_state" "ec2" {
  backend = "local"
  config = {
    path = "../ec2/terraform.tfstate"
  }
}

resource "aws_apigatewayv2_api" "my_api" {
  name          = "my-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "my_get_integration" {
  api_id             = aws_apigatewayv2_api.my_api.id
  integration_uri    = "http://${data.terraform_remote_state.ec2.outputs.elastic_ip}"  # Corregido
  integration_method = "ANY"
  integration_type   = "HTTP_PROXY"
}

resource "aws_apigatewayv2_integration" "my_post_integration" {
  api_id             = aws_apigatewayv2_api.my_api.id
  integration_uri    = "http://${data.terraform_remote_state.ec2.outputs.elastic_ip}"  # Corregido
  integration_method = "ANY"
  integration_type   = "HTTP_PROXY"
}

resource "aws_apigatewayv2_route" "my_get_route" {
  api_id             = aws_apigatewayv2_api.my_api.id
  route_key          = "ANY /example"  # Cambia esto según tus necesidades
  target             = "integrations/${aws_apigatewayv2_integration.my_get_integration.id}"
}

resource "aws_apigatewayv2_route" "my_post_route" {
  api_id             = aws_apigatewayv2_api.my_api.id
  route_key          = "POST /example"  # Cambia esto según tus necesidades
  target             = "integrations/${aws_apigatewayv2_integration.my_post_integration.id}"
}

resource "aws_apigatewayv2_stage" "my_stage" {
  api_id      = aws_apigatewayv2_api.my_api.id
  name        = "prod"
  auto_deploy = true
}

output "api_gateway_module" {
  value = aws_apigatewayv2_stage.my_stage.invoke_url
}







