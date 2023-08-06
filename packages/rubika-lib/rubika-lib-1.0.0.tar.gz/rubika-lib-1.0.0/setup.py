from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["jdatetime", "pytz", "pycryptodome", "requests" , "tqdm", "urllib3"]

setup(
    name="rubika-lib",
    version="1.0.0",
    author="Shayan Heidari",
    author_email="snipe4kill.tg@gmail.com",
    description="This is an unofficial library for deploying robots on Rubika accounts",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/snipe4kill/rubika/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
)