from setuptools import setup, find_packages
import sys, os

version = '4.2'

setup(name='metnav',
      version=version,
      description="Facet Metadata Navigation from eXist and LOM-fr",
      long_description="""\
Facet Navigation on LOM / LOMfr (Learning Objects Metadata and french profile of Learning Objects Metadata) using choosen tags from LOM XMLschema, management of objects and articles related to the displayed page, frontline article or object, list of last articles introduced in the database. Prodiuct is best fitted with eXistDA product to be connected to eXist database.
""",
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Plone eXist-db facet navigation LOM LOM-fr',
      author='UNIS (ENS Lyon)',
      author_email='unis@ens-lyon.fr',
      url='http://unis.ens-lyon.fr',
      license='CeCILL-B',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'pisa',
          'reportlab',
          'html5lib',
          'z3c.form',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
