from setuptools import setup, find_packages

setup(
    name='tms_test_project',
    version='0.2',
    author="Dzmitry Mishuta",
    author_email='moonmvmd@gmail.com',
    license='MIT',
    description='This is the project for testing.',
    packages=find_packages(),
    url='https://github.com/moonmvm/RPPBA',
    install_requires=[
        'Django==4.0.4',
        'fastapi==0.75.1',
    ],
)