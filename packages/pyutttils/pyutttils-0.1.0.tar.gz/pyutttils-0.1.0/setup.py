import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyutttils",  # Replace with your own username
    version="0.1.0",
    author="Ivann LARUELLE",
    author_email="ivann@laruelle.me",
    description="Package de fonctions utilitaires pour l'Université de Technologie de Troyes (UTT)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/larueli/pyutttils",
    packages=setuptools.find_packages(exclude=["docs"]),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    python_requires='>=3.6',
)
