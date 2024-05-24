from flask import Flask, render_template, request
from botocore.exceptions import ClientError
import uuid
import boto3
import logging

app = Flask(__name__)

# Configurar boto3 para se conectar ao DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TabelaDynamoDB')

@app.route('/', methods=['GET', 'POST'])
def form():
    name = None
    email = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        # Gerar um UUID para o item
        item_id = str(uuid.uuid4())

        # Inserir os dados no DynamoDB
        try:
            table.put_item(
                Item={
                    'id': item_id,
                    'name': name,
                    'email': email
                }
            )
            logging.info("Dados inseridos com sucesso no DynamoDB")
        except ClientError as e:
            logging.error(e)
            return "Erro ao inserir dados no DynamoDB", 500

        # Recuperar os dados do DynamoDB para exibição
        try:
            response = table.get_item(
                Key={
                    'id': item_id
                }
            )
            item = response.get('Item')
            if item:
                name = item.get('name')
                email = item.get('email')
        except ClientError as e:
            logging.error(e)
            return "Erro ao recuperar dados do DynamoDB", 500

    return render_template('form.html', name=name, email=email)

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
