from setuptools import setup, find_packages


setup(
    name='model-insight',
    version='0.1',
    license='MIT',
    author="Wang Haihua",
    author_email='reformship@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='mathematical modeling',
    install_requires=[
          'numpy','pandas','matplotlib'
      ],

)
