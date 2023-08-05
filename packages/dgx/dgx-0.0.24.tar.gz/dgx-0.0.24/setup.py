from setuptools import setup, find_packages

long_desc = ""
with open('./README.md') as fl:
    long_desc = fl.read()

version = ""
with open('./dgx/_version.py') as f:
    dic = dict()
    exec(f.read(), dic)
    version = dic['__version__']

setup(
    name='dgx',
    packages=find_packages(
        include=["dgx", "dgx.*"]
    ),
    version=version,
    license='MIT',
    description='Dealergeek API',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Jeff Aguilar',
    author_email='jeff.aguilar.06@gmail.com',
    url='https://github.com/jaguilar08/dgx',
    download_url='https://github.com/jaguilar08/dgx/archive/refs/tags/0.1.tar.gz',
    keywords=['DEALERGEEK', 'API'],
    install_requires=[
        'Werkzeug',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'dgx = dgx.__main__:main',
        ]
    }
)
