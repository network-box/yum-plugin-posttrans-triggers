Name:    machins
Version: 1
Release: 1
Summary: Get several Machins!

License: MIT
URL:     http://machins.inexistant-dummies.org

%description
Get several Machins!


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
[%{_datadir}/machin]
exec=/bin/echo "First trigger on %%(path)s"
EOF


%files
%{_datadir}/%{name}/some_resource
%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d/%{name}.conf


%changelog
* Wed Mar 14 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1-1
- Initial package.
