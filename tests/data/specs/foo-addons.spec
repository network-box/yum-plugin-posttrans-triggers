Name:    foo-addons
Version: 1
Release: 1
Summary: Just foo some more!! 

License: MIT
URL:     http://foo-addons.inexistant-dummies.org

%description
Just foo some more!


%prep
# Nothing to do, that's a dummy package


%build
# Nothing to do, that's a dummy package


%install
install -d %{buildroot}%{_datadir}/foo/
cat >> %{buildroot}%{_datadir}/foo/some_other_resource << EOF
# Imagine there's actually something here...
#
# Something that might warrant reloading a service or whatever.
EOF

install -d %{buildroot}%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d
cat >> %{buildroot}%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d/%{name}.conf << EOF
[%{_datadir}/foo]
exec=/bin/echo 'Got addons trigger on path %%(path)s (file is %%(file)s)'
EOF


%files
%{_datadir}/foo/some_other_resource
%{_sysconfdir}/yum/pluginconf.d/posttrans-triggers.conf.d/%{name}.conf


%changelog
* Wed Mar 14 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1-1
- Initial package.
