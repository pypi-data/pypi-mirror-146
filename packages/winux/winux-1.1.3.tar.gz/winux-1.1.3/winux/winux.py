import click, os

name = 'nt'

@click.command()
def clear():
    if os.name == name:
        os.system('cls')

@click.command()
def ls():
    if os.name == name:
        os.system('dir')

@click.command()
@click.argument('fileName')
@click.argument('destination')
def mv(fileName, destination):
    if os.name == name:
        os.system(f'move {fileName} {destination}')

@click.command()
@click.argument('file')
@click.argument('destination')
def cp(file, destination):
    if os.name == name:
        os.system(f'copy {file} {destination}')

@click.command()
@click.argument('file')
@click.option('-rf')
def rm(file, rf):
    if os.name == name:
        if rf == None:
            os.system(f'del {file}')
        else:
            os.system(f'rmdir {file}')

@click.command()
@click.argument('file')
def cat(file):
    if os.name == name:
        os.system(f'type {file}')

@click.command()
def pwd():
    if os.name == name:
        os.system('chdir')

@click.command()
def date():
    if os.name == name:
        os.system('time')

@click.command()
@click.argument('file')
def nano(file):
    if os.name == name:
        os.system(f'edit {file}')

@click.command()
def mem():
    if os.name == name:
        os.system('free')

@click.command()
@click.argument('argument')
def du(argument):
    if os.name == name:
        if argument != None and argument == '-s':
            os.system('chdisk')

@click.command()
@click.argument('process')
def kill(prc):
    if os.name == name:
        os.system(f'taskkill {prc}')

@click.command()
@click.argument('command')
def man(command):
    if os.name == name:
        os.system(f'{command}/?')


@click.command()
@click.argument('name')
def mkdir(name):
    if os.name == name:
        os.syetem(f'md {name}')

#@click.command()
#@click.command('opt')
#def psX(opt):
#    if os.name == name:
#        if opt != None and opt == 'x':
#            os.system('tasklist')
#        else:
#            print('Error. Must pass \"x\" parameter after "ps" command.')