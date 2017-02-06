from setuptools import setup

setup(name='kpstat',
      version='1.0',
      description='Python Statistics',
      author='Damian Kacperski, Adam Poznar',
      author_email='adampoznar@gmail.com',
      download_url='https://github.com/kacperskid/bioinfo-statystyka',
      packages=['kpstat'],
      install_requires=['scipy','pandas']
     )
