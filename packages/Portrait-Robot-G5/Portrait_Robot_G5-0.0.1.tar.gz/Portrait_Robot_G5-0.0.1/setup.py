import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Portrait_Robot_G5",
    version = "0.0.1",
    author = "Canjura, Loisel, Ouaret, Gaun, Valente",
    author_email = "sonia-elizabeth.canjura-rodriguez@insa-lyon.fr",
    description = "4BIM project by group 5",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lina-ouaret/Project_4bim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.3',
    install_requires=[
        'keras',
        'tensorflow',
        'cv2',
        'scikit-image' 
    ]
)
