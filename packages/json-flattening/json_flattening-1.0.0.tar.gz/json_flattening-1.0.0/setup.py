from setuptools import setup, find_packages

classifiers =[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent']


setup(
    name='json_flattening',
    version='1.0.0',
    author='Rahul Goel',
    description = 'Package to flatten json Data',
    long_description_content_type='text/markdown',
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    license='MIT',
    packages=find_packages(),
    classifiers = classifiers,
    keywords='json flatten',
    install_requires=[
          'pandas','numpy'
      ],

)