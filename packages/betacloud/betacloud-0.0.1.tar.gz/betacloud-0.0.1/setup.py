from setuptools import find_packages
from setuptools import setup

PROJECT = 'betacloud'
exec(open(f'{PROJECT}/version.py').read())

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=__version__,  # noqa

    description='OSISM manager interface',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='OSISM GmbH',
    author_email='info@osism.tech',

    maintainer='OSISM GmbH',
    maintainer_email='info@osism.tech',

    url='https://github.com/betacloud/client',
    download_url='https://github.com/betacloud/client/tarball/main',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Developers',
        'Environment :: Console',
    ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'betacloud= betacloud.main:main'
        ]
    },

    zip_safe=False,
)
