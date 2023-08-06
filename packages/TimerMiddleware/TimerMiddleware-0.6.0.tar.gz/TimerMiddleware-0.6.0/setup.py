from setuptools import setup

setup(name='TimerMiddleware',
      version='0.6.0',
      url='http://sourceforge.net/p/timermiddleware',
      description='add timing instrumentation to WSGI applications',
      long_description='TimerMiddleware is a Python package for adding timing instrumentation to WSGI applications.',
      packages=['timermiddleware'],
      install_requires=['webob', 'future'],
      python_requires='>=3.7',
      tests_require=['nose'],
      license='Apache 2.0',
      classifiers=[
          #  From http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3.7',
          'Topic :: System :: Benchmark',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
      ],
)
