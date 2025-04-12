from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# A chave de API será lida da variável de ambiente no Render
W2G_API_KEY = os.environ.get('W2G_API_KEY')
W2G_CREATE_ROOM_URL = "https://api.w2g.tv/rooms/create.json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_room', methods=['POST'])
def create_w2g_room():
    print(f"Valor de W2G_API_KEY ANTES da verificação: '{W2G_API_KEY}'") # Para diagnóstico
    if not W2G_API_KEY:
        return jsonify({'error': 'Chave de API do Watch2Gether não configurada no Render'}), 500

    video_url = request.form.get('video_url')
    if not video_url:
        return jsonify({'error': 'URL do vídeo é obrigatório'}), 400

    payload = {
        "w2g_api_key": W2G_API_KEY,
        "share": video_url
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(W2G_CREATE_ROOM_URL, headers=headers, json=payload)
        response.raise_for_status()
        room_data = response.json()
        return jsonify({'room_url': f"https://w2g.tv/rooms/{room_data['streamkey']}"})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro ao comunicar com a API do Watch2Gether: {e}'}), 500
    except ValueError:
        return jsonify({'error': 'Resposta inválida da API do Watch2Gether'}), 500

@app.route('/test_key')
def test_key():
    api_key = os.environ.get('W2G_API_KEY')
    return jsonify({'api_key': api_key})

if __name__ == '__main__':
    # Não execute o servidor de desenvolvimento do Flask em produção no Render
    pass
    
