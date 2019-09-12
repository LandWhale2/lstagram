import dj_database_url


...

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

...

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgesql_psycopg2',
        'NAME' : 'lowell',
        'USER' : 'name',
        'PASSWORD' : '',
        'HOST' : 'locallhost',
        'PORT' : '',
    }
}
...

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)