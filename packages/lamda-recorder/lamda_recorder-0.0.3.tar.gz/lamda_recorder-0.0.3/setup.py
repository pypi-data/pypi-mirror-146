import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lamda_recorder",
    version="0.0.3",
    install_requires=['prettytable', 'numpy'],
    author="Haoyuan He",
    author_email="hehy@lamda.nju.edu.cn",
    description="recorder for machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
