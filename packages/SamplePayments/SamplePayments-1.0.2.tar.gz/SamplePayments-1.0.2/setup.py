from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='SamplePayments',
  version='1.0.2',
  description='Sample payment library',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sudharshan Shetty',
  author_email='sudharshan.ss@vavve.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['Payments'], 
  packages=find_packages(),
  install_requires=['requests','json.encoder'] 
)