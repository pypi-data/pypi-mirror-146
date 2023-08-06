from setuptools import setup, find_packages



VERSION = '0.0.1'
DESCRIPTION = 'Generate csv,xlxs,excel,pdf and html file from python dictionary objects'
LONG_DESCRIPTION = 'A package that allows to create CSV, XML, PDF ,Excel and HTML file'

# Setting up
setup(
    name="object_to_xfile",
    version=VERSION,
    author="Sachin Indoriya",
    author_email="sachinindoriya63@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas','xml','pdfkit','flatten_json','dicttoxml'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)