"""A package for overriding yaml.
"""

from setuptools import setup, find_namespace_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="yaml-override",
    version="0.0.1",
    description="A YAML pre-processor to override one or more YAML files with the values.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/intelliguy/yaml-override",
    author="Sungil Im",
    author_email="usnexp@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Markup",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="yaml, merge, override",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    # namespace_packages=["intelliguy"],
    python_requires=">=3.6, <4",
    install_requires=["pyyaml"],
    extras_require={  # Optional
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    # entry_points={
    #     "console_scripts": [
    #         "yaml-override=intelliguy.yaml_combine.__main__:main",
    #     ],
    # },
    project_urls={
        "Bug Reports": "https://github.com/intelliguy/yaml-override/issues",
        "Source": "https://github.com/intelliguy/yaml-override/",
    },
)
