import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TUMMET",
    version="0.0.5",
    author="Michael Winkler",
    author_email="michael.b.winkler@tum.de",
    description="A packages to evaluate material test data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mbwinkler/TUM-MET",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "TUMMET"},
    packages=setuptools.find_packages(where="TUMMET"),
    python_requires=">=3.9",
    install_requires=[
        'colorama == 0.4.4',
        'cycler == 0.11.0',
        'fonttools == 4.31.2',
        'kiwisolver == 1.4.2',
        'matplotlib == 3.5.1',
        'numpy == 1.22.3',
        'packaging == 21.3',
        'pandas == 1.4.2',
        'Pillow == 9.1.0',
        'pyparsing == 3.0.7',
        'pytz == 2022.1',
        'scipy == 1.8.0',
        'seaborn == 0.11.2',
        'six == 1.16.0',
        'tqdm == 4.64.0']
)
