from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='makerpy',
  version='0.0.1.1',
  description='A very work in progress tool that helps you create a python project by helping you with for example pygame',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Rocko Visser',
  author_email='rockodagamer@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='app development',
  packages=find_packages(),
  install_requires=['pygame', 'tensorflow']
)
