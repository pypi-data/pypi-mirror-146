from setuptools import setup
import pathlib

LICENSE = 'Apache License 2.0'
HERE = pathlib.Path(__file__).parent

setup(name='okra_py_official',
      version='1.1',
      description='Python wrapper for Okra API',
      long_description=(HERE / "README.md").read_text(),
      long_description_content_type="text/markdown",
      url='https://github.com/okraHQ/okra_py',
      author="Okra",
      author_email='tech@okra.ng',
      license=LICENSE,
      install_requires=['requests'],
      packages=['okra_py'],
      )
