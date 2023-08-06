import setuptools
from pathlib import Path

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="smtp4helm",
    version="0.0.2",
    author="Evan Ottinger",
    author_email="evan@ottingerdigitallabs.com",
    description="Wrapper for smtplib to interface with Helm server",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/evanottinger/helm-smtp",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    packages=["smtp4helm"],
    install_requires=["pytomlpp"],
)
