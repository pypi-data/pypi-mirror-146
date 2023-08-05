from setuptools import setup, find_packages


with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read()

setup(
    name="Snake-enzoscalassara",
    version="0.0.1",
    author="Enzo Scalassara",
    author_email="enzo_scalassara@hotmail.com",
    description="Snake I did",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enzoscalassara/package-test",
    packages=find_packages(),
    install_requires=requirements,
    python_requires= ">=3.7"
)



