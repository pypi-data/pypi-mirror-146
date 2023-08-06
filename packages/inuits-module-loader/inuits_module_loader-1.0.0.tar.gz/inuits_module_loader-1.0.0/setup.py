from distutils.core import setup

setup(
    name='inuits_module_loader',
    version='1.0.0',
    description="A library to load modules/classes based on their dotted string path.",
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
    provides=['inuits_module_loader']
)
