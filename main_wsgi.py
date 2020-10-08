from constants import GET, POST
from views import *
from urls import urls
from request_methods import get_method, post_method


class Response:
    def __init__(self, code, body):
        self.code = code
        self.body = body


class Request:
    def __init__(self, data=None):
        self.data = data or {}


def url_edge_check(environ):
    url = environ['PATH_INFO']
    if url[-1] != '/':
        url += '/'
    return url


def secret_middleware(request):
    request.data['secret'] = 'SECRET'


class Application:

    def __init__(self, urls, middlewares):
        self.urls = urls
        self.middlewares = middlewares

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """
        # сначала в функцию start_response передаем код ответа и заголовки
        # pprint(environ)

        if environ['REQUEST_METHOD'] == POST:
            return post_method(environ, start_response)

        elif environ['REQUEST_METHOD'] == GET and environ['QUERY_STRING'] != '':
            return get_method(environ, start_response)

        else:
            url = url_edge_check(environ)
            request = Request()

            for item in self.middlewares:
                item(request)

            if url in self.urls:
                view = self.urls[url]
                code, page = view(request)
                if type(page) != bytes:
                    response = Response(code, [page.encode(encoding='utf-8')])
                else:
                    response = Response(code, [page])
            else:
                response = view_404(request)
            start_response(response.code, [('Content-Type', 'text/html')])
            # возвращаем тело ответа в виде списка из bite
            return response.body


middlewares = [
    secret_middleware,
]

application = Application(urls, middlewares)
