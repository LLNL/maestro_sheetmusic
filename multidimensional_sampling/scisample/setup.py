import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scisample",
    version="0.0.1",
    author="Chris Krenn",
    author_email="TBD",
    description="Parameter sampling for scientific computing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="TBD",
    license='MIT License',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'maestrowf': ['maestrowf'],
        'best_candidate': ['pandas', 'numpy', 'scipy']
    }
)
