from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="processamento_imagem_bz",
    version="0.0.1",
    author="Marcelo Goulart Lima",
    author_email="glima.marcelo@gmail.com",
    description="Projeto DIO - processamento de imagens com Python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glima-marcelo/Projetos_DIO/tree/master/Python/processamento-imagem-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
