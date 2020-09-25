from templator import render


class Response:
    def __init__(self, code, body):
        self.code = code
        self.body = body


class Request:
    def __init__(self, data=None):
        self.data = data or {}


def main_view(request: Request) -> Response:
    secret = request.data.get('secret', None)
    body = f'Main {secret}'
    return Response('200 OK', [body.encode(encoding='utf-8')])


def about_view(request: Request) -> Response:
    return Response('200 OK', [b'<h1>About</h1>'])


def authors_view(request: Request) -> Response:
    page = render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    return Response('200 OK', [page.encode(encoding='utf-8')])


def movies_view(request: Request) -> Response:
    page = render('films.html', object_list=[{'name': 'Green mile'}, {'name': 'Schindler list'}])
    return Response('200 OK', [page.encode(encoding='utf-8')])


def url_edge_check(environ):
    url = environ['PATH_INFO']
    if url[-1] != '/':
        url += '/'
    return url


def view_404(request: Request):
    return Response('404 Not Found', [b'<h1>NOT FOUND</h1>'])


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
            response = view(request)
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
