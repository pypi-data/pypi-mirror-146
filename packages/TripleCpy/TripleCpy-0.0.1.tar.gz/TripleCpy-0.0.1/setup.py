from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='TripleCpy',
    version='0.0.1',
    description='Chatterjee Correlation Coefficient',
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Behnam Sadeghi',
    author_email='z5218858@zmail.unsw.edu.au',
    license='MIT',
    classifiers=classifiers,
    keywords='Correlation Coefficient',
    packaes=find_packages(),
    install_requires=['']

)