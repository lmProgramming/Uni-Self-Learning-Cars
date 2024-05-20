from setuptools import setup # type: ignore
from Cython.Build import cythonize # type: ignore

# python cython_setup.py build_ext --inplace

setup(
    ext_modules = cythonize("vector_math.pyx")
)