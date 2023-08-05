
from setuptools import setup
  
# reading long description from file
with open('DESCRIPTION.txt') as file:
    long_description = file.read()
  
  
# specify requirements of your package here
REQUIREMENTS = ['tensorflow','tensorflow_addons','numpy','gensim','requests']
  
# some more details
CLASSIFIERS = [
    'Development Status :: 1 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    ]
  
# calling the setup function 
setup(name='utranslate',
      version='1.0.0',
      description='translation module ',
      long_description=long_description,
      url='',
      author='Vaibhav Mankar',
      author_email='mankarvaibhav819@gmail.com',
      license='MIT',
      packages=['utranslate'],
      #classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='python'
      )