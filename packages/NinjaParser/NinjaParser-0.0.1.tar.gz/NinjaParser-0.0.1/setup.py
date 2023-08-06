from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="NinjaParser",
    version="0.0.1",
    author="Murat Keçeli",
    author_email="keceli@gmail.com",
    description="Parse .ninja_log files and print statistics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keceli/NinjaParser",
    project_urls={
        "Bug Tracker": "https://github.com/keceli/NinjaParser/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["ninja_parser"],
    entry_points={
        'console_scripts': [
            'ninja_parser = ninja_parser:main',
        ],}
)
