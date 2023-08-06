from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="frappyapibilling",
      version="0.1.0",
      description="Billing and Quota Backend for Plan-Based, Restricted API Access",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ilfrich/frappy-api-billing",
      author="Peter Ilfrich",
      author_email="das-peter@gmx.de",
      packages=[
          "frappyapibilling"
      ],
      install_requires=[
          "flask"
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)
