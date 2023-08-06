import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agci",
    version="0.0.1",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="how to debut a PyPI for chemistry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ytakefuji/agci",
    project_urls={
        "Bug Tracker": "https://github.com/ytakefuji/agci",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['agci'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'agci = agci:main'
        ]
    },
)
