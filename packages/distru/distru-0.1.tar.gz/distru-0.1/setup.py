from setuptools import setup, find_packages

setup(name='distru',
      version='0.1',
      description="Package to generate or read different distributions.\
                  Visualize and make some operations on the distributions",
      license='MIT',
      author="Osama Ayman",
      author_email='osama.ayman252@gmail.com',
      url='https://github.com/OsamaAyman/publish-pypi',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=[
          'matplotlib',
          'numpy'],
      )
