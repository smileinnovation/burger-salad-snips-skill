from setuptools import setup

setup(
    name='foodinference',
    version='1.0.0',
    description='Food classification skill',
    author='Yenshu',
    url='',
    download_url='',
    license='MIT',
    install_requires=['pyserial', 'configparser','netaddr', ' pycryptodome'],
    test_suite="tests",
    keywords=['snips', 'food'],
    packages=['foodinference'],
    package_data={'foodinference': ['Snipsspec']},
    include_package_data=True
)
