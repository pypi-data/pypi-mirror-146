from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='VirtualPlayroomSIM',
  version='1.0.0',
  description='Playroom Simulator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Jiafei, Jieyi',
  author_email='duanjiafei@hotmail.sg',
  license='MIT', 
  classifiers=classifiers,
  keywords='simulator', 
  packages=find_packages(),
  install_requires=[''] 
)