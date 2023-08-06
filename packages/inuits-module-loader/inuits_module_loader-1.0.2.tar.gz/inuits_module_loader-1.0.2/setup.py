from distutils.core import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

setup(
    name='inuits_module_loader',
    version='1.0.2',
    description='A library to load modules/classes based on their dotted string path.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
    author='Matthias Dillen',
    author_email='matthias.dillen@inuits.eu',
    license='GPLv2',
    packages=[
        'inuits_module_loader'
    ],
    provides=['inuits_module_loader'],
    url='https://github.com/inuits/module-loader'
)
