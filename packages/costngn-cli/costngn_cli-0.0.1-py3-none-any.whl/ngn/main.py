import typer
from ngn.config.config import *

'''
alpha expected behavior
costngn-cli (default company and account data)
costngn-cli config ->input account data
costngn-cli --show config -> show account/s data (without keys)
costngn-cli AWS ->aws default account data
costngn-cli DO  ->DO default account data
costngn-cli --help ->automatic

#app = typer.Typer()
#@app.command()


def main(): #it was for a test
    typer.echo("Hello from main")
    typer.run(hello)
'''
def hello(name:str):
    typer.echo(f"Hello {name} from hello")





def main():
    print('passing for main in ct1')
    typer.echo(f"passing for main in ct1")
    typer.run(distributor)


def distributor(what:str= typer.Argument(..., help="Action to take config|AWS")):
    #print('Printing what from distributor on same file:',what)
    typer.echo(f"Printing what from distributor on same file: {what}")
    #typer.echo(f"Huy {name}")
    if what=='config':
        typer.echo('go to config')
        #typer.run(conf_post)
    elif what=='AWS':
        typer.echo('go to AWS account data')
    else:
        typer.echo('invalid option')
    





'''
def ngn():
    
    print('go to get')

    conf_get('Jack')


if __name__ == "__main__":
    typer.run(main)

'''

