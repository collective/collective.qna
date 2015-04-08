from setuptools import setup, find_packages


version = "0.1"


setup(
    name='collective.qna',
    version=version,
    description='Stackexchange-alike question and answer forum',
    long_description=open("README.rst").read() + "\n" +
                     open("CHANGES.txt").read(),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python"],
    keywords='plone qna question answer',
    author='Jamie Lentin',
    author_email='plone-developers@lists.sourceforge.net',
    url='http://pypi.python.org/pypi/collective.qna',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.app.contentlisting',
        'plone.app.dexterity',
        'plone.app.testing',
        'plone.app.theming',
        ],
    extras_require={
        'test': [
            'plone.app.testing',
        ]
    },
    entry_points="""
        [z3c.autoinclude.plugin]
        target = collective
    """,
    )
