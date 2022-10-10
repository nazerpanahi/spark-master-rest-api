import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spark_master_rest_api",
    python_requires=">=3.6",
    version="0.1.0",
    url="https://github.com/nazerpanahi/spark-master-rest-api",
    license="GPLv3",
    author="Hamid Nazerpanahi",
    description="Wrapper for spark master REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["spark_master_rest_api"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
