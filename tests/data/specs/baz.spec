Name:    baz
Version: 1
Release: 1
Summary: You gotta love Baz!

License: MIT
URL:     http://baz.inexistant-dummies.org

%description
You gotta love Baz!


%prep
# Nothing to do, that's a dummy package


%build
# Nothing to do, that's a dummy package


%install
install -d %{buildroot}%{_libdir}/%{name}/
cat >> %{buildroot}%{_libdir}/%{name}/some_resource << EOF
# Imagine there's actually something here...
#
# Something that might warrant reloading a service or whatever.
EOF

install -d %{buildroot}%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d
cat >> %{buildroot}%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d/%{name}.conf << EOF
[/usr/%%(libarch)s/%{name}]
exec=/bin/echo 'Got trigger on path using libarch'
EOF


%files
%{_libdir}/%{name}/some_resource
%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d/%{name}.conf


%changelog
* Wed Mar 14 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1-1
- Initial package.
