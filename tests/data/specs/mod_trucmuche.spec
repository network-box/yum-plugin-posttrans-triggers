Name:    mod_trucmuche
Version: 1
Release: 1
Summary: A module for Trucmuche

License: MIT
URL:     http://mod_trucmuche.inexistant-dummies.org

%description
A module for Trucmuche.


%prep
# Nothing to do, that's a dummy package


%build
# Nothing to do, that's a dummy package


%install
install -d %{buildroot}%{_datadir}/trucmuche-modules/
cat >> %{buildroot}%{_datadir}/trucmuche-modules/some_resource << EOF
# Imagine there's actually something here...
#
# Something that might warrant reloading a service or whatever.
EOF


%files
%{_datadir}/trucmuche-modules/some_resource


%changelog
* Wed Mar 14 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 1-1
- Initial package.
