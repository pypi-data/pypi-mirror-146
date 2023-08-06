import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="how_its_made",                     # This is the name of the package
    version="1.2",                        # The initial release version
    author="Callum Evans",                     # Full name of the author
    description="Generates how it's made titles",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["how_its_made"],             # Name of the python package
    package_dir={'':'how_its_made/src'},     # Directory of the source code of the package
    install_requires=['pyttsx3>=2.90']                     # Install other dependencies if any
)

print("Thanks for installing 'How It's Made!' (v 1.2)")