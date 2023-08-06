from setuptools import setup


setup(
    name='LoadAndSplit',
    version="1.0",
    keywords=["test", "xxx"],
    author_email="fcwyzzr@163.com",
    packages=['LoadAndSplit'],
    license="GPL Licence",
    requires=['numpy', 'collections'],
    install_requires=['numpy'],
    package_data={'LoadAndSplit': ['Default_Model.pkl']}
)
