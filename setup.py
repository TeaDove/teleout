import setuptools


setuptools.setup(
    name="teleout", 
    version="1.0.1",
    author="Peter Ibragimov",
    author_email="peter.ibragimov@gmail.com",
    description="Terminal utility, for sending data directly to telegram users via pipes, files(pure and ziped) or just text.",
    url="https://github.com/TeaDove/teleout",
    download_url='https://github.com/TeaDove/teleout/archive/v1.0.1.tar.gz',
    licence='gpl-3.0',
    keywords = ['TELEGRAM', 'PIPE', 'UTILITY'],   
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Topic :: Utilities'
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
