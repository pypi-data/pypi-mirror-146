from setuptools import setup

with open("PYPI.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

tests_require=['pytest', 'pytest-mock']

setup(
    name="gpulink",
    version="0.2.0",
    author="Philip Klaus",
    description="A simple tool for monitoring and displaying GPU stats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PhilipKlaus/gpu-link",
    project_urls={
        "Bug Tracker": "https://github.com/PhilipKlaus/gpu-link/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['gpulink', 'gpulink.cli'],
    python_requires=">=3.6",
    install_requires=[
        "pynvml >= 11.4.1",
        "matplotlib >= 3.5.1",
        "numpy >= 1.22.2",
        "tabulate >= 0.8.9",
        "colorama >= 0.4.4"
    ],
    tests_require=tests_require,
    extras_require={"test": tests_require},
    entry_points={
        'console_scripts': ['gpulink=gpulink.__main__:main'],
    },

)
