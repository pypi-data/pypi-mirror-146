import setuptools
from distutils.util import convert_path

# https://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
main_ns = {}
ver_path = convert_path('ghasandbox/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GitHub Actions Sandbox",
    version=main_ns['VERSION'],
    author="Todd Roberts",
    author_email="toddrob@gmail.com",
    description="Sandbox for GitHub Actions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toddrob99/gh-actions-sandbox",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
