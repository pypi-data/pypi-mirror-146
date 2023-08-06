from setuptools import setup, find_packages


setup(
    name='model-insight',
    version='0.3.5',
    license='MIT',
    author="Wang Haihua",
    author_email='reformship@gmail.com',
    description='A package for learning and teaching mathematical modeling',
    long_description=open('DESCRIPTION.rst').read(),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/reformship/model-insight',
    keywords='mathematical modeling',
    install_requires=[
          'numpy','pandas','matplotlib'
      ],
    include_package_data=True,
    package_data={'': ['src/model_insight/datasets/*.csv','src/model_insight/datasets/*.xls','src/model_insight/datasets/*.xlsx']},

)
