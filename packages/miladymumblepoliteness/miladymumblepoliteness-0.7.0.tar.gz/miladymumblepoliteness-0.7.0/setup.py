import setuptools

from better_profanity import __version__

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="miladymumblepoliteness",
    version=__version__,
    author="nullbuddy1243",
    author_email="",
    description="fork of better_profanity for milady mumble politeness ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nullbuddy1243/miladymumblepoliteness",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires="==3.*",
    packages=setuptools.find_packages(),
    data_files=[
        ("wordlist", ["better_profanity/profanity_wordlist.txt"]),
        ("unicode_characters", ["better_profanity/alphabetic_unicode.json"]),
    ],
    package_data={
        "miladymumblepoliteness": ["profanity_wordlist.txt", "alphabetic_unicode.json"]
    },
    include_package_data=True,
)
