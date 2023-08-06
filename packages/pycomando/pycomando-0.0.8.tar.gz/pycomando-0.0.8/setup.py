import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="pycomando",
    version=get_version("pycomando/__init__.py"),
    author="Daniel Oberti",
    author_email="obertidaniel@gmail.com",
    description="Wrapper command",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/doberti/pycomando",
    download_url='http://pypi.python.org/pypi/pycomando/',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=["pycomando"],
    platforms='any',
    data_files=[
        ('share/pycomando/examples', ['examples/ejemplo1.py']),
        ('share/pycomando', ['LICENSE', 'README.md']),
    ],
    entry_points={
        'console_scripts': ['pycomando=pycomando.pycomando:main'] #????
    },
    python_requires=">=3.7",
    # setup_requires=['flake8']
    install_requires=[
        'argcomplete',
        'rich',
        'tabulate',
        'redis',
        'pandas',
        'eland',
        'elasticsearch',
        'PyYAML'
    ]
)
