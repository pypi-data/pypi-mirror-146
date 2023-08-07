from setuptools import setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='quizmaker3000',
    version='0.0.1',
    description='A very simple quiz maker. Thats it.. Stop..  It took a while don\'t question me',
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Limeed',
    author_email='limeed.yt@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='ASCII, terminal, output',
    packages=find_packages(),
    install_requires=['']
)