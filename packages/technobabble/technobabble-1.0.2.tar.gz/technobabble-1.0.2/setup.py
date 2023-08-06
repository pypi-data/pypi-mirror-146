import glob
import os

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

current_path = os.path.dirname(os.path.abspath(__file__))
json_files = [
    os.path.relpath(path, current_path)
    for path in glob.glob(f"{current_path}/**/*.json", recursive=True)
]
resource_files = [
    os.path.relpath(path, current_path)
    for path in glob.glob(f"{current_path}/technobabble/resources/*", recursive=True)
]

setuptools.setup(
    name="technobabble",
    version="1.0.2",
    author="Giorgio Vilardo",
    description="Technobabble will own your soul",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
