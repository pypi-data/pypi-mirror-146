from pathlib import Path
from setuptools import setup

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="auton_survival",
    version="0.0.5",
    description="Provides a flexible API for various problems in survival analysis, including regression, counterfactual estimation, and phenotyping.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://autonlab.github.io/auton-survival/",
    author="Chirag Nagpal",
    author_email="chiragn@cs.cmu.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=[
        "auton_survival",
        "auton_survival/models",
        "auton_survival/models/cmhe",
        "auton_survival/models/cph",
        "auton_survival/models/dcm",
        "auton_survival/models/dsm"
        ],
    include_package_data=True,
    install_requires=["torch", "numpy", "pandas", "tqdm", "scikit-learn", "torchvision", "scikit-survival", "matplotlib"],
)
