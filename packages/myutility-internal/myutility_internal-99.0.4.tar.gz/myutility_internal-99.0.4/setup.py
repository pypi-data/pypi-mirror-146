from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='myutility_internal',
    version='99.0.4',
    description='This is an internal utility that will process numbers.',
    py_modules=["myutility_internal"],
    package_dir={'': 'src'},
    extras_require={
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
	"Programming Language :: Python :: 3.9",
	'Programming Language :: Python :: 3.10',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Super Secure",
    author_email="sectester15@gmail.com",
    url="https://github.com/ndoell/myutility_internal"
)
