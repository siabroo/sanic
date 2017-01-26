from datetime import datetime, timedelta
from http.cookies import SimpleCookie
from sanic import Sanic
from sanic.response import json, text
from sanic.utils import sanic_endpoint_test
import pytest


# ------------------------------------------------------------ #
#  GET
# ------------------------------------------------------------ #

def test_cookies():
    app = Sanic('test_text')

    @app.route('/')
    def handler(request):
        response = text('Cookies are: {}'.format(request.cookies['test']))
        response.cookies['right_back'] = 'at you'
        return response

    request, response = sanic_endpoint_test(app, cookies={"test": "working!"})
    response_cookies = SimpleCookie()
    response_cookies.load(response.headers.get('Set-Cookie', {}))

    assert response.text == 'Cookies are: working!'
    assert response_cookies['right_back'].value == 'at you'

@pytest.mark.parametrize("httponly,expected", [
        (False, False),
        (True, True),
])
def test_false_cookies(httponly, expected):
    app = Sanic('test_text')

    @app.route('/')
    def handler(request):
        response = text('Cookies are: {}'.format(request.cookies['test']))
        response.cookies['right_back'] = 'at you'
        response.cookies['right_back']['httponly'] = httponly
        return response

    request, response = sanic_endpoint_test(app)
    response_cookies = SimpleCookie()
    response_cookies.load(response.headers.get('Set-Cookie', {}))

    'HttpOnly' in response_cookies == expected

def test_http2_cookies():
    app = Sanic('test_http2_cookies')

    @app.route('/')
    async def handler(request):
        response = text('Cookies are: {}'.format(request.cookies['test']))
        return response

    headers = {'cookie': 'test=working!'}
    request, response = sanic_endpoint_test(app, headers=headers)

    assert response.text == 'Cookies are: working!'

def test_cookie_options():
    app = Sanic('test_text')

    @app.route('/')
    def handler(request):
        response = text("OK")
        response.cookies['test'] = 'at you'
        response.cookies['test']['httponly'] = True
        response.cookies['test']['expires'] = datetime.now() + timedelta(seconds=10)
        return response

    request, response = sanic_endpoint_test(app)
    response_cookies = SimpleCookie()
    response_cookies.load(response.headers.get('Set-Cookie', {}))

    assert response_cookies['test'].value == 'at you'
    assert response_cookies['test']['httponly'] == True
