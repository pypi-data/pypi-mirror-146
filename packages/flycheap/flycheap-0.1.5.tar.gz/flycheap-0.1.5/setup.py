from setuptools import setup, find_packages
with open('README.md', "r", encoding = "utf-8") as file:
    readme = file.read()
setup(
    name = 'flycheap', 
    version = '0.1.5', 
    author = 'Primarie', 
    author_email = "SyzygyPrimarie@gmail.com",
    description = "Flight Tickets Price Collection, Statistics and Analysis based on ctrip.com",
    url = r"https://github.com/LF502/FlyCheap", 
    python_requires = ">=3.6", 
    long_description = readme, 
    long_description_content_type = 'text/markdown', 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"], 
    package_dir={"": "src"},
    packages = find_packages(where="src"),
    install_requires = ['requests', 'json5', 'openpyxl', 'pandas']
    )