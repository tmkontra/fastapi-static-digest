import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastapi-static-digest",
    version="1.0.0",
    author="Tyler M Kontra",
    author_email="tyler@tylerkontra.com",
    description="Static file digest cache busting for FastAPI/Starlette",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Source': 'https://github.com/ttymck/fastapi-static-digest',
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'starlette'   
    ]
)