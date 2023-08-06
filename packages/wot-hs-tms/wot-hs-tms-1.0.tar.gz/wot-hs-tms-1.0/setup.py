from setuptools import setup, find_packages


setup(
    name='wot-hs-tms',
    version='1.0',
    license='MIT',
    author="Hleb Serafimovich",
    author_email='hleb.serafimovich@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},

)