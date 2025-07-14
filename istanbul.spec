Summary:	Desktop session recorder for the Free Desktop
Summary(pl.UTF-8):	Narzędzie do nagrywania sesji graficznych
Name:		istanbul
Version:	0.2.2
Release:	11
License:	GPL v2
Group:		X11/Applications
Source0:	http://zaheer.merali.org/%{name}-%{version}.tar.bz2
# Source0-md5:	8ddcfd5a29dcd10fdafc10af9f66848b
Patch0:		%{name}-quality.patch
Patch1:		%{name}-build.patch
Patch2:		%{name}-debian.patch
URL:		http://live.gnome.org/Istanbul
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
BuildRequires:	python-Xlib >= 0.13
BuildRequires:	python-gnome-extras-devel
BuildRequires:	python-gstreamer-devel >= 0.10
BuildRequires:	python-pygtk-gtk
BuildRequires:	rpm-pythonprov
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	GConf2
%pyrequires_eq	python-libs
Requires:	gstreamer-GConf
Requires:	gstreamer-imagesink-x
Requires:	gstreamer-theora
Requires:	gstreamer-vorbis
Requires:	python-Xlib >= 0.13
Requires:	python-gnome-extras-egg
Requires:	python-gstreamer >= 0.10
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Istanbul is a desktop session recorder for the Free Desktop. It
records your session into an Ogg Theora video file.

%description -l pl.UTF-8
Istanbul to narzędzie do nagrywania sesji graficznych. Nagrywa sesje
do plików filmów w formacie Ogg Theora.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
for a in `cat debian/patches/series`; do
	patch -p1 < debian/patches/$a || exit 1
done

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

[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}

rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-*/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install istanbul.schemas
/sbin/ldconfig

%preun
%gconf_schema_uninstall istanbul.schemas

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_libdir}/gstreamer-*/*.so*
%{_mandir}/man1/*.1*
%{_desktopdir}/istanbul.desktop
%{_pixmapsdir}/istanbul.png
%{py_sitescriptdir}/%{name}
%{_sysconfdir}/gconf/schemas/istanbul.schemas
