from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='lutstrings',
    version='0.1.3',    
    description='Python package to reorder init strings',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/byuccl/encrypted_ip/tree/main/lutstrings',
    author='Daniel Hutchings',
    author_email='dhutch@dazoo.org',
    license='MIT',
    packages=['lutstrings'],
    install_requires=[],

    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)
