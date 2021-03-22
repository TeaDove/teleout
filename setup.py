import setuptools


setuptools.setup(
    name="teleout", 
    version="0.0.1",
    author="Peter Ibragimov",
    author_email="peter.ibragimov@gmail.com",
    description="Terminal utility, for sending data directly to telegram users via pipes, files(pure and ziped) or just text.",
    url="https://github.com/TeaDove/teleout",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: UNIX",
    ],
    python_requires='>=3.7',
    entry_points = {
        'console_scripts': ['teleout=teleout.main:main']
    },
    install_requires=[
        "pyrogram>=1.0.7",
        "tgcrypto"
    ]
)
