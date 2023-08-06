# python setup.py develop
from setuptools import setup


CLASSIFIERS = """\
License :: OSI Approved
Programming Language :: Python :: 3.10 :: or higher
Topic :: Software Development
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

DISTNAME = 'complex_number'
AUTHOR = 'Enzo Baraldi'
# AUTHOR_EMAIL = ""
DESCRIPTION = 'This is a simple complex number python package.'
KEYWORDS = ["python", "python3", "python3.10", "complex number", "complex numbers"]
LICENSE = 'MIT'
README = 'This is a simple complex number python package.'

VERSION = '0.1.0'
ISRELEASED = False

PYTHON_MIN_VERSION = '3.10'
# PYTHON_MAX_VERSION = '3.10'
# PYTHON_REQUIRES = f'>={PYTHON_MIN_VERSION}, <= {PYTHON_MAX_VERSION}'
PYTHON_REQUIRES = f">={PYTHON_MIN_VERSION}"

INSTALL_REQUIRES = []

PACKAGES = [
    'complex_number',
    'tests',
]

metadata = dict(
    name=DISTNAME,
    version=VERSION,
    long_description=README,
    packages=PACKAGES,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    author=AUTHOR,
    # author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    keywords=KEYWORDS,
    classifiers=[CLASSIFIERS],
    license=LICENSE
)


def setup_package() -> None:
    setup(**metadata)


if __name__ == '__main__':
    setup_package()
