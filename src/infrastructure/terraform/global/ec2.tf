resource "aws_instance" "servidor_api" {
  ami           = "ami-0e86e20dae9224db8"  # AMI do Ubuntu em us-east-1
  instance_type = "t2.micro"

  tags = {
    Name = "ServidorAPI"
  }
}

resource "aws_instance" "servidor_receiver" {
  ami           = "ami-0e86e20dae9224db8"  # AMI do Ubuntu em us-east-1
  instance_type = "t2.micro"

  tags = {
    Name = "ServidorRECEIVER"
  }
}

resource "aws_instance" "servidor_auth" {
  ami           = "ami-0e86e20dae9224db8"  # AMI do Ubuntu em us-east-1
  instance_type = "t2.micro"

  tags = {
    Name = "ServidorAUTH"
  }
}

resource "aws_instance" "servidor_rabbit" {
  ami           = "ami-0e86e20dae9224db8"  # AMI do Ubuntu em us-east-1
  instance_type = "t2.micro"

  tags = {
    Name = "ServidorRABBIT"
  }
}

resource "aws_instance" "servidor_dashboard" {
  ami           = "ami-0e86e20dae9224db8"  # AMI do Ubuntu em us-east-1
  instance_type = "t2.micro"

  tags = {
    Name = "ServidorDASHBOARD"
  }
}




