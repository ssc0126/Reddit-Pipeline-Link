terraform {
    required_version = ">= 1.2.7"

    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 4.26"
        }
    }
}


provider "aws" {
    region = "us-east-1"
}


#https://rhuaridh.co.uk/blog/redshift-terraform-example.html

resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier = "redshift-cluster-2"
  database_name      = "test"
  master_username    = "user2"
  master_password    = var.master_password
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  publicly_accessible = "true"

  skip_final_snapshot = true
}



# Create Role for Redshift cluster to read data from S3
resource "aws_iam_role" "redshift_role" {
  name = "Reading_S3"
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"]
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
        "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole"
            ],
            "Principal": {
                "Service": [
                    "redshift.amazonaws.com"
                ]
            }
        }
    ]
  })
}

resource "aws_s3_bucket" "reddit_bucket" {
  bucket = var.s3_bucket
}
