import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epysod", # Replace with your own username
    version="0.0.4",
    author="i am vee",
    install_requires=['docutils>=0.3'],
    author_email="naeini.v@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamvee/epysod",
    packages=setuptools.find_packages(),
    scripts=['bin/epysod'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
