from setuptools import setup, find_packages

setup(
    name='exceptbot',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=3.0',
        'python-decouple>=3.4',
    ],
    url='https://exceptbot.com',  # Replace with your repository URL
    author='Brian Risk',
    author_email='geneffects@gmail.com',
    description='Exception Logger with AI Suggestions for Django',
)
