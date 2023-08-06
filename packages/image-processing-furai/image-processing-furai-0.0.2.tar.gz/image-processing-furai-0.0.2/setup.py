from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image-processing-furai",
    version="0.0.2",
    author="Furaime",
    author_email="louan.carvalho@gmail.com",
    description="Image processing package to resize and analize images and histogram",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Furaime/image_processing",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)