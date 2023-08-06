import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="relazioni",
    version="0.0.2",
    author="Dan A. Rosa De Jesús",
    author_email="contact@chicodelarosa.com",
    description="A lightweight package for strength of the relationship between two variables analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chicodelarosa/relazioni",
    project_urls={
        "Bug Tracker": "https://github.com/chicodelarosa/relazioni/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'':'src'},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'numpy',
        'scikit-learn',
        'pandas',
        'scipy',
    ],
)