from setuptools import setup

setup(
    name="kenny-loggings",
    version="0.1.2",
    description="A simple Django model event logger.",
    long_description="A simple Django model event logger.",
    keywords="python, django, logging",
    author="Chris Jones <chris@brack3t.com>, Kenneth Love <kenneth@brack3t.com>",
    author_email="chris@brack3t.com",
    url="https://github.com/brack3t/kenny-loggings",
    license="BSD",
    packages=["loggings", "loggings.tests", "loggings.migrations"],
    zip_safe=False,
    install_requires=[],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Environment :: Web Environment",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ],
)
