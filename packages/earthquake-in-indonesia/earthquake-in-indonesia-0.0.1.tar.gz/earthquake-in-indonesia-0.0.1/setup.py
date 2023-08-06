"""
https://packaging.python.org/en/latest/tutorials/packaging-projects/
markdown guide : https://www.markdownguide.org/cheat-sheet
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="earthquake-in-indonesia",
    version="0.0.1",
    author="Hendra Kusuma",
    author_email="hendrakusuma.vegas@gmail.com",
    description="this package will scrape information  (BMKG)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Henzo-Kawaii/latest-information-earthquake-update--indonesia",
    project_urls={
        "Website": "https://henzogagerz.blogspot.com/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src")
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
