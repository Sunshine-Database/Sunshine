from server import app

import click

@click.group()
def sunshine():
    pass

@sunshine.command()
@click.option('--host', default = '127.0.0.1', help = 'Хост для сервера')
@click.option('--port', default = 8000,        help = 'Порт для сервера')
def serve(host, port):
    click.echo(f'Запуск сервера Sunshine Database <{host}:{port}>')
    app.run(
        host = host, 
        port = port
    )
    

@sunshine.command()
def push():
    click.echo('Выполнение команды push')

@sunshine.command()
def deploy():
    click.echo('Выполнение команды deploy')

if __name__ == '__main__':
    sunshine()