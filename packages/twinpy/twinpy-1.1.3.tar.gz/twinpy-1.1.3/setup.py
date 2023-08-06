import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twinpy",
    version="1.1.3",
    author="Robert Roos",
    author_email="robert.soor@gmail.com",
    license="MIT",
    description="Package to interface with TwinCAT (incl. Simulink models)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/ctw-bw/twinpy",
    packages=["twinpy.twincat", "twinpy.ui"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    install_requires=[
        "pyads>=3.3.9",
        "PyQt5>=5.15",
        "pyqtconsole>=1.2.2",
        "pyqtgraph>=0.12.3",
    ],
    python_requires=">=3.6",
)
