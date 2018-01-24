from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='mini_shd',
    version='0.1',
    packages=find_packages(),
    package_data={
        'mini_shd_webclient': [
            'templates/*.html',
            'static/*.css',
            'static/bootstrap/css/*.css',
            'static/bootstrap/img/*.png',
            'static/bootstrap/js/*.js'
        ]
    },
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
)
