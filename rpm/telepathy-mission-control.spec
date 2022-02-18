Name:       telepathy-mission-control

Summary:    Central control for Telepathy connection manager
Version:    5.16.6
Release:    1
License:    LGPLv2 and LGPLv2+
URL:        https://git.sailfishos.org/mer-core/telepathy-mission-control/
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.privileges
Patch0:     0001-Use-nemo-path-for-installed-tests.patch
Patch1:     0002-Disable-gtkdoc.patch
Patch2:     0003-McdSlacker-Revert-use-of-org.gnome.SessionManager-in.patch
Patch3:     0004-Add-mktests.sh-script.patch
Patch4:     0005-Introduce-a-systemd-service-for-mission-control-5.patch
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires:   mapplauncherd
BuildRequires:  pkgconfig(dbus-1) >= 0.95
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.82
BuildRequires:  pkgconfig(telepathy-glib) >= 0.19.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gmodule-no-export-2.0)
BuildRequires:  pkgconfig(gio-2.0) >= 2.28
BuildRequires:  pkgconfig(mce)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  libxslt
BuildRequires:  fdupes
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
# To build tests
BuildRequires:  python3-base
BuildRequires:  python3-twisted
BuildRequires:  dbus-python3

%description
Mission Control, or MC, is a Telepathy component providing a way for
"end-user" applications to abstract some of the details of connection
managers, to provide a simple way to manipulate a bunch of connection
managers at once, and to remove the need to have in each program the
account definitions and credentials.


%package tests
Summary:    Tests package for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   python3-base
Requires:   python3-twisted
Requires:   dbus-python3
Requires:   python3-gobject

%description tests
The %{name}-tests package contains tests and
tests.xml for automated testing.


%package devel
Summary:    Headers files for %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header
files for developing applications that use %{name}.


%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%autogen --disable-static \
--libdir=%{_libdir} \
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

install -d %{buildroot}%{_userunitdir}/user-session.target.wants/
ln -s ../mission-control-5.service %{buildroot}%{_userunitdir}/user-session.target.wants/mission-control-5.service

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} AUTHORS ChangeLog

mkdir -p %{buildroot}%{_datadir}/mapplauncherd/privileges.d
install -m 644 -p %{SOURCE1} %{buildroot}%{_datadir}/mapplauncherd/privileges.d/

# Plugin directory
mkdir -p %{buildroot}%{_libdir}/mission-control-plugins.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/mapplauncherd/privileges.d/*
%{_userunitdir}/mission-control-5.service
%{_userunitdir}/user-session.target.wants/mission-control-5.service
%{_libdir}/libmission-control-plugins.so.*
%{_libexecdir}/mission-control-5
# Own mission control plugins dir.
%dir %{_libdir}/mission-control-plugins.0

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
