from setuptools import setup
from pathlib import Path

path = Path(__file__).resolve().parent


with open(path/'README.md', encoding='utf-8') as f:
    long_description = f.read()

    
with open(path/'VERSION') as version_file:
    version = version_file.read().strip()


setup(name='collector_ring_buffer',
      version=version,
      description='Ring Buffer para controlar latencia',
      url='http://gitlab.csn.uchile.cl/dpineda/collector',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='MIT',
      packages=['crb'],
      keywords = ["collector","buffer", "control"],
      install_requires=[],
      entry_points={},
      include_package_data=True,
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
