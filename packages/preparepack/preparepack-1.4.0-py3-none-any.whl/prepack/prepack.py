import click, os

@click.command(help='Description: Builds directories and files for Python package programmation from template. \n\n Argument:    NAME\tName of your package')
@click.argument('name', required=True)
def prepack(name):
    os.system(f'mkdir {name}_package; cd {name}_package; mkdir {name}')
    with open(f'{name}_package/setup.py', 'w') as set:
        set.write(f'from setuptools import setup\n\nsetup(\n    name=\'{name}\',\n    author=\'\',\n    version=\'0.0.0\',\n    packages=[\'{name}\'])')

    with open(f'{name}_package/{name}/__init__.py', 'w') as ini:
        ini.write(f'from .{name} import *')

    with open(f'{name}_package/{name}/{name}.py', 'w') as file:
        file.write('')

@click.command(help='Description: Builds .tar.gz and .whl for uploading the package on PyPi. This command must be executed in same folder where is located "setup.py" file')
def build():
    os.system('pip install .')
    try:
        os.system('python setup.py sdist bdist_wheel')
    except:
        os.system('python3 setup.py sdist bdist_wheel')

@click.command(help='Description: Starts process for upload of the pakcage on PyPi. This command must be executed in same folder where is located the "dist" folder')
def pypi():
    try:
        os.system('python -m twine upload dist/*')
    except:
        os.system('python3 -m twine upload dist/*')