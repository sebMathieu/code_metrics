from setuptools import setup, find_packages

setup(
    name='code_metrics',
    version='0.0.2',
    description='Compute Python code metrics reports.',
    url='https://github.com/sebMathieu/code_metrics',
    author='Sébastien Mathieu',
    packages=find_packages(),
    package_data={'': ['*.svg']},
    install_requires=['docopt',
                      'radon',
                      'coverage',
                      'rst',
                      'jinja2'],
    zip_safe=False
)
