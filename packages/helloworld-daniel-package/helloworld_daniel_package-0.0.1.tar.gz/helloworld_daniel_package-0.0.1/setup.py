from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="helloworld_daniel_package",
    version="0.0.1",
    author="daniel_nery",
    author_email="danielpontesnery@gmail.com",
    description="modelo de pacote python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DanielNery/modelo_pacote-python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
)