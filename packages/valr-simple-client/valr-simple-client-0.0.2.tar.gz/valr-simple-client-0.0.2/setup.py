import setuptools
from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='valr-simple-client',
    version='0.0.2',
    description='VALR API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development',
    ],
    install_requires=['requests', 'python-dotenv'],
    keywords=['python', 'package', 'valr', 'crypto', 'api', 'rest', 'client'],
    url='https://github.com/Moon-developer/Valr-simple-client',
    author='Marco Fernandes',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.8'
)
