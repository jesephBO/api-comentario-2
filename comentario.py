import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    
    nombre_tabla = os.environ["TABLE_NAME"]
    nombre_bucket = os.environ["BUCKET_NAME"]
    
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    
    # 1. Guardar en DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response_dynamo = table.put_item(Item=comentario)
    
    # 2. Guardar en bucket S3 con estrategia push
    s3 = boto3.client('s3')
    nombre_archivo = f"comentario_{tenant_id}_{uuidv1}.json"
    
    response_s3 = s3.put_object(
        Bucket=nombre_bucket,
        Key=nombre_archivo,
        Body=json.dumps(comentario),
        ContentType='application/json'
    )
    
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response_dynamo': response_dynamo,
        'response_s3': response_s3
    }