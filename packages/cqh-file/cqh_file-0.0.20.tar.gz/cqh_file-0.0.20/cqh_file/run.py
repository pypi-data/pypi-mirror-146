import string
import cqh_file
import click

#ctypes.windll.user32.MessageBoxW(0, msg, title, 1)


class Logger(object):
    def __init__(self, level):
        self.level = level
    
    def info(self, msg):
        self.log('info', msg)
    
    def debug(self, msg):
        self.log("debug", msg)
    
    def warn(self, msg):
        self.log("warn", msg)
    
    def error(self, msg):
        self.info("error", msg)
    
    def log(self, level, msg):
        level_list = ["debug", "info", "warn", "error"]
        def get_level(l):
            l = l.lower()
            if l not in level_list:
                return 0
            return level_list.index(l)
        log_level= get_level(level)
        conf_level = get_level(self.level)
        if log_level >= conf_level:
            click.echo(msg)


@click.group()
def cli():
    pass




@click.command()
@click.option("--port", default=8081)
@click.option("--dir")
@click.option("--timeout", default=60)
def serve(port, dir, timeout):
    click.echo("port:{}".format(port))
    click.echo("dir:{}, timeout:{}".format(dir, timeout))
    from cqh_file import __version__
    click.echo("version:{}".format(__version__))
    from cqh_file.serve import create_app

    create_app(port=port, dir=dir, timeout=timeout)

def parse_time(v):
    if v[-1].isdigit():
        return int(v)
    value, unit = v[:-1], v[-1]
    value = int(value)
    unit_d = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 3600*24
    }
    return unit_d[unit]* value

@click.command()
@click.option("--url")
@click.option("--dir", multiple=True)
@click.option("--sleep", default="300s")
@click.option("--delete", default=1)
@click.option("--level",default="info")
def client(url, dir, sleep, delete, level):
    click.echo("url:{}, dir:{}, sleep:{}, delete:{}, level:{}".format(url,dir, sleep, delete, level))
    sleep = parse_time(sleep)

    logger= Logger(level)
    
    from cqh_file import __version__
    logger.info("version:{}".format(__version__))
    from cqh_file.client import ClientLoop
    loop = ClientLoop(url=url, dir=dir, sleep=sleep, 
    delete=delete,
    logger=logger)
    loop.loop()

cli.add_command(serve)
cli.add_command(client)


if __name__ == "__main__":
    cli()
