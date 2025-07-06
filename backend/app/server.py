print("Inicializando o servidor...")

from flask import Flask, jsonify, request, send_from_directory

import os
from dotenv import load_dotenv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from openai import OpenAI
from enum import Enum
from flask_cors import CORS

class EmailClassification(Enum):
    PRODUCTIVE = 'Productive'
    IMPRODUCTIVE = 'Improductive'

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

def gerarRespostaAutomatica(texto):
    
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "system", "content": "Você é um assistente que classifica emails e sugere respostas."
            },
            {
                "role": "user", "content": f"""
                Classifique o email a seguir como 'Produtivo' ou 'Improdutivo' e, depois, sugira uma resposta.
                IMPORTANTE: responda neste formato, sem variações:

                Categoria: <Produtivo ou Improdutivo>
                Resposta: <sugestão de resposta>

                Email: {texto}
                """
            }
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def categorizacao(resultadoIA):
 
    categoria = None
    resposta = None
  
    linhas = resultadoIA.split('\n')
    for linha in linhas:
        if linha.lower().startswith('categoria'):
            categoria = linha.split(':', 1)[1].strip()
        elif linha.lower().startswith('resposta'):
            resposta = linha.split(':', 1)[1].strip()
            
    return categoria, resposta


def processadorDeTexto(texto):
    tokenizacao = word_tokenize(texto.lower())
    excessoDePalavras = set(stopwords.words('portuguese'))
    filtro = [word for word in tokenizacao if word not in excessoDePalavras]
    textoProcessado = ' '.join(filtro)
    return textoProcessado

app = Flask(__name__)
CORS(app)

print('---SERVIDOR HELLO WORLD ATIVO---')

@app.route("/")
def helloWorld():
    return jsonify(
        {
            "message": "Hello World"
        }
    )

@app.route('/client/<path:path>')
def arquivos_estaticos(path):
    return send_from_directory('client', path)

@app.route('/seutexto', methods=['POST'])


@app.route('/classificar-e-responder', methods=['POST'])
def classificarEmails():
    if 'arquivo' not in request.files:
        return jsonify({'error': 'Arquivo não enviado'}), 400

    arquivo = request.files['arquivo']

    if arquivo.filename == '':
        return jsonify({'error': 'Arquivo vazio'}), 400

    conteudo = arquivo.read().decode('utf-8')
    conteudoFiltrado = processadorDeTexto(conteudo)

    resultadoIA = gerarRespostaAutomatica(conteudoFiltrado)
    

    categoria, resposta = categorizacao(resultadoIA)

    return jsonify({
        'categorizacao': categoria,
        'sugestaoDeResposta': resposta
    })



if __name__ == "__main__":
    #arquivo = 'artigo-5.txt'
    #textoFinal = processadorDeTexto(arquivo)
    #print('Teste do Artigo 5º da CF 1988')
    #print(textoFinal)
    app.run(debug=True)
