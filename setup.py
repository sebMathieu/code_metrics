from setuptools import setup, find_packages

setup(
    name='code_metrics',
    version='0.0.1',
    description='Compute Python code metrics reports.',
    url='https://github.com/sebMathieu/code_metrics',
    author='Sébastien Mathieu',
    packages=find_packages(),
    install_requires=['docopt',
                      'radon',
                      'coverage',
                      'rst'],
    zip_safe=False
)
