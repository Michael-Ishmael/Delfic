from distutils.core import setup

setup(
    name='delfic_crawler',
    version='1.00',
    packages=['delfic', 'delfic.data', 'delfic.crawler', 'delfic.crawler.xgoogle', 'delfic.entities',
              'delfic_crawler_test'],
    url='',
    license='',
    author='scorpio',
    author_email='',
    description='Crawly Script', requires=['jnius']
)
