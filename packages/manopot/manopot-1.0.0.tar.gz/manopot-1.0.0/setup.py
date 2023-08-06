from setuptools import setup


def readme_file_contents():
    with open('README.rst') as readme_file:
        data = readme_file.read()
    return data


setup(
    name='manopot',
    version='1.0.0',
    description='Simple TCP HoneyPot',
    long_description=readme_file_contents(),
    author='Apurv Goyal',
    author_email='apurv.goyal01@gmail.com',
    license='MIT',
    packages=['manopot'],
    zip_safe=False,
    install_requires=[]
)