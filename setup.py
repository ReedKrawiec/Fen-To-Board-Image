import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='fenToBoardImage',  
     version='0.4',
     author="Reed Krawiec",
     author_email="reedkrawiec@gmail.com",
     description="Create PIL images from chess Fen strings",
     long_description=long_description,
   long_description_content_type="text/markdown",
     keywords=["chess fen Pil low board"],
     license="MIT",
     url="https://github.com/ReedKrawiec/fenToBoardImage",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
         "Topic :: Scientific/Engineering :: Image Processing"
     ],
 )