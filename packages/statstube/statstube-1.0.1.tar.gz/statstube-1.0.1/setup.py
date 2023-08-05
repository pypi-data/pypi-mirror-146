from setuptools import find_packages, setup

setup(
    name='statstube',
    packages=find_packages(include=['statstube']),
    version='1.0.1',
    description='This project aims to provide a proper and simpler way to crawl YouTube content.',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='William Kana',
    author_email='',
    keyword='YouTube-Crawler',
    license='Apache-2.0 License',
    install_requires=[''],
    setup_requires=['pytest-runner==5.3.1'],
    tests_require=['pytest==7.0.0'],
    test_suite='tests',
)
