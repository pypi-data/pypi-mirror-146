import imp
import setuptools
from cding import __version__
 
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
 
setuptools.setup(
    name="cding", 
    version=__version__,
    author="ding chen",
    author_email="kevindingchan@outlook.com",
    license='MIT',
    description="A library with various functionality that can be useful.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kevindingchan/cding",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['tqdm', 'opencv-python', 'pandas', 'matplotlib', 'pycocotools'],
)