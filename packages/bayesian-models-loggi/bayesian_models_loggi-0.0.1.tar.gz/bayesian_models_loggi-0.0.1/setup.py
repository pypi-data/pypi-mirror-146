from setuptools import find_packages, setup

setup(
    name='bayesian_models_loggi',
    packages=find_packages(include=['bayesian_models_loggi']),
    version='0.0.1',
    description='Bayesian Models, focused on comparing tests scenarios.',
    author='Loggi - Yan Werneck',
    license='MIT',
    install_requires=['numpy', 'plotly'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)