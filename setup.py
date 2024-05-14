from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("vector_math.pyx")
)