from pathlib import Path
from setuptools import setup
import subprocess

"""
install gdal first
"""
def install_gdal():
    print("Installing gdal")
    filename=str(Path(__file__).resolve().parent/"first_install_gdal.sh")
    command = "bash %s" %filename
    print(command)
    results=subprocess.run(command, shell=True, universal_newlines=True, check=True)
    print("Resultado de instalar gdal",results.stdout)

path = Path(__file__).resolve().parent
with open(path/'README.md', encoding='utf-8') as f:
    long_description = f.read()

with open(path/'VERSION') as version_file:
    version = version_file.read().strip()

install_gdal()

setup(name='orm_collector',
      version=version,
      description='ORM Collector Schemma',
      url='http://gitlab.csn.uchile.cl/dpineda/orm_collector',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      packages=['orm_collector'],
      keywords="collector gnss orm",
      install_requires=["networktools",
                        "basic_logtools",
                        "validators",
                        "shapely",
                        "psycopg2",
                        "sqlalchemy>=1.3.17",
                        "geoalchemy2",
                        "ujson",
                        "django",
                        "click"],
      entry_points={
        'console_scripts': [
            "orm_create_db = orm_collector.scripts.create_db:run_crear_schema",
            "orm_load_data = orm_collector.scripts.load_data:load_data_orm",
            "orm_vars = orm_collector.scripts.create_db:show_envvars",
            "orm_show_data = orm_collector.scripts.show_data:show_data"
        ]
        },
      include_package_data=True,
      license='GPLv3',
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False
      )
