Name:    foo
Version: 2
Release: 1
Summary: Just foo! 

License: MIT
URL:     http://foo.inexistant-dummies.org

%description
Just foo!


%prep
# Nothing to do, that's a dummy package


%build
# Nothing to do, that's a dummy package


%install
install -d %{buildroot}%{_datadir}/%{name}-%{version}/
cat >> %{buildroot}%{_datadir}/%{name}-%{version}/some_resource << EOF
# Imagine there's actually something here...
#
# Something that might warrant reloading a service or whatever.
EOF

install -d %{buildroot}%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d
cat >> %{buildroot}%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d/%{name}.conf << EOF
[%{_datadir}/%{name}/]
exec=/bin/echo 'Got trigger on old path %%(path)s (file is %%(file)s)'

[%{_datadir}/%{name}-%{version}/]
exec=/bin/echo 'Got trigger on new path %%(path)s (file is %%(file)s)'
EOF


%files
%{_datadir}/%{name}-%{version}/some_resource
%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d/%{name}.conf


%changelog
* Thu Mar 15 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 2-1
- This is an update.

* Tue Mar 13 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1-1
- Initial package.
