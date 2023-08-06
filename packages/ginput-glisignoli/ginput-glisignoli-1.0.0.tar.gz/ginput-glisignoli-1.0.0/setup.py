from setuptools import find_packages, setup

# Meta information
version = open('VERSION').read().strip()
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # Basic info
    name='ginput-glisignoli',
    version=version,
    author='Gino Lisignoli',
    author_email='glisignoli@gmail.com',
    url='https://github.com/glisignpli/python-ginput',
    description='Send keystrokes to a virtual keyboard',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/glisignoli/python-ginput/issues",
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages(where="src"),
    install_requires=['libevdev==0.10', 'pyperclip==1.8.2'],
    extras_require={
        'dev': [
            'autopep8'
        ],
    },

    # Scripts
    entry_points={
        'console_scripts': [
            'ginput=ginput.command_line:main'],
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
    python_requires=">=3.10",
)
