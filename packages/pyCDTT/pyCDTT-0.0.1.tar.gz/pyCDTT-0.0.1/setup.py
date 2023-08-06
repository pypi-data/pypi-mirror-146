import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyCDTT",
    version="0.0.1",
    author="CDT",
    author_email="ZMF_CDT-1@outlook.com",
    description="这是CDT的工具包模块！",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ],
    install_requires=[],
    python_requires=">=3",
    # url="https://github.com/CDT-1/",
)