from django.shortcuts import render
import datetime
import requests
import json
from rest_framework_jwt.utils import jwt_encode_handler
from django.views.decorators.http import require_POST
import base64
import hashlib
from werkzeug.utils import secure_filename
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token

cookies = {}

@requires_csrf_token
def home(request):
    if 'user_id' in request.COOKIES:
        user_id = request.COOKIES['user_id']
        if user_id in cookies:
            return render(request, 'main/main_login_completed.html')
        else:
            return render(request, 'main/main.html')
    else:
        return render(request, 'main/main.html')
@requires_csrf_token
def download(request):
    if 'user_id' in request.COOKIES:
        user_id = request.COOKIES['user_id']
        if user_id in cookies:
            data = cookies[user_id]
            if request.method == 'POST':
                if 'send' in request.POST:
                    def generate_jwt_token(login, password, link, url):
                        header = {
                            'alg': 'HS256',
                            'typ': 'JWT'
                        }
                        payload = {
                            'login': login,
                            'password': password,
                            'link': link,
                            'url': url,
                            'exp': 600
                        }
                        header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().strip('=')
                        payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().strip('=')
                        secret = '123456789'
                        signature = hashlib.sha256(f'{header_encoded}.{payload_encoded}{secret}'.encode()).hexdigest()
                        token = f'{header_encoded}.{payload_encoded}.{signature}'
                        return token

                    login = data[0]
                    password = data[1]
                    link = request.POST['input']

                    url = link.split("=")
                    token = generate_jwt_token(login, password, link, url[1])

                    url = f'http://192.168.1.103:8080/download?token={token}'
                    response = requests.post(url)
                    video = response.content
                    with open('static/mp4/video.mp4', 'wb') as f:
                        f.write(video)
                    answer = 'Видео успешно загружено.'
                    video_url = 'http://127.0.0.1:8000/static/mp4/video.mp4'
                    text = 'Скачать видео'
                    return render(request, 'main/download_login_completed.html', {'answer': answer, 'video_url': video_url, 'text': text})
            else:
                return render(request, 'main/download_login_completed.html')
        else:
            return render(request, 'main/download.html')
    else:
        return render(request, 'main/download.html')

@requires_csrf_token
def oauth(request):
    if 'user_id' in request.COOKIES:
        if request.method == 'POST':
            if 'oauth' in request.POST:
                def generate_jwt_token(login, password):
                    header = {
                        'alg': 'HS256',
                        'typ': 'JWT'
                    }
                    payload = {
                        'login': login,
                        'password': password,
                        'exp': 600
                    }
                    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().strip('=')
                    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().strip('=')
                    secret = '123456789'
                    signature = hashlib.sha256(f'{header_encoded}.{payload_encoded}{secret}'.encode()).hexdigest()
                    token = f'{header_encoded}.{payload_encoded}.{signature}'
                    return token

                login = request.POST['login']
                password = request.POST['password']
                token = generate_jwt_token(login, password)

                url = f'http://192.168.1.103:8080/enter?token={token}'
                response = requests.get(url)
                answer = response.text

                if answer == "Успешный вход":
                    response = HttpResponse()
                    user_id = secrets.token_hex(16)
                    response.set_cookie('user_id', user_id)
                    cookies[user_id] = [login, password]
                    return response, render(request, 'main/main_login_completed.html')
                else:
                    text = 'Пользователя с таким email не найдено. Проверьте правильность ввода или зарегистрируйтесь по кнопке ниже'
                    return render(request, 'main/oauth.html', {'text': text})
        else:
            return render(request, 'main/oauth.html')
    else:
        return render(request, 'main/oauth.html')


@requires_csrf_token
def reg(request):
    if 'user_id' in request.COOKIES:
        if request.method == 'POST':
            if 'reg' in request.POST:
                def generate_jwt_token(login, password):
                    header = {
                        'alg': 'HS256',
                        'typ': 'JWT'
                    }
                    payload = {
                        'login': login,
                        'password': password,
                        'exp': 600
                    }
                    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().strip('=')
                    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().strip('=')
                    secret = '123456789'
                    signature = hashlib.sha256(f'{header_encoded}.{payload_encoded}{secret}'.encode()).hexdigest()
                    token = f'{header_encoded}.{payload_encoded}.{signature}'
                    return token


                login = request.POST['login']
                password = request.POST['password']
                token = generate_jwt_token(login, password)

                url = f'http://192.168.1.103:8080/auth?token={token}'
                response = requests.get(url)
                answer = response.text

                if answer == "Регистрация прошла успешно":
                    response = HttpResponse()
                    user_id = secrets.token_hex(16)
                    response.set_cookie('user_id', user_id)
                    cookies[user_id] = [login, password]
                    return response, render(request, 'main/main_login_completed.html')
                else:
                    return render(request, 'main/reg.html')
        else:
            return render(request, 'main/reg.html')
    else:
        return render(request, 'main/reg.html')


@requires_csrf_token
def list(request):
    if 'user_id' in request.COOKIES:
        user_id = request.COOKIES['user_id']
        if user_id in cookies:
            data = cookies[user_id]
            def generate_jwt_token(login, password):
                header = {
                    'alg': 'HS256',
                    'typ': 'JWT'
                }
                payload = {
                    'login': login,
                    'password': password,
                    'exp': 600
                }
                header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().strip('=')
                payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().strip('=')
                secret = '123456789'
                signature = hashlib.sha256(f'{header_encoded}.{payload_encoded}{secret}'.encode()).hexdigest()
                token = f'{header_encoded}.{payload_encoded}.{signature}'
                return token

            login = data[0]
            password = data[1]
            token = generate_jwt_token(login, password)

            url = f'http://192.168.1.103:8080/history?token={token}'
            response = requests.get(url)
            answer = response.text
            if len(answer) == 0:
                return render(request, 'main/list_login_completed.html')
            else:
                urls = answer.split(" ")
                return render(request, 'main/list_login_completed.html', {'urls': urls})
        else:
            return render(request, 'main/list.html')
    else:
        return render(request, 'main/list.html')


