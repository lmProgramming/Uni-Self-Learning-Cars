from setuptools import setup
from Cython.Build import cythonize

# python cython_setup.py build_ext --inplace

setup(
    ext_modules = cythonize("vector_math.pyx")
)