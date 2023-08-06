from setuptools import setup, find_packages
 
setup(
    name='metathing',
    version='0.1.7',
    description='MT-Service Python',
    license='N/A',
    packages=find_packages(exclude=['test', 'workdir', 'metathing/__pycache__']),
)