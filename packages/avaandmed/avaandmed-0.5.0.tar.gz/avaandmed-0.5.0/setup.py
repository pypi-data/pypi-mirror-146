from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='avaandmed',
    version='0.5.0',
    description='Python library for Avaandmed(Open Data) portal API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Michanix/avaandmed-py',
    author='Mihhail Matišinets',
    author_email='mihhail.matisinets@gmail.com',
    install_requires=[
        'requests>=2.25',
        'pydantic>=1.8'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.6, <4',
)
