import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepwin_alpha",
    version="0.0.1",
    author="leon",
    author_email="leon0226@gmail.com",
    description="a small backtest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/Ye980226/deepwin_alpha",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)