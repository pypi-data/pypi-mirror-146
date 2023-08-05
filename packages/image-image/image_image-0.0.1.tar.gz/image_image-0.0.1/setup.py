from setuptools import setup, find_packages

with open ("readme.md", "r") as f:
    page_description = f.read()

with open ("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = 'image_image',
    version='0.0.1',
    author='Leonardo Alves de Andrade',
    author_email = 'leonardo.andrade@engenharia.ufjf.br',
    description= 'pacote de processamento de imagem teste',
    url= '',
    packages = find_packages(),
    install_requires=requirements,
    python_requires='>=3.0',
)