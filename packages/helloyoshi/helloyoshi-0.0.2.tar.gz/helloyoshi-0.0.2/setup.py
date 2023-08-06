from setuptools import setup, find_packages
import codecs
import os


#To create package
# pip3 install wheel
# python3 setup.py sdist bdist_wheel

#To install locally and check
#Navigate to dist directory
#keep an eye on version
# pip install helloyoshi-0.0.2-py3-none-any.whl
#or for force reinstall
# pip install helloyoshi-0.0.2-py3-none-any.whl --force-reinstall
#after this you can 
# cd ..
# python
# import helloyoshi
# helloyoshi.sayhello(5)
# a = helloyoshi.hy()
# a.working(6)


#To upload package
# pip3 install twine
# twine upload dist/*



# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Basic Hello Package'
LONG_DESCRIPTION = 'Basic Hello Package from Yoshi Bansal'

# Setting up
setup(
    name="helloyoshi",
    version=VERSION,
    author="Yoshi Bansal",
    author_email="<bansalyoshi@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas'],
    keywords=['python', 'hello', 'yoshi', 'bansal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)