import setuptools
import ark_server

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ark-server-CERTIC",
    version=ark_server.version,
    author="Mickaël Desfrênes",
    author_email="mickael.desfrenes@unicaen.fr",
    description="Ark server library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.unicaen.fr/pdn-certic/ark",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "psycopg2-binary",
        "sanic",
        "aiopg",
        "asyncio-extras",
        "argh",
        "hashids==1.3.1",
        "python-dotenv",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": ["ark=ark_server.__main__:run_cli"],
    },
)
