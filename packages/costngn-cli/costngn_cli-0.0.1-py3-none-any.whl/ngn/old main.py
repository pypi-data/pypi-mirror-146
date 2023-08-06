import typer
from config.config import *

'''
alpha expected behavior
costngn-cli (default company and account data)
costngn-cli config ->input account data
costngn-cli --show config -> show account/s data (without keys)
costngn-cli AWS ->aws default account data
costngn-cli DO  ->DO default account data
costngn-cli --help ->automatic


'''
#app = typer.Typer()


#@app.command()
def main( what:str):
    #if config => config account
    #else the argument is company(and account name?)
    if what=='config':  
        #typer.run(conf_post())
        typer.echo(f"Hello {what}")

    elif what=='AWS':
        typer.run(conf_get('DefaultNick'))

'''
def hello(name:str):
    typer.echo(f"Hello {name}")


def ngn():
    
    print('go to get')

    conf_get('Jack')


if __name__ == "__main__":
    typer.run(main)

'''

