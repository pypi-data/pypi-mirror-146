import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iot_protocol_rule_py3",
    version="2.2.0",
    author="ikxyang",
    author_email="sosdawn@163.com",
    description="iot_protocol_rule_py3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/ikxyang/iot_protocol_rule_py3",
    project_urls={
        "Bug Tracker": "https://gitee.com/ikxyang/iot_protocol_rule_py3/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.5",
)
