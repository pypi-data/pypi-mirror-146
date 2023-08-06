# pylint: disable=W0622
"""cubicweb-subprocess application packaging information"""

modname = 'subprocess'
distname = 'cubicweb-subprocess'

numversion = (1, 2, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'This cube helps to manage and monitor subprocesses.'
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname

__depends__ = {'cubicweb': ">= 3.25.0, < 3.37.0",
               'cubicweb-file': '>= 1.16.0'}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: JavaScript',
    ]
