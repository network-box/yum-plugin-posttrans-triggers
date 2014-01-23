## About posttrans-triggers

RPM package maintainers are familiar with the various scriptlets to control an
RPM transaction, such as `%post`, `%postun`, `%posttrans`, etc...

One thing missing though, is the possibility to run some commands at the end
of a transaction, and **only once**.

Consider the following example:

* the package `httpd` provides the service `httpd.service`
* the packages `mod_perl` and `mod_ssl` provide resources for this service

When the `mod_perl` or `mod_ssl` modules are installed, updated or removed,
the service `httpd.service` should be reloaded. This could be effectively done
in the `%postun` or `%posttrans` scriplet of each package.

However, if both `mod_perl` and `mod_ssl` are present in the same transaction,
then `httpd.service` will be reloaded twice in a very short time, which might
cause some trouble. Even if it doesn't, it is inefficient.

This plugin allows packages to specify paths to be watched, and actions to
take after a transaction during which files matching those paths were changed.

Of course, each action will be executed only once, which means that in the
above example, `httpd.service` will only be reloaded once.

In essence, this plugin implements what `%posttrans` should really be.


## Install

To use this YUM plugin, you need:

* a RPM-managed operating system
* Yum == 3.2.29
  This is the version on EL 6, but it will probably work with other versions
  too, e.g on Fedora. I've simply never tested those, feedback is warmly
  welcome.
* Python == 2.6
  Again, this is the version on EL 6, but it would probably work with other
  versions. Let me know if you try it.

Installing this plugin from the sources should be as simple as running one
command, as root:

```
# python setup.py install
```

Hopefully, this plugin is already packaged in your favorite distribution, so
you can just run:

```
# yum install yum-plugin-posttrans-triggers
```


## Usage

The plugin is enabled by default, but won't do anything unless it is told to.

There are two ways to let the plugin know you want it to run the configured
triggers:

* only for one transaction, passing the `--posttrans-triggers` option to Yum
* permanently, by setting the `always_run_triggers` option to `1` in the
  `/etc/yum/pluginconf.d/posttrans-triggers.conf` file.


## Configuration syntax

Each watcher file must be installed in the
`/etc/yum/pluginconf.d/posttrans-triggers.conf.d/` folder and be named with
the `.conf` extension.

The syntax is very similar to the INI one:

```
[/path/to/watch]
exec=/path/to/command option1 option2
```

Each file can have as many sections as paths to watch.

Paths are watched recursively, and the section is in fact the **beginning** of
the path to watch. That means that the following paths will be matched by the
above example section:

* ``/path/to/watch``
* ``/path/to/watch/subfolder/file``
* ``/path/to/watched/file``
* ``/path/to/watch-anything/here/really``

One can specify as many commands to execute as desired, simply by specifying
more than one `exec=` line:

```
[/path/to/watch]
exec=/path/to/command option1 option2
exec=/path/to/anothercommand option3 option4
```

Of course, several files can watch the same path, and specify different
commands to be run.

If several triggers are configured with identical `exec=` commands, it will be
executed **only once**. As an example, the following commands are all
considered identical, since a shell would parse them all the same way:

```
exec= /bin/systemctl reload httpd.service
exec=/bin/systemctl  reload httpd.service
exec=/bin/systemctl reload  httpd.service
exec=/bin/systemctl reload 'httpd.service'
exec=/bin/systemctl reload "httpd.service"
```

The commands are executed in a minimal environment, not the full environment of
the parent process (`yum`). At the moment, the environment passed to each
command contains only the `LC_*` and `LANG` variables.

As a consequence, the `exec=` command must be specified with its full path,
since the `PATH` variable is removed from its environment before execution.

To implement the example cited in the preamble, the `httpd` package would
provide the `/etc/yum/pluginconf.d/posttrans-triggers.conf.d/httpd.conf` file
with the following content:

```
[/usr/%(libarch)/httpd/modules/]
exec=/bin/systemctl reload httpd.service
```

Then every time a package like `mod_perl`, containing an Apache module, gets
installed, updated or removed, the Apache server would reload all its modules
to take the change into account automatically.


## Legal

This project is distributed under the terms of the
[GNU General Public License version 3 or later](http://www.gnu.org/licenses/gpl.html).

It was written as part of my work at [Network Box](http://www.network-box.com)
as we needed it for our own products.

We do not require you to assign your copyright or sign a legal document of any
kind before accepting your contributions to this project, so send us patches
or pull requests!
