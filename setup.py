#!/usr/bin/env python
import os
from fnmatch import fnmatchcase

from setuptools import setup,find_packages
from distutils.util import convert_path

# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ["*.py", "*.pyc", "*~", ".*", "*.bak", "Makefile"]
standard_exclude_directories = [
    ".*", "CVS", "_darcs", "./build",
    "./dist", "EGG-INFO", "*.egg-info",
    "example"
]

# Copied from paste/util/finddata.py
def find_package_data(where=".", package="", exclude=standard_exclude,
        exclude_directories=standard_exclude_directories,
        only_in_packages=True, show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.
    
    The dictionary looks like::
    
        {"package": [files]}
    
    Where ``files`` is a list of all the files in that package that
    don't match anything in ``exclude``.
    
    If ``only_in_packages`` is true, then top-level directories that
    are not packages won't be included (but directories under packages
    will).
    
    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.
    
    If ``show_ignored`` is true, then all the files that aren't
    included in package data are shown on stderr (for debugging
    purposes).
    
    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.
    """
    
    out = {}
    stack = [(convert_path(where), "", package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "Directory %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                if (os.path.isfile(os.path.join(fn, "__init__.py"))
                    and not prefix):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + "." + name
                    stack.append((fn, "", new_package, False))
                else:
                    stack.append((fn, prefix + name + "/", package, only_in_packages))
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "File %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out


excluded_directories = standard_exclude_directories + ["./requirements", "./scripts"]
package_data = find_package_data(exclude_directories=excluded_directories)

METADATA = dict(
    name='django-allauth',
    version='0.4.0',
    author='Raymond Penners',
    author_email='raymond.penners@intenct.nl',
    description='Integrated set of Django applications addressing authentication, registration, account management as well as 3rd party (social) account authentication.',
    long_description=open('README.rst').read(),
    url='http://github.com/pennersr/django-allauth',
    keywords='django auth account social openid twitter facebook oauth registration',
    install_requires=['django', 
                      'oauth2', 
                      'python-openid',
                      'django-email-confirmation'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    packages=find_packages(),
    package_data=package_data
)

if __name__ == '__main__':
    setup(**METADATA)
    
