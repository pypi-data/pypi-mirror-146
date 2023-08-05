import os
import re
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

install_requires = [
    "numpy", "pandas", "sklearn", "xgboost", "shap", "scipy"
]

setup(
    name='indi',
    version=find_version("indi", "__init__.py"),
    url='https://github.com',
    author='Scott Lundberg',
    author_email='scott.lundberg@microsoft.com',
    description='Causal inference using model disentanglment.',
    packages=find_packages(exclude=['notebooks']),
    install_requires=install_requires
)
