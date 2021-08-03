import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="science_api_examples",
    version="0.1",
    author="ENACOM",
    author_email="pedro.campos@enacom.com.br",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=required,
    packages=setuptools.find_packages(),
    include_package_data=True,
    description="Basic template for science projects"
)
