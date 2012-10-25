from setuptools import setup, find_packages


version = "0.1"


setup(
    name='collective.qna',
    version=version,
    description='Stackexchange-alike question and answer forum',
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python"],
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.app.contentlisting',
        'plone.app.dexterity',
        'plone.app.testing',
        'plone.app.theming',
        ],
    )
