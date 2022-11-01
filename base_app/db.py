import click
import psycopg2
from flask import g, current_app


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=current_app.config['DATABASE_HOST'],
            database=current_app.config['DATABASE_NAME'],
            user=current_app.config['DATABASE_USERNAME'],
            password=current_app.config['DATABASE_PASSWORD'],
        )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
