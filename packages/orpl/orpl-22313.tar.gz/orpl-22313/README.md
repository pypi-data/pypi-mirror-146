<h1 align="center">OpenRELib</h1>
<p align="center">
    <img alt="Made with Python" src="https://img.shields.io/badge/Made%20with-Python-%23FFD242?logo=python&logoColor=white">
    <blockquote>Форк simpledemotivators с багфиксами</blockquote>



## Установка
1) Стабильная версия через GitHub: 
   
   ```sh
   pip3 install https://github.com/Daemon-RE/openre-pylib/archive/main/openre-pylib.zip --upgrade
   ```


На Windows: pip

На Linux/MacOS - pip3

### Примеры использования
1. Demotivator() - создает простой демотиватор с дефолтным шаблоном.
```python
from orpl import Demotivator

dem = Demotivator('test', '123') # 2 строчки
dem.create('filename.jpg') # Название изображения, которое будет взято за основу демотиватора
```

2. Quote() - создает цитату
```python 
from orpl import Quote

a = Quote('text', "name")
a.create('filename.png') # Файл аватарки юзера, сохраняет с названием qresult.jpg
```

### Документация
* [Demotivator() - подробная документация](./docs/demotivator.md)
* [Quote() - подробная документация](./docs/quote.md)
* [Возможные ошибки](./docs/errors.md)
