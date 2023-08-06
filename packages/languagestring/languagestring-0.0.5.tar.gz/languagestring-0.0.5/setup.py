from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="languagestring",
    version="0.0.5",
    author="Matt Waller",
    author_email="mattghwaller@gmail.com",
    description="Get all language characters for some european languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MattWaller/languagestring",
    project_urls={
        "Bug Tracker": "https://github.com/MattWaller/languagestring/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['languagestring'],                      # root folder of your package
    package_dir={'/': ''},      # directory which contains the python code
    package_data={'/': ['assets/*.json']},  # directory which contains your json
    python_requires=">=3.6",
    include_package_data=True,
)