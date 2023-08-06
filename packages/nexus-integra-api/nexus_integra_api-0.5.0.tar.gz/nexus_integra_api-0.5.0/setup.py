from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='nexus_integra_api',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    version='0.5.0',
    description='Nexus API connection methods and utilities',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://nexusintegra.io',
    install_requires=['pandas', 'requests'],
    setup_requires=[],
    test_requires=['python-dotenv', 'unitest'],
    author='Nexus Integra',
    author_email='laura.moreno@nexusintegra.io',
    license='UNLICENSED: private Nexus Integra',
)
