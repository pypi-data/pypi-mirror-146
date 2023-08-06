import os

from setuptools import find_packages, setup

version_contents = {}
version_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "tianqiai/version.py"
)
with open(version_path, "rt") as f:
    exec(f.read(), version_contents)

setup(
    name="tianqiai",
    description="Python client library for the tianqiai API",
    version=version_contents["VERSION"],
    install_requires=[
        "requests>=2.20",  # to get the patch for CVE-2018-18074
        "tqdm",  # Needed for progress bars
        "pandas>=1.2.3",  # Needed for CLI fine-tuning data preparation tool
        "pandas-stubs>=1.1.0.11",  # Needed for type hints for mypy
    ],
    extras_require={"dev": ["black~=21.6b0", "pytest==6.*"]},
    python_requires=">=3.6.1",
    entry_points={
        'console_scripts': [
            'tianqiai=tianqiai._tianqiai_scripts:main',
        ],
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "tianqiai": [
            "py.typed",
        ]
    },
    author="tianqiai",
    author_email="jiecai.shan@aminer.cn",
    url="https://github.com/shanjiecai/tianqiai-python",
)
