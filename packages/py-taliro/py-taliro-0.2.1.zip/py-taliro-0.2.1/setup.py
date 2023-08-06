""" Py-TaLiRo is the Python interface for TP/DP-TaLiRo.

It provides:

- A robust interface to the C libraries of TP/DP-TaLiRo
- Euclidean distance robustness computations
- Hybrid Automata (HA) representations as graphs
- Hybrid distance robustness computations
"""
DOCLINES = (__doc__ or "").split("\n")

from pathlib import Path

from numpy import get_include as np_include
from setuptools import Extension, setup
from Cython.Build import cythonize

CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License v2 (GPLv2)
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Programming Language :: C
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: Scientific/Engineering
Topic :: Software Development
Topic :: Software Development :: Libraries :: Python Modules
Typing :: Typed
"""


# collect C sources
source_dirs = ["src/core", "src/parser"]
source_files = [
    str(src_file) for src_dir in source_dirs for src_file in Path(src_dir).glob("**/*.c")
]

extensions = [
    Extension(
        name="tptaliro",
        sources=["bindings/python/tptaliro.pyx", *source_files],
        include_dirs=["src", np_include()],
    )
]

setup(
    name="py-taliro",
    version="0.2.1",
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    url="https://gitlab.com/sbtg/dp-taliro",
    author="Jacob Anderson",
    author_email="andersonjwan@gmail.com",
    download_url="https://pypi.org/project/py-taliro",
    project_urls={
        "Bug Tracker": "https://gitlab.com/sbtg/dp-taliro/issues"
    },
    license="GPLv2",
    classifiers=[cl for cl in CLASSIFIERS.split("\n") if cl],
    platforms=[
        "Linux",
        "Windows"
    ],
    ext_package="taliro",
    ext_modules=cythonize(extensions),
    install_requires=[
        "numpy>=1.22"
    ],
    python_requires=">=3.8"
)
