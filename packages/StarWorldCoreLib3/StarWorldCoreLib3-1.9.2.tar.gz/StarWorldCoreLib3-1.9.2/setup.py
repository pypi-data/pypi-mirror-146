import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="StarWorldCoreLib3",
    version="1.9.2", 
    author="StarWorld", 
    author_email="starworldstudio1@gmail.com",
    description="StarWorldCoreLib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WowStarWorld/StarWorldCoreLib3",
    packages= setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
setuptools.setup()
