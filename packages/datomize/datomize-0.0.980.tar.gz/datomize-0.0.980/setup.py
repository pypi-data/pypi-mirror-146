from setuptools import setup, find_namespace_packages

setup(
    name="datomize",
    version="0.0.980",
    description="Datomize python client",
    packages=find_namespace_packages(),
    install_requires=[
        'requests',
    ],
    url="https://datomize.github.io/datomizeSDK",
    author="Datomize Ltd.",
    author_email="support@datomize.com",
    project_urls={
        "Documentation": "https://datomize.github.io/datomizeSDK",
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
