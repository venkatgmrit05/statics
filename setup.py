# setup.py placed at root directory
from setuptools import setup, find_packages
# import re

# __version__ = re.findall(
#     r""" __version__ =["']+([0-9\.\-dev]*)["']+""",
#     open('linkedinjobautomation/__init__.py').read(),
# )[0]

prod_requirements = []
dev_requirements = []

setup(
    name='statics',
    version='0.0.1',
    author='umavenkatkaranam',
    description='physics statics',
    long_description='solver for physics statics problems',
    url='',
    keywords='physics, python ,statics, setuptools',
    # packages='find:',
    packages=find_packages(),
    python_requires='>=3.7, <4',
    install_requires=['pandas', 'numpy'],
    extras_require={
        'test': ['pytest', 'coverage'],
    },
    package_data={
        'statics': [],
    },
    entry_points={
        'console_scripts': [
            'statics=statics:autoapply',
        ]
    }
)
