from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="VVSW",
    ext_modules=cythonize(['./artifical_intelligence/*.pyx', './game_state/*.pyx'])
)