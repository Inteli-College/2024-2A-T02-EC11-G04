---
title: Deploy na nuvem
sidebar_position: 4
---

---

# **Documentação de Deploy na AWS Usando Terraform**

## **1. Pré-requisitos**
Antes de iniciar o deploy, você deve garantir que os seguintes requisitos estejam atendidos:

- **Conta AWS**: Acesso válido a uma conta AWS.
- **IAM User**: Um usuário IAM com permissões para gerenciar recursos (EC2, S3, RDS, etc.).
- **Terraform**: Instalado e configurado localmente. [Guia de instalação](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- **AWS CLI**: Configurado e autenticado com suas credenciais. [Guia de configuração](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

### **Instalar Terraform e AWS CLI**
1. Instale o Terraform seguindo as instruções: [Terraform CLI Installation](https://learn.hashicorp.com/tutorials/terraform/install-cli).
2. Instale e configure a AWS CLI: [AWS CLI Installation](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

### **Configuração da AWS CLI**
```bash
aws configure
```
Informe:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name (ex: us-east-1)
- Default output format (ex: json)

---

## **2. Arquitetura de Deploy**

- **5 EC2 Instances** (tipo t2.micro)
- **2 RDS Instances** (MySQL)
- **1 Bucket S3**

---

## **3. Arquivos Terraform**

### **3.1. Estrutura do Diretório**
```bash
infrastructure
├──terraform
    ├── ec2.tf
    ├── main.tf
    ├── rds.tf
    ├── s3.tf
    ├── sg.tf
    └── terraform.tfstate
    
```

### **3.4. Arquivo `main.tf`**
Neste arquivo, configuramos todos as variáveis de versionamento.

#### **3.4.1. EC2 Instances**
Aqui criamos 5 instâncias EC2 com o tipo `t2.micro`.
```hcl
resource "aws_instance" "app" {
  count         = var.ec2_count
  ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 AMI
  instance_type = var.instance_type

  tags = {
    Name = "AppInstance-${count.index + 1}"
  }
}
```

#### **3.4.2. RDS Instances**
Aqui criamos 2 bancos de dados RDS Postgres.
```hcl
resource "aws_db_instance" "db" {
  count                   = 2
  allocated_storage        = 20
  engine                   = "postgres"
  instance_class           = "db.t2.micro"
  name                     = var.db_name
  username                 = var.db_username
  password                 = var.db_password
  parameter_group_name     = "default.mysql8.0"
  skip_final_snapshot      = true
  publicly_accessible      = false

  tags = {
    Name = "RDSInstance-${count.index + 1}"
  }
}
```

#### **3.4.3. S3 Bucket**
Aqui criamos um bucket S3 para armazenar dados.
```hcl
resource "aws_s3_bucket" "bucket_main" {
  bucket = "bucket_greench"

}
```

---

## **4. Deploy com Terraform**

### **4.1. Inicializar o Terraform**
Este comando irá baixar os provedores e preparar o ambiente:
```bash
terraform init
```

### **4.2. Visualizar o plano**
Você pode visualizar o que será criado antes de aplicar:
```bash
terraform plan
```

### **4.3. Aplicar o plano**
Para iniciar o deploy da infraestrutura na AWS:
```bash
terraform apply
```
Digite "yes" quando solicitado para confirmar a criação dos recursos.

---

## **5. Monitoramento e Acesso**

### **5.1. Verificar as instâncias EC2**
Após o deploy, você pode verificar as instâncias EC2 pela AWS Management Console ou diretamente pelas saídas do Terraform, que mostram os IPs públicos.

Para conectar-se via SSH a uma das instâncias EC2, use o seguinte comando (substitua `<public_ip>` pelo IP retornado pelo output):
```bash
ssh -i /path/to/your-key.pem ec2-user@<public_ip>
```

### **5.2. Acessar o RDS**
Você pode acessar o banco de dados RDS com as credenciais definidas no arquivo do RDS. O endpoint RDS será exibido nas saídas do Terraform.

---

## **6. Encerramento**

### **6.1. Destruir a infraestrutura**
Para remover toda a infraestrutura criada, execute o comando abaixo. Isso removerá todas as instâncias EC2, RDS e o bucket S3:
```bash
terraform destroy
```
Digite "yes" para confirmar a destruição.

---

## **7. Considerações Finais**
Este guia fornece uma base sólida para o deploy de nossa infraestrutura AWS usando Terraform. Dependendo das necessidades específicas do projeto, essa estrutura pode ser expandida para incluir mais serviços, como Elastic Load Balancing (ELB), Auto Scaling, VPCs, entre outros.
