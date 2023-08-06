import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='hello_world_ocr',
    version='1.0.1',
    license='MIT',
    description="Hello world test for uploading pypi packages",
    long_description=README, 
    long_description_content_type="text/markdown",
    author="Wendell Hom",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/wendell-hom',
    keywords='example project',
    install_requires=[
          'pytesseract',
		  'numpy'
      ],
)
