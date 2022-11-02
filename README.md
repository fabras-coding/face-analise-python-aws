# face-analise-python-aws
Projeto de Estudo de Lambda e S3 - Utilizando serviço Rekognition da AWS com Python para análise de faces humanas.

## Pré Reqs e Passos

Ter dois buckets criados. Um para hospedar o site estático e outro para as imagens. Lembrando que é importante adicionar as policies para que um Bucket possa acessar o outro, e a lambda possa acessar ambos.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::SeuBucket/*"
            ]
        }
    ]
}
```

**Lembre-se de efetuar as alterações no código "index.html", da pasta "fa-site" e no código python, para alterar o nome do bucket e da imagem que ele irá avaliar.**

Configure o Trigger na Lambda para que sempre que cair um arquivo no bucket de imagens com o nome que você configurou no python (no meu caso "_analise.png"), seja disparada a função. A configuração default do Lambda já atende a necessidade do projeto. 

**A função lambda precisa ser criada com a versãom 3.7 do python**

**O código "main.py" só precisa ser executado uma vez. Da sua máquina local**
**O código que deverá subir na Lambda é o faceanalise.py**

**Lembre-se de transformar o bucket onde está a pasta "fa-site" em um host de site estático (isso é feito na última opção dentro de "Properties")

Desenho do projeto
![image](https://user-images.githubusercontent.com/34045906/199373607-b9942fa9-92f0-48ff-a9a4-c41b251d70a9.png)
