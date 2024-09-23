resource "aws_db_instance" "main_postgresql_db" {
  identifier             = "prod-db"
  engine                 = "postgres"
  engine_version         = "16.3"
  username               = "postgres"
  db_name                = "postgres"
  instance_class         = "db.t3.micro"
  vpc_security_group_ids = [aws_security_group.main_sg.id]
  allocated_storage      = 20
  multi_az               = false
  password               = "postgres123"
  publicly_accessible    = true
  skip_final_snapshot    = true
}

resource "aws_db_instance" "auth_postgresql_db" {
  identifier             = "auth-db"
  engine                 = "postgres"
  engine_version         = "16.3"
  username               = "postgres"
  db_name                = "postgres"
  instance_class         = "db.t3.micro"
  vpc_security_group_ids = [aws_security_group.main_sg.id]
  allocated_storage      = 20
  multi_az               = false
  password               = "postgres123"
  publicly_accessible    = true
  skip_final_snapshot    = true
}