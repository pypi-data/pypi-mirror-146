from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fw2ai',
    version='0.1.1',    
    description='Making security analysis simpler by applying AI to binary artefacts of firmware',
    url='https://github.com/cpuinfo/fw2ai.git',
    author='Mahesh Patil',
    author_email='cpuinfo10@gmail.com',
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=find_packages("fw2ai/src"),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["fw2ai"],             # Name of the python package
    package_dir={'':'fw2ai/src'},     # Directory of the source code of the package
    include_package_data=True,
    install_requires=["Click"],                     # Install other dependencies if any
    entry_points={
        "console_scripts": [
            "fw2ai = fw2ai:cli",
        ]
    }
)