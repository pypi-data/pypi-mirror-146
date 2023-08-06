import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="checkContaminants",
    version="0.99",
    author="Nishka Arora, Dr. Ashish Mahabal, Dr. Nitin Singh, Dr. Moogega Cooper",
    author_email="naarora@caltech.edu, aam@astro.caltech.edu, nitin.k.singh@jpl.nasa.gov, moogega.cooper@jpl.nasa.gov",
    description="Command Line Package that can be used to analyse locations datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/checkContaminants/checkSpaceContamination.git",
    project_urls={
        "Project URL": "https://github.com/checkContaminants/checkSpaceContamination",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    package_data={'':['data/*.csv', 'data/*.txt', 'test/data/*.csv', 'test/data/gentests/*.csv']},
    python_requires=">=3.6",
    install_requires=['pandas==1.3.4', 'numpy==1.21.2', 'tabulate==0.8.9', 'matplotlib==3.4.3', 
                        'matplotlib-venn==0.11.6'],
    entry_points = {
        'console_scripts': ['checkContaminants=checkContaminants.checkContaminants:main']
    },

    test_suite = 'nose.collector',
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
