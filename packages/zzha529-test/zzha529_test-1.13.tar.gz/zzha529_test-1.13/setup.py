import setuptools

setuptools.setup(
    name="zzha529_test",
    version="1.13",
    author="zzha529",
    description="personal redis queue consumer",
    long_description="personal redis queue consumer",
    packages=setuptools.find_packages(),
    install_requires=["redis==4.1.0"],
    python_requires=">3",
)

