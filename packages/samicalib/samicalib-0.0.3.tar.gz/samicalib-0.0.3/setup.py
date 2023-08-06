from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='samicalib',
  version='0.0.3',
  description='gets you a samica',
  long_description=open('README.txt').read(),
  url='',  
  author='Antek Meco',
  author_email='nik000@protonmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='samica', 
  packages=find_packages(),
  install_requires=[''] 
)