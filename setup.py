import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mdalint",
    version="0.0.1",
    author="Jonathan Barnoud",
    author_email="jonathan@barnoud.net",
    description="Linter for MDAnalysis and programs using it.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MDAnalysis/mdalint",
    project_urls={
        "Bug Tracker": "https://github.com/MDAnalysis/mdalint/issues",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    packages=['mdalint'],
    python_requires=">=3.7",
    install_requires=[
        'astroid',
    ],
    entry_points={
        'console_scripts': ['mdalint=mdalint:cli'],
    },
)
