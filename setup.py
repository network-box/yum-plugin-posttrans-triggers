from distutils.core import setup, Command
from distutils.command.install import install as _install
import os


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()


class clean(Command):
    """A custom distutils command to clean the development tree."""
    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def _clean_path(self, endswith, dirname, fnames):
        for fname in fnames:
            if fname.endswith(endswith):
                path = os.path.join(dirname, fname)
                print("cleaning %s" % os.path.relpath(path))
                os.unlink(path)

    def run(self):
        import shutil

        for path in ["build", "dist", "tests/data/specs/BUILD",
                    "tests/data/specs/BUILDROOT", "tests/data/specs/RPMS"]:
            if os.path.isdir(path):
                print("cleaning %s" % path)
                shutil.rmtree(path)

        for path in ["MANIFEST"]:
            if os.path.isfile(path):
                print("cleaning %s" % path)
                os.unlink(path)

        os.path.walk("tests/data/specs", self._clean_path, ".rpm")
        os.path.walk(".", self._clean_path, ".pyc")
        os.path.walk(".", self._clean_path, ".pyo")

class install(_install):
    """Specialized installer.

    The YUM plugins are not installed in the regular Python modules tree.
    """
    def initialize_options(self):
        _install.initialize_options(self)
        # Remove this line and self.root defaults to '.', which is not desired
        self.root = '/'

    def run(self):
        # Install the plugin code
        yumplugins_coderoot = os.path.join(self.root, "usr/lib/yum-plugins/")
        self.mkpath(yumplugins_coderoot, mode=0755)
        self.copy_file("posttrans-triggers.py", yumplugins_coderoot,
                       preserve_mode=0)

        # Install the plugin conf
        yumplugins_confroot = os.path.join(self.root, "etc/yum/pluginconf.d/")
        self.mkpath(yumplugins_confroot, mode=0755)
        self.copy_file("posttrans-triggers.conf", yumplugins_confroot,
                       preserve_mode=0)

        # Install the triggers dir
        self.mkpath(os.path.join(yumplugins_confroot,
                                 "posttrans-triggers.conf.d"),
                    mode=755)

class test(Command):
    """A custom distutils command to run unit tests."""
    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        """Run all the unit tests found in the `tests/' folder."""
        import sys
        import unittest

        if os.getuid() != 0:
            print("Unit tests must unfortunately be run as root")
            sys.exit(1)

        # FIXME: There has to be a way to run the unit tests against the
        #        development tree
        yumplugins_coderoot = "/usr/lib/yum-plugins/"
        if not os.path.exists(os.path.join(yumplugins_coderoot,
                                           "posttrans-triggers.py")):
            print("Unit tests require the plugin to be installed")
            sys.exit(1)

        print("\nWarning:\n--------\n    Unit tests are run against the " \
              "system-installed version of the plugin\n")
        raw_input("    Press any key to continue...\n")

        import tests

        loader = unittest.TestLoader()
        t = unittest.TextTestRunner(verbosity=self.verbose)
        result = t.run(loader.loadTestsFromModule(tests))

        if result.errors or result.failures:
            sys.exit(1)


setup(name='yum-plugin-posttrans-triggers',
        version='2.1',
        description='Run some file triggers after a yum transaction',
        long_description=README,
        classifiers=[
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python",
            "Topic :: System :: Installation/Setup",
            "Topic :: System :: Software Distribution",
            "Topic :: System :: Systems Administration",
            ],
        author='Mathieu Bridon',
        author_email='bochecha@fedoraproject.org',
        url='https://gitorious.org/yum-plugin-posttrans-triggers/yum-plugin-posttrans-triggers',
        license='GPLv3+',
        py_modules=['posttrans-triggers'],
        requires = [
            # The following are not available as distutils modules, but listing
            # them here seems like the nice thing to do for package maintainers
            # "yum>=3.2.29", # Not tested with older releases (that means RHEL6)
            ],
        cmdclass={
            "clean": clean, 'install': install, 'test': test,
            },
        )
