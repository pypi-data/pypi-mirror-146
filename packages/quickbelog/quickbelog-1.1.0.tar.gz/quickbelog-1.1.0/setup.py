import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="quickbelog",
    version="1.1.0",
    author="Eldad Bishari",
    author_email="eldad@1221tlv.org",
    description="Automate IT operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eldad1221/quickbelog",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
