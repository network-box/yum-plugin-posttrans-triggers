Name:    bidule
Version: 1
Release: 1
Summary: Get a Bidule!

License: MIT
URL:     http://bidule.inexistant-dummies.org

%description
Get a Bidule!


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
[%{_datadir}/%{name}]
exec=/bin/ls /path/to/inexistent/file
EOF


%files
%{_datadir}/%{name}/some_resource
%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d/%{name}.conf


%changelog
* Tue Mar 13 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1-1
- Initial package.
