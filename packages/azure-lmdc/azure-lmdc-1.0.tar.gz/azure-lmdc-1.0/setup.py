from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

# This call to setup() does all the work
setup(
    name="azure-lmdc",
    version="1.0",
    description="Esta biblioteca tem como objetivo generalizar funções da integração entre Azure e Python utilizando o SDK do Azure",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="LMDC-UFF",
    author_email="opensource@lmdc.uff.br",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["azure_lmdc"],
    include_package_data=True,
    install_requires=["azure-identity==1.8.0", "azure-storage-file-datalake==12.6.0"],
    entry_points={
        "console_scripts": [
            "azure-lmdc=azure_lmdc.demo:main",
        ]
    },
)