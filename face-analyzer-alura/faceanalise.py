import json

import boto3

s3 = boto3.resource('s3')
client = boto3.client('rekognition')

def detecta_faces():
    response= client.index_faces(
                CollectionId='faces2',
                DetectionAttributes=['DEFAULT'],
                ExternalImageId='temp',
                Image={
                    'S3Object': {
                        'Bucket': 'fa-imagens-alura-fabs',
                        'Name': '_analise.png',
                    },
                },
            )
    #print('Faces indexed:')
    #for faceRecord in response['FaceRecords']:
    #    print('  Face ID: ' + faceRecord['Face']['FaceId'])
    #    print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
    return response

def cria_lista_faces_detectadas(faces_detectadas):
    faceId_detectadas =[]
    for imagem in range(len(faces_detectadas['FaceRecords'])):
        faceId_detectadas.append(faces_detectadas['FaceRecords'][imagem]['Face']['FaceId'])
    return faceId_detectadas

def compara_imagens(faces_detectadas):
    resultado_comparacao = []
    for idImagem in faces_detectadas:
        resultado_comparacao.append(
            client.search_faces(
                CollectionId='faces2',
                FaceId=idImagem,
                FaceMatchThreshold=80,
                MaxFaces=10
            )
        )
    return  resultado_comparacao

def gera_dados_json(resultado_comparacao):
    dados_json= []
    for face_matches in resultado_comparacao:
        if(len(face_matches.get('FaceMatches'))) >= 1:
            perfil = dict(nome=face_matches['FaceMatches'][0]['Face']['ExternalImageId'],
                          faceMatch=round(face_matches['FaceMatches'][0]['Similarity'], 2))
            dados_json.append(perfil)
    return dados_json

def publica_dados_s3(dados_json):
    arquivo = s3.Object('fa-site-alura-fabs', 'dados.json')
    arquivo.put(Body=json.dumps(dados_json))

def exclui_imagens_colecao(faceId_detectadas):
    client.delete_faces(
        CollectionId='faces2',
        FaceIds=faceId_detectadas
    )

def main(event, context):
    faces_detectadas = detecta_faces()
    faceId_detectadas = cria_lista_faces_detectadas(faces_detectadas)
    resultado_comparacao = compara_imagens(faceId_detectadas)
    dados_json = gera_dados_json(resultado_comparacao)
    publica_dados_s3(dados_json)
    exclui_imagens_colecao(faceId_detectadas)
    print(json.dumps(dados_json, indent=4))

