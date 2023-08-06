import setuptools
from atomquant.version import __version__

version_file = "atomquant/version.py"


def get_version():
    with open(version_file, "r") as f:
        exec(compile(f.read(), version_file, "exec"))
    return locals()["__version__"]


with open("readme.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = ["numpy", "opencv-python", "alfred-py"]

setuptools.setup(
    name="atomquant",
    version=get_version(),
    author="Lucas Jin",
    author_email="11@qq.com",
    install_requires=REQUIREMENTS,
    description="AtomQuant: Quantization For Human.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jinfagang/atomquant",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
)
