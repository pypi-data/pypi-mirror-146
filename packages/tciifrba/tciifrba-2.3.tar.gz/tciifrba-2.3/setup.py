from setuptools import setup

setup(
   name='tciifrba',
   version='2.3',
   description='Biblioteca de la cátedra de TCII UTN FRBA',
   author='Andres Di Donato, Mariano Llamedo Soria',
   author_email='foomail@foo.com',
   packages=['tciifrba'],  # would be the same as name
   install_requires=['schemdraw '], #external packages acting as dependencies
)