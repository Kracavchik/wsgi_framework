from views import *
from request_methods import get_method

urls = {
    '/': main_view,
    '/about/': about_view,
    '/authors/': authors_view,
    '/movies/': movies_view,
    '/send/': post_view,
}