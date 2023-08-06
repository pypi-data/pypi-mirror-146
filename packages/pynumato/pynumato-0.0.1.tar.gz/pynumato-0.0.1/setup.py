import setuptools
from codecs import open as codec_open
from os import close, unlink
from os.path import abspath, dirname, join as joinpath
from re import split as resplit, search as research

META_PATH = joinpath('pynumato', '__init__.py')

HERE = abspath(dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codec_open(joinpath(HERE, *parts), 'rb', 'utf-8') as dfp:
        return dfp.read()


def read_desc(*parts):
    """Read and filter long description
    """
    text = read(*parts)
    text = resplit(r'\.\.\sEOT', text)[0]
    return text


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = research(
        r"(?m)^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    print(long_description)

setuptools.setup(
    name="pynumato",
    version=find_meta('version'),
    author="Tiempo",
    author_email="henitsoa.rakotomalala@tiempo-secure.com",
    description="Library to communicate with relays",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henitsoa-tiempo/pynumato.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=[
        ],
)

# setuptools.setup(
#     name=find_meta('title'),
#     version=find_meta('version'),
#     author=find_meta('author'),
#     author_email=find_meta('email'),
#     description=find_meta('description'),
#     long_description = long_description,
#     long_description_content_type="text/markdown",
#     url=find_meta('uri'),
#     packages=setuptools.find_packages(),
#     package_dir={'': '.'},
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: Apache Software License",
#         "Operating System :: OS Independent",
#         "Development Status :: 5 - Production/Stable"
#     ],
#     python_requires='>=3.6',
# )
