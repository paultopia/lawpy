from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='lawpy',
      version='0.1',
      description='Pythonic interface to courtlistener.com api',
      long_description=readme(),
      url='https://github.com/paultopia/lawpy',
      classifiers=[
          'Development Status :: 3 - Alpha',
          "Intended Audience :: Developers",
          "Intended Audience :: Legal Industry",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3 :: Only"
      ],
      keywords="law, courtlistener, cases, court",
      author='Paul Gowder',
      author_email='paul.gowder@gmail.com',
      license='MIT',
      packages=['lawpy'],
      install_requires=[
          'requests'
      ],
      python_requires='>=3',
      zip_safe=False)