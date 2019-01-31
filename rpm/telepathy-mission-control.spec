Name:       telepathy-mission-control

Summary:    Central control for Telepathy connection manager
Version:    5.15.0
Release:    1
Group:      System/Libraries
License:    LGPLv2.1 and LGPLv2.1+
URL:        http://telepathy.freedesktop.org/wiki/Mission_Control/
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.privileges
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(dbus-1) >= 0.95
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.82
BuildRequires:  pkgconfig(telepathy-glib) >= 0.19.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gmodule-no-export-2.0)
BuildRequires:  pkgconfig(gio-2.0) >= 2.28
BuildRequires:  pkgconfig(mce)
BuildRequires:  libxslt
BuildRequires:  python
BuildRequires:  fdupes
BuildRequires:  python-twisted
BuildRequires:  dbus-python

%description
Mission Control, or MC, is a Telepathy component providing a way for
"end-user" applications to abstract some of the details of connection
managers, to provide a simple way to manipulate a bunch of connection
managers at once, and to remove the need to have in each program the
account definitions and credentials.


%package tests
Summary:    Tests package for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   python-twisted
Requires:   dbus-python
Requires:   pygobject2

%description tests
The %{name}-tests package contains tests and
tests.xml for automated testing.


%package devel
Summary:    Headers files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header
files for developing applications that use %{name}.


%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.

%prep
%setup -q -n %{name}-%{version}/telepathy-mission-control

%build
%autogen --disable-static \
--disable-gtk-doc \
--with-accounts-cache-dir=/tmp \
--disable-Werror \
--with-connectivity=connman \
--disable-conn-setting \
--enable-installed-tests \
--disable-gtk-doc

make %{?_smp_mflags}

tests/twisted/mktests.sh > tests/tests.xml

%install
rm -rf %{buildroot}
%make_install

%fdupes %{buildroot}/%{_datadir}/gtk-doc/
%fdupes %{buildroot}/%{_includedir}
install -m 0644 tests/tests.xml %{buildroot}/opt/tests/telepathy-mission-control/tests.xml
install -m 0644 tests/README %{buildroot}/opt/tests/telepathy-mission-control/README

install -d %{buildroot}%{_libdir}/systemd/user/user-session.target.wants/
ln -s ../mission-control-5.service %{buildroot}%{_libdir}/systemd/user/user-session.target.wants/mission-control-5.service

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} AUTHORS ChangeLog

mkdir -p %{buildroot}%{_datadir}/mapplauncherd/privileges.d
install -m 644 -p %{SOURCE1} %{buildroot}%{_datadir}/mapplauncherd/privileges.d/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/mapplauncherd/privileges.d/*
%{_libdir}/systemd/user/mission-control-5.service
%{_libdir}/systemd/user/user-session.target.wants/mission-control-5.service
%{_libdir}/libmission-control-plugins.so.*
%{_libexecdir}/mission-control-5

%files tests
%defattr(-,root,root,-)
/opt/tests/telepathy-mission-control

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libmission-control-plugins.so

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/mc-tool.1.*
%{_mandir}/man1/mc-wait-for-name.1.*
%{_mandir}/man8/mission-control-5.8.*
%{_docdir}/%{name}-%{version}
