About posttrans-triggers
========================

RPM package maintainers are familiar with the various scriptlets to control an
RPM transaction, such as %post, %postun, %posttrans, etc...

One thing missing though, is the possibility to run some commands at the end
of a transaction, and **only once**.

Consider the following case:

* the package ``A`` provides the service ``A.service``
* the packages ``B`` and ``C`` provide resources for this service

When ``B`` or ``C`` are installed/updated/removed, ``A.service`` should be
reloaded. This could be effectively done in ``%postun``, as is advised in the
Fedora packaging guidelines.

However, if both ``B`` and ``C`` are changed in the same transaction, then
``A.service`` will be reloaded twice in a very short time, which might cause
some trouble.

This plugin allows packages to specify files to be watched, and an action to
take after a transaction which saw those changed.

Install
=======

To use this YUM plugin, you need:

    - a RPM-managed operating system
    - YUM >= 3.2.29 (this is the version of RHEL 6)

Installing this plugin from the sources should be as simple as running one
command, as root::

    # python setup.py install

As for any Python module using Distutils, you can optionally specify the
installation root::

    # python setup.py install --root=/my/own/root

Hopefully, this plugin is already packaged in your favorite distribution, so
you can just run::

    # yum install yum-plugin-posttrans-triggers


Usage
=====

The plugin is enabled by default, but won't do anything unless it is told to.

There are two ways to let the plugin know you want it to run the configured
triggers:

* only for one transaction, passing the ``--posttrans-triggers`` option to YUM
* permanently, by setting the ``always_run_triggers`` option to ``1`` in the
* ``/etc/yum/pluginconf.d/posttrans-triggers.conf`` file.


Legal
=====

This project is distributed under the terms of the `GNU General Public License version 3 or later`_.

It was written as part of my work at `Network Box`_ as we needed it for our
own products.

We do not require you to assign your copyright or sign a legal document of any
kind before accepting your contributions to this project, so send us patches!

. _GNU General Public License version 3 or later: http://www.gnu.org/licenses/gpl.html

. _Network Box: http://www.network-box.com
