import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "p6-namer",
    "version": "0.8.28",
    "description": "Sets the AWS IAM Account Alias with a Custom Resource",
    "license": "Apache-2.0",
    "url": "https://github.com/p6m7g8/p6-cdk-namer.git",
    "long_description_content_type": "text/markdown",
    "author": "Philip M. Gollucci<pgollucci@p6m7g8.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/p6m7g8/p6-cdk-namer.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "p6_namer",
        "p6_namer._jsii"
    ],
    "package_data": {
        "p6_namer._jsii": [
            "p6-cdk-namer@0.8.28.jsii.tgz"
        ],
        "p6_namer": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.15.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.56.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
