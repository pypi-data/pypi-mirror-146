import requests

from .Demotivator import Demotivator
from .Quote import Quote

try:
    version = requests.get(
        'https://gitlab.freedesktop.org/feralcas/vass-core-lib/-/raw/main/vaascorelib/version.txt'
    ).text.splitlines()

    if version[0] != '1.0':
        print(f'[VaasCoreLib] Данная версия библиотеки устарела, обновитесь до v{version[0]} с GitHub',
              f'\nИзменения: {version[1]}')
except requests.exceptions.RequestException:
    print('[VaasCoreLib] Не удалось проверить версию библиотеки на актуальность')

__all__ = (
    'Demotivator',
    'Quote'
)
