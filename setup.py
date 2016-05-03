from setuptools import setup, find_packages

setup(
    name='django-cache-extension',
    version='1.0.1',
    description='cache extension for django',
    url='https://github.com/Beeblio/django-cache-extension',
    author='Shanbay python dev group',
    author_email='developer@shanbay.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=('tests*',)),
    install_requires=map(lambda x: x.replace('==', '>='), open("requirements.txt").readlines()),
)
