from setuptools import setup, find_packages

with open("README.md", "r") as rd:
  long_description = rd.read()

setup(
 name="verefa",
 version='1.2.2',
 description='Verefa client side package for sending and receiving data from the Verefa database system.',
 url='https://verefa.com/', 
 author='Verefa Development',
 author_email='admin@verefa.com',
 long_description=long_description,
 long_description_content_type="text/markdown",
 classifiers=[
   'Development Status :: 5 - Production/Stable',
   'Intended Audience :: Developers',
   'Operating System :: OS Independent',
   'License :: OSI Approved :: MIT License',
   'Programming Language :: Python :: 3',
   'Programming Language :: Python :: 3.5',
   'Programming Language :: Python :: 3.6',
   'Programming Language :: Python :: 3.7',
   'Programming Language :: Python :: 3.8',
 ],
 keywords=['python', 'verefa', 'encryption', 'database'],
 packages=find_packages()
)