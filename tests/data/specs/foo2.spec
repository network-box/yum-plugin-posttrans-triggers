Name:    foo2
Version: 1
Release: 1
Summary: Just foo, but better!

License: MIT
URL:     http://foo2.inexistant-dummies.org

Obsoletes: foo

%description
Just foo!


%prep
# Nothing to do, that's a dummy package


%build
# Nothing to do, that's a dummy package


%install
install -d %{buildroot}%{_datadir}/%{name}/
cat >> %{buildroot}%{_datadir}/%{name}/some_resource << EOF
# Imagine there's actually something here...
#
# Something that might warrant reloading a service or whatever.
EOF

install -d %{buildroot}%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d
cat >> %{buildroot}%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d/%{name}.conf << EOF
[%{_datadir}/foo/]
exec=/bin/echo 'Got trigger on obsolete path %%(path)s (file is %%(file)s)'

[%{_datadir}/%{name}/]
exec=/bin/echo 'Got trigger on new path %%(path)s (file is %%(file)s)'
EOF


%files
%{_datadir}/%{name}/some_resource
%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d/%{name}.conf


%changelog
* Thu Mar 15 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1-1
- Initial package.
