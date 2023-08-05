# pylint: disable=W0622
"""cubicweb-geocoding application packaging information"""

modname = 'geocoding'
distname = 'cubicweb-geocoding'

numversion = (0, 5, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'geocoding views such as google maps'
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]

__depends__ = {'cubicweb': ">= 3.24.0, < 3.38.0"}
__recommends__ = {}
