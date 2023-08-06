from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="wagner_dio_image_processing",
    version="0.0.1",
    author="wagner trindade",
    author_email="wagner.d.trindade@gmail.com",
    description="image processing python project example",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wagnerdtrindade/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8'
)