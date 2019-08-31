from setuptools import setup, find_packages

version = __import__('patois').__version__
author = __import__('patois').__author__
author_email = __import__('patois').__email__

req = open('requirements.txt')
requirements = req.readlines()
req.close()

setup(
    name='patois',
    version=version,
    url='https://github.com/henriblancke/patois',
    long_description_markdown_filename='README.md',
    description='NLP toolbox with some handy pre-processing functionality.',
    author=author,
    author_email=author_email,
    packages=find_packages(),
    package_dir={'patois': 'patois'},
    include_package_data=True,
    install_requires=requirements,
    platforms=['any'],
    classifiers=[
        'Programming Language :: Python :: 2.7'
        'Programming Language :: Python :: 3.5'
    ],
    test_suite='tests',
    tests_require=['pytest', 'pytest-cov']
)
