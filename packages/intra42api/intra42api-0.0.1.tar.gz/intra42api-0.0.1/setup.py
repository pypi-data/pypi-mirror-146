from setuptools import setup, find_packages
 
classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
 
setup(
  name='intra42api',
  version='0.0.1',
  description='42Network API Wrapper',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Nasroallah El Idrissi',
  author_email='nelidris@student.1337.ma',
  license='MIT', 
  classifiers=classifiers,
  keywords=['API Wrapper', '42Network'], 
  packages=find_packages(),
  install_requires=['requests'] 
)