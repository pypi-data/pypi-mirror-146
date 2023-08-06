import setuptools
import numpy

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="merlin-ts",
    packages=["merlin-ts"],
    version="0.0.1",
    setup_requires=["numpy"],
    install_requires=["numpy", "scipy"],
    include_dirs=[numpy.get_include()],
    long_description=long_description,
    author="Xinye Chen",
    maintainer="Xinye Chen",
    
    classifiers=["Intended Audience :: Science/Research",
                "Intended Audience :: Developers",
                "Programming Language :: Python",
                "Topic :: Software Development",
                "Topic :: Scientific/Engineering",
                "Operating System :: Microsoft :: Windows",
                "Operating System :: Unix",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                ],
    author_email="xinye.chen@manchester.ac.uk",
    maintainer_email="xinye.chen@manchester.ac.uk",
    description="Massive time series anomalies detection of arbitrary length",
    long_description_content_type='text/markdown',
    url="https://github.com/nla-group/slearn.git",
    license='MIT License'
)