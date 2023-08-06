from setuptools import setup

setup(
    install_requires=[
        "cffi==1.15.0",
        "cryptography==36.0.0",
        "dataclasses==0.6; python_version == '3.6'",
        "pycparser==2.21",
        "pyjwt[crypto]==2.3.0",
    ],
    dependency_links=[],
)
