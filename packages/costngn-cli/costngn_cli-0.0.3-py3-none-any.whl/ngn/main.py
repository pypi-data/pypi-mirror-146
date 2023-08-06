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

def main(): #it was for a test
    typer.echo("Hello from main")
    typer.run(hello)
'''

app = typer.Typer()

@app.command()
def config():
    typer.echo('Enter below your account access information:')
    typer.echo('You can type anything, it will be saved but it has no effect by now')
    typer.run(conf_post)

@app.command()
def show():
    typer.echo('Show config file contents:')
    typer.run(conf_get)



@app.command()
def hello(name:str):
    typer.echo(f"Hello {name} from hello!")




@app.command()
def aws():
    #print('nothing here by now')
    typer.echo(f"nothing here yet")
    #typer.run(distributor)


'''
def main(what:str= typer.Argument(..., help="Action to take config|AWS")):
    print('passing for main in ct1')
    typer.echo(f"passing for main in ct1")
    #typer.run(distributor)
    typer.run(conf_post())
'''

'''
def ngn():
    
    print('go to get')

    conf_get('Jack')

'''
if __name__ == "__main__":
    app()
    



