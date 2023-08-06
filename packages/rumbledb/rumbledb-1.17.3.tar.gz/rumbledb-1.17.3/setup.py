import setuptools

setuptools.setup(
    # Name of the module
    name='rumbledb',
    version='1.17.3',
    # Details
    description='Jupyter extensions to use RumbleDB in notebooks, in server mode or through Apache Livy.',
    long_description='Jupyter extensions to use RumbleDB in notebooks, in server mode or through Apache Livy.',
    # The project's main homepage.
    url='https://www.rumbledb.org/',
    # Author details
    author='Ghislain Fourny',
    author_email='ghislain.fourny@inf.ethz.ch',
    # License
    license='Apache License 2.0',
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    keywords='rumble jsoniq rumbledb json IPython jupyter',
    classifiers=[
        # Intended Audience.
        'Intended Audience :: Developers',
        # Operating Systems.
        'Operating System :: OS Independent',
    ],
    install_requires=['requests', 'jupyter'],
)
