from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Base project template'
LONG_DESCRIPTION = 'A base Python project template'

# Setting up
setup(
    name="magnifi_base_template",
    version=VERSION,
    author="Nick Wight",
    author_email="<nick.wight@mymagnifi.org>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['magnifi', 'templates'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)