# Criar o bucket S3
resource "aws_s3_bucket" "bucket_main" {
  bucket = "bucket-greench"  # Nome único para o bucket
  force_destroy = true
}

resource "aws_s3_bucket_ownership_controls" "bucket_main" {
  bucket = aws_s3_bucket.bucket_main.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "bucket_main" {
  bucket = aws_s3_bucket.bucket_main.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "bucket_main" {
  depends_on = [
    aws_s3_bucket_ownership_controls.bucket_main,
    aws_s3_bucket_public_access_block.bucket_main,
  ]

  bucket = aws_s3_bucket.bucket_main.id
  acl    = "public-read"
}

# Output para exibir o nome do bucket após a criação
output "bucket_name" {
  value       = aws_s3_bucket.bucket_main.bucket
  description = "Nome do bucket S3 criado"
}