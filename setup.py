from setuptools import setup

setup(
    name="kenny-loggings",
    version="0.1.0",
    description='',
    long_description='',
    keywords="python, django",
    author="Chris Jones <chris@brack3t.com>",
    author_email="chris@brack3t.com",
    url="https://github.com/brack3t/kenny-loggings",
    license="BSD",
    packages=["loggings"],
    zip_safe=False,
    install_requires=["requests"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2 :: Only",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Intended Audience :: Information Technology"
    ],
)
