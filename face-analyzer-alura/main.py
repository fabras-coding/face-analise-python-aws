import json

import boto3

s3 = boto3.resource('s3')
client = boto3.client('rekognition')

def cria_collection():
    response = client.create_collection(
        CollectionId='faces2'
    )
    return response

def lista_imagens():
    imagens = []
    bucket = s3.Bucket('fa-imagens-alura-fabs')
    for imagem in bucket.objects.all():
        imagens.append(imagem.key)
    print(imagens)
    return imagens


def indexa_colecao(imagens):

    for i in imagens:
        response = client.index_faces(
            CollectionId='faces2',
            DetectionAttributes=[],
            ExternalImageId=i[:-4],
            Image={
                'S3Object': {
                    'Bucket': 'fa-imagens-alura-fabs',
                    'Name': i,
                },
            },
        )
        print('Faces indexed:')
        for faceRecord in response['FaceRecords']:
            print('  Face ID: ' + faceRecord['Face']['FaceId'])
            print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

print(json.dumps(cria_collection(), indent=4))
imagens = lista_imagens()
indexa_colecao(imagens)