import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="widgeon",
    version="0.0.2",
    author="Simon Kriele",
    author_email="kriele.simon@gmail.com",
    description="A simple tool for building UIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dots-git/widgets",
    project_urls={
        "Bug Tracker": "https://github.com/dots-git/widgets/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    package_data={"": ["data/*"]},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

