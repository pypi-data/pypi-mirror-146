from setuptools import setup, find_packages


setup(
    name='ARES_EP',
    version='0.0.1',
    author="Zachary Baker",
    author_email='zac.r.baker06@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
