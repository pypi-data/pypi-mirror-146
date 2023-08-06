from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing2",
    version="0.0.1",
    author="Davi H.",
    author_email="davi.henrique.lima01@gmail.com",
    description="My short description",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Davi-dev-C/package-template",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
