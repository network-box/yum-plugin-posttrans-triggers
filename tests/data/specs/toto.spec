Name:    toto
Version: 1
Release: 1
Summary: It's the story of Toto...

License: MIT
URL:     http://toto.inexistant-dummies.org

%description
It's the story of Toto...


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
[%{_datadir}]
exec=/bin/echo 'Got trigger on path %%(path)s (file is %%(file)s)'

[%{_datadir}/%{name}]
exec=/bin/echo 'Got trigger on path %%(path)s (file is %%(file)s)'
EOF


%files
%{_datadir}/%{name}/some_resource
%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d/%{name}.conf


%changelog
* Tue Mar 13 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1-1
- Initial package.
