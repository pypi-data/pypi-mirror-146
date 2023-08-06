from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='IMD',
  version='1.0',
  description='Gets difference between images',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Niek D.',
  author_email='guest12085@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='difference',
  packages=find_packages(where='IMD/__init.py', include='*'),
  install_requires=['PIL'] 
)