from setuptools import setup, find_packages
from os import path

# Read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read the contents of your LICENSE file
with open(path.join(this_directory, 'LICENSE.md'), encoding='utf-8') as f:
    license_text = f.read()

# Read the contents of the requirements file and create a list
with open(path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = [line.strip() for line in f if line.strip()]

setup(
    name='exceptbot',
    version='1.0.12',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    url='https://exceptbot.com',
    author='Brian Risk',
    author_email='geneffects@gmail.com',
    description='Exception Logger with AI Suggestions for Django',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=license_text,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: Other/Proprietary License",
    ],
    python_requires='>=3.6',
)