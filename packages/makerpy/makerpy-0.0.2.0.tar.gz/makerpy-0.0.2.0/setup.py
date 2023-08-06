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
  version='0.0.2.0',
  description='A python libary that makes the hard things easy.',
  long_description="This is a tool that helps you to make hard things easy.",
  url='',  
  author='Rocko Visser',
  author_email='rockodagamer@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='app development',
  packages=find_packages(),
  install_requires=['pygame', 'tensorflow']
)
