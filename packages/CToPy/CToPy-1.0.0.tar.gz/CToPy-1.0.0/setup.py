from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='CToPy',
  version='1.0.0',
  description='C function compiler library',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ondřej Baudisch',
  author_email='ondrabaudisch@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='compiler', 
  packages=find_packages(),
  install_requires=[''] 
)