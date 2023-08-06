from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dio_img_processing",
    version="0.0.1",
    author="Josimar Gabriel R. de Araújo",
    author_email="jgr-araujo@protonmail.com",
    description="Image processing tool.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jgr-araujo/dio-img-processing",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
