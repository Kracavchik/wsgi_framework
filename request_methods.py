def parse_input_data(data: str):
    result = {}
    if data:
        # делим параметры через &
        params = data.split('&')
        for item in params:
            # делим ключ и значение через =
            k, v = item.split('=')
            result[k] = v
    return result


def get_method(environ, start_response):
    """
    :param environ: словарь данных от сервера
    :param start_response: функция для ответа серверу
    """
    # получаем параметры запроса
    query_string = environ['QUERY_STRING']
    print(query_string)
    # превращаем параметры в словарь
    request_params = parse_input_data(query_string)
    print(request_params)
    start_response('200 OK', [('Content-Type', 'text/html')])

    return [b"I'm GET answer!"]


def get_wsgi_input_data(env) -> bytes:
    # получаем длину тела
    content_length_data = env.get('CONTENT_LENGTH')
    # приводим к int
    content_length = int(content_length_data) if content_length_data else 0
    # считываем данные если они есть
    data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
    return data


def parse_wsgi_input_data(data: bytes) -> dict:
    result = {}
    if data:
        # декодируем данные
        data_str = data.decode(encoding='utf-8')
        # собираем их в словарь
        result = parse_input_data(data_str)
    return result


def post_method(environ, start_response):
    """
    :param environ: словарь данных от сервера
    :param start_response: функция для ответа серверу
    """
    # получаем данные
    data = get_wsgi_input_data(environ)
    # превращаем данные в словарь
    data = parse_wsgi_input_data(data)
    print(data)
    start_response('200 OK', [('Content-Type', 'text/html')])

    return [b"I'm POST answer!"]
