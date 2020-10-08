from constants import CODE_200, CODE_404
from templator import render


def main_view(request):
    secret = request.data.get('secret', None)
    body = f'Main {secret}'
    return CODE_200, body.encode(encoding='utf-8')


def about_view(request):
    return CODE_200, b'<h1>About</h1>'


def authors_view(request):
    return CODE_200, render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])


def movies_view(request):
    return CODE_200, render('films.html', object_list=[{'name': 'Green mile'}, {'name': 'Schindler list'}])


def view_404(request):
    return CODE_404, b'<h1>NOT FOUND</h1>'


def post_view(request):
    return CODE_200, render('post_form.html')
