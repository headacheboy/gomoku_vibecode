from setuptools import setup, Extension
from Cython.Build import cythonize
import sys

extensions = [
    Extension("gomoku.ai_cy", ["gomoku/ai_cy.pyx"]),
]

setup(
    name="gomoku_ai_cy",
    ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"}),
)
