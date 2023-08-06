"""Setup the package."""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Krijg het versienummer:
import re
VERSIONFILE = "mlflowcollab/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

# Hier moeten alle requirements komen te staan
requirements = ['pyperclip',
                'mlflow'
                ]

setuptools.setup(
    name="mlflowcollab",
    version=verstr,
    author="Sjoerd Gnodde",
    author_email="sgnodde@hhdelfland.nl",
    description="Gebruik MLFlow op een centrale locatie",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dev.azure.com/HWH-WE-DEEP/VV-WAM/_git/mlflowcollab",
    packages=['mlflowcollab'],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent"  
    ],
    python_requires='>=3.6',
)
