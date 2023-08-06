import setuptools

setuptools.setup(
    name="orpl",
    version="22313",
    author="OpenRE",
    author_email="admin@w102018tv.xyz",
    description="The fork of simpledemotivators",
    url="https://github.com/Daemon-RE/openre-pylib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pillow',
        'requests',
    ],
)
