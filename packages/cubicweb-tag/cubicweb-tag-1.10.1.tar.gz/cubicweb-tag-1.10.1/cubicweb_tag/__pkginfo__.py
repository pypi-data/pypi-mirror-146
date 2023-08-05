# pylint: disable-msg=W0622
"""cubicweb-tag packaging information"""

modname = 'tag'
distname = "cubicweb-%s" % modname

numversion = (1, 10, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
description = "tag component for the CubicWeb framework"
author = "Logilab"
author_email = "contact@logilab.fr"
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname
classifiers = [
           'Environment :: Web Environment',
           'Framework :: CubicWeb',
           'Programming Language :: Python',
           'Programming Language :: JavaScript',
           ]

__depends__ = {'cubicweb': ">= 3.24.0, < 3.33.0"}
