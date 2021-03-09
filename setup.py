"""Export litex SoC definitions to Zephyr board files"""

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setuptools.setup(
    name="litex_zephyr_export",
    version="0.1",
    author="Robert Wilbrandt",
    author_email="robert@stamm-wilbrandt.de",
    description="Export litex SoC definitions to Zephyr board files",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    scripts=["scripts/generate-zephyr-board"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
)
