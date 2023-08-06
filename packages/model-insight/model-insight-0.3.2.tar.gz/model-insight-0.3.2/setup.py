from setuptools import setup, find_packages


setup(
    name='model-insight',
    version='0.3.2',
    license='MIT',
    author="Wang Haihua",
    author_email='reformship@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/reformship/model-insight',
    keywords='mathematical modeling',
    install_requires=[
          'numpy','pandas','matplotlib'
      ],

)
