from setuptools import (
    setup,
    find_packages,
    )

setup(
    name="masxml_dali_parser",
    version = "0.0.2",
    author="Chris M",
    author_email='c.j.madge@qmul.ac.uk',
    url="https://github.com/chrism-qmul/masxml_dali_parser",
    download_url = "https://github.com/chrism-qmul/masxml_dali_parser",
    description="Parser for new MASXML DALI Format",
    long_description="""Thin extension of ETree to help parse MASXML DALI files""",
    license="MIT",
    packages=find_packages(),
    install_requires = [
      'lxml>=4.2.5'
      ],
    use_2to3 = True,
    classifiers=[
      "Intended Audience :: Developers",
      "License :: OSI Approved :: MIT License",
      'Programming Language :: Python :: 3',
      "Topic :: Text Processing :: Markup :: XML",
      ],
    )
