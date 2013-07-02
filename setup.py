import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'flask',
    'Flask-SQLAlchemy',
    'pbkdf2',
]

setup(name='taskplanner',
      version='0.1',
      author='Jack Spenser',
      author_email='jack.spenser@gmx.us',
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      )