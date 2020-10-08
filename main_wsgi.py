from constants import CODE_200, CODE_404
from templator import render


class Response:
    def __init__(self, code, body):
        self.code = code
        self.body = body


class Request:
    def __init__(self, data=None):
        self.data = data or {}


def main_view(request: Request):
    secret = request.data.get('secret', None)
    body = f'Main {secret}'
    return CODE_200, body.encode(encoding='utf-8')


def about_view(request: Request):
    return CODE_200, b'<h1>About</h1>'


def authors_view(request: Request):
    return CODE_200, render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])


def movies_view(request: Request):
    return CODE_200, render('films.html', object_list=[{'name': 'Green mile'}, {'name': 'Schindler list'}])


def url_edge_check(environ):
    url = environ['PATH_INFO']
    if url[-1] != '/':
        url += '/'
    return url


def view_404(request: Request):
    return CODE_404, b'<h1>NOT FOUND</h1>'


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


urls = {
    '/': main_view,
    '/about/': about_view,
    '/authors/': authors_view,
    '/movies/': movies_view
}

middlewares = [
    secret_middleware,
]

application = Application(urls, middlewares)
