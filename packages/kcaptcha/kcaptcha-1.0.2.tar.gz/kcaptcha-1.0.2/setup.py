from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="kcaptcha",
    version="1.0.2",
    author="xpc",
    description="kill captcha",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(where='.', exclude=(), include=('*',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'onnxruntime', 'Pillow', 'opencv-python', 'loguru'],
    python_requires='<3.10',
    include_package_data=True,
    install_package_data=True,
)
