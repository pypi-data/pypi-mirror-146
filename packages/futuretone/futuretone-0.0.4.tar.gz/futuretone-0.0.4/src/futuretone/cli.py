import typer
from pathlib import Path
from .config import get_config, ValidationError
from .twitch import FutureToneIntegrationBot

app = typer.Typer()


@app.command()
def todo():
    """Work in Progress"""
    # TODO
    return 'This is not done yet ;)'


@app.command()
def twitch_bot(config_file: Path = typer.Option('config.ini', '--config',
                                                exists=True,
                                                file_okay=True,
                                                dir_okay=False,
                                                writable=False,
                                                readable=True,
                                                resolve_path=True),
               verbose: int = typer.Option(0, '--verbose', '-v', count=True)):
    try:
        settings = get_config(config_file)
    except FileNotFoundError as ex:
        typer.echo(ex, err=True)
        typer.echo('Please refer to "https://rentry.co/mikuslow_strimer" for more information.')
        raise typer.Exit()
    except ValidationError as ex:
        typer.echo(ex, err=True)
        typer.echo('Please refer to "https://rentry.co/mikuslow_strimer" for more information.')
        raise typer.Exit()

    if verbose > 0:
        settings.global_.verbose = verbose

    try:
        bot = FutureToneIntegrationBot(settings)
        bot.run()
    except Exception as ex:
        typer.echo(ex, err=True)
        typer.echo('Please refer to "https://rentry.co/mikuslow_strimer" for more information.')


if __name__ == '__main__':
    app()
