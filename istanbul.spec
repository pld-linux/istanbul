Summary:	Desktop session recorder for the Free Desktop
Name:		istanbul
Version:	0.2.1
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://zaheer.merali.org/%{name}-%{version}.tar.bz2
# Source0-md5:	a28cad50f8e29bdce6f8a61af7932539
URL:		http://live.gnome.org/Istanbul
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
BuildRequires:	python-gnome-extras-devel
BuildRequires:	python-gstreamer >= 0.10
BuildRequires:	python-pygtk-gtk
%pyrequires_eq	python-libs
Requires:	gstreamer-theora
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Istanbul is a desktop session recorder for the Free Desktop.
It records your session into an Ogg Theora video file.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I common
%{__autoconf}
%{__automake}
%configure \
	--disable-gconftool
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}
%py_postclean $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install istanbul.schemas
/sbin/ldconfig

%postun
%gconf_schema_uninstall istanbul.schemas
/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README

%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/*
%attr(755,root,root) %{_libdir}/gstreamer-*/*.so*
%{_mandir}/man1/*
%{_pixmapsdir}/*
%{py_sitescriptdir}/%{name}
%{_sysconfdir}/gconf/schemas/*

%if %{with subpackage}
%files subpackage
%defattr(644,root,root,755)
#%doc extras/*.gz
#%{_datadir}/%{name}-ext
%endif
