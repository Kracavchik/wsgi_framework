import os
from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    """
    :param folder: templates folder
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    # Открываем шаблон по имени
    file_path = os.path.join(folder, template_name)
    with open(file_path, encoding='utf-8') as f:
        # Читаем
        template = Template(f.read())
    # рендерим шаблон с параметрами
    return template.render(**kwargs)
