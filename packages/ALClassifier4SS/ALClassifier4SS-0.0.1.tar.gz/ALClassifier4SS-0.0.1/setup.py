from setuptools import find_packages, setup

setup(
    name='ALClassifier4SS',
    packages=find_packages(),
    version='0.0.1',
    description='It is an active learning support vector machine library to classify school shooting',
    author='Minxing Zhang',
    author_email='minxing.zhang@emory.edu',
    license='MIT',
    install_requires=['scikit-learn', 'pandas', 'numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)