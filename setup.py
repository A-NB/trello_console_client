import setuptools  
  
with open("README.md", "r") as fh:  
    long_description = fh.read()  
setuptools.setup(  
    name="trello_client-basics-api-A-NB",
    version="0.0.1",
    author="A-NB",
    author_email="bel-an510@yandex.ru",
    description="Allows you to manage YOUR WORKSPACES from the console on the website https://trello.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/A-NB/trello_console_client",
    packages=setuptools.find_packages(),
    classifiers=[ "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',)