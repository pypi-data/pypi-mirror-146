import setuptools
from pathlib import Path

setuptools.setup(
    name="lyypdf",  # unique，不能与pypi存储库中的包重名
    version=1.0,
    long_description=Path("README.md").read_text(),
    # 告诉 what packages are going to be 分发distributed
    # 因为在这个项目中，目前有一个package：lyypdf
    # lyypdf 包中两个modules：pdf2image, pdf2text

    # 查找项目并自动发现我们定义了的packages，但是需要告诉他派出两个目录test和data【setuptools.find_packages([排除字符串])】
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
