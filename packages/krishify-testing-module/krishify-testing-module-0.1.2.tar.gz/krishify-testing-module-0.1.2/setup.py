from setuptools import setup, find_packages


setup(
    name='krishify-testing-module',
    version='0.1.2',
    license='MIT',
    author="Ashish Kumar",
    author_email='ashish@krishify.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://www.krishify.com/',
    keywords='fbm module',
    install_requires=[
          'scikit-learn',
      ],

)