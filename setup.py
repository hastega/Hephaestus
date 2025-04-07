from setuptools import find_packages, setup

setup(
    name="hep",
    version="1.0.0",
    description="Hephaestus CLI Utility",
    long_description="",
    maintainer="Daniel Angelozzi",
    maintainer_email="d.angelozzi@hastega.it",
    author="Hastega",
    author_email="d.angelozzi@hastega.it",
    url="https://github.com/hastega/Hephaestus",
    license="MIT License",
    packages=find_packages(),
    install_requires=[
        "GitPython",
        "tqdm",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={
        "console_scripts": [
            "hep = hep.main:main",
        ],
    },
)
