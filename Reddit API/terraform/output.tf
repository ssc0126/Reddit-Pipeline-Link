# Output hostname of Redshift
output "redshift_cluster_hostname" {
  description = "ID of the Redshift instance"
  value       = aws_redshift_cluster.redshift_cluster.endpoint
}


# Output Redshift username
output "redshift_username" {
    description = "Username of Redshift cluster"
    value = aws_redshift_cluster.redshift_cluster.master_username
}



# Output Account ID of AWS
data "aws_caller_identity" "current" {}
output "account_id" {
  value = data.aws_caller_identity.current.account_id
}


#Output S3 bucket name
output "s3_bucket_name" {
    description = "S3 Bucket name"
    value = var.s3_bucket
}