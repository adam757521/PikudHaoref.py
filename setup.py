from setuptools import setup

f = open("README.md", "r")
README = f.read()

setup(
    name="pikudhaoref.py",
    packages=["pikudhaoref"],
    version="0.0.6",
    license="MIT",
    description="An API wrapper for Pikud Haoref's rocket API.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="adam7100",
    url="https://github.com/adam757521/PikudHaoref.py",
    download_url="https://github.com/adam757521/PikudHaoref.py/archive/refs/tags/v0.0.6.tar.gz",
    keywords=["rocket", "siren", "pikudhaoref", "api", "wrapper", "python"],
    install_requires=[
        "requests",
        "aiohttp",
        "pytz",
    ],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
