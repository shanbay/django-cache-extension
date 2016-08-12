from setuptools import setup

setup(
    name='django-cache-extension',
    version='1.0.10',
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
    packages=['cache_extension'],
    package_data={'cache_extension': ['backends/*.py']},
    install_requires=['django-redis', 'redis', 'hiredis'],
)
