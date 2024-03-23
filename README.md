## Database preparation:
'''sql
CREATE DATABASE testdb;
'''
Далее создаём таблицы через описанные модели
'''shell
flask db migrate -m 'example message'
flask db upgrade
'''