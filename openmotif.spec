#
# WARNING: BETA versions of openmotif are using higher soname
# than STABLE one so please don't use beta versions here because
# when stable version somes out everything would need to be recompiled
# using ,,stable soname''. Check out CURRENT= in configure.{in,ac}.
#
Summary:	OpenMotif
Summary(pl.UTF-8):	OpenMotif
Name:		openmotif
Version:	2.3.1
Release:	2
License:	Open Group Public License
Group:		X11/Libraries
Source0:	ftp://ftp.ics.com/openmotif/2.3/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b6acc7fecec611bc39b1b3f4b2a0e452
#Source1:	%{name}-%{version}-icsextra.tgz
Source2:	mwmrc
Source3:	mwm.RunWM
Source5:	mwm-xsession.desktop
Source6:	ac_find_motif.m4
Patch0:		%{name}-makedepend.patch
Patch1:		%{name}-mwmrc.patch
Patch2:		%{name}-bison.patch
Patch3:		%{name}-freetype.patch
Patch4:		%{name}-parbuild.patch
Patch5:		%{name}-libtool.patch
URL:		http://www.openmotif.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	freetype-devel
BuildRequires:	libtool
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	pkgconfig
BuildRequires:	xorg-data-xbitmaps
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXp-devel
Requires:	%{name}-libs = %{version}-%{release}
Provides:	motif = 2.3
# Not restricted, lesstif provided library version 1.2
# OpenMotif provide library version 2.1
#Obsoletes:	lesstif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

%define		xbitmapsdir	%{_includedir}/X11/bitmaps
%define		xlibdir		%{_libdir}/X11

%description
Motif is the user interface standart in the Enterprise for
applications that run on UNIX platforms for Sun, HP, IBM, Compaq, SGI,
and others.

%description -l pl.UTF-8
Motif jest standardem wyglądu interfejsu graficznego dla aplikacji
działających w środowiskach UNIX takich jak Sun, HP, IBM, Compaq, SGI
i inne.

%package clients
Summary:	OpenMotif clients
Summary(pl.UTF-8):	OpenMotif - programy klienckie
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Obsoletes:	lesstif-clients

%description clients
Uil and xmbind.

%description clients -l pl.UTF-8
uil i xmbind.

%package libs
Summary:	OpenMotif shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone OpenMotif
Group:		Libraries
Conflicts:	openmotif < 2.2.3-0.3

%description libs
OpenMotif shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone OpenMotif.

%package devel
Summary:	OpenMotif devel
Summary(pl.UTF-8):	Pliki nagłówkowe OpenMotif
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	xorg-lib-libXmu-devel
Requires:	xorg-lib-libXp-devel
Provides:	motif-devel = 2.3
Obsoletes:	lesstif-devel

%description devel
Header files for OpenMotif.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla bibliotek OpenMotif.

%package static
Summary:	OpenMotif static
Summary(pl.UTF-8):	Statyczne biblioteki OpenMotif
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	motif-static = 2.3
Obsoletes:	lesstif-static

%description static
OpenMotif static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne OpenMotif.

%package demos
Summary:	OpenMotif demos
Summary(pl.UTF-8):	Programy demonstracyjne do OpenMotif
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description demos
OpenMotif demos.

%description demos -l pl.UTF-8
Programy demonstracyjne do OpenMotif.

%package mwm
Summary:	Motif window manager
Summary(pl.UTF-8):	Motifowy zarządca okien
Group:		X11/Window Managers
Requires:	%{name} = %{version}-%{release}
Obsoletes:	lesstif-mwm

%description mwm
A BETA release of mwm. It is derived from fvwm, with a new parser that
understands mwmrc syntax, and a general understanding of Mwm
resources.

%description mwm -l pl.UTF-8
Wersja BETA mwm. Pochodzi z fvwm, ma nowy parser rozumiejący składnię
mwmrc oraz zasoby Mwm.

%package compat
Summary:	Fake OpenMotif compat libraries
Summary(pl.UTF-8):	Dowiązania udające biblioteki kompatybilności OpenMotif
Group:		Libraries
Requires:	%{_libdir}/libXm.so.4.0.1
%ifarch %{x8664} ia64 ppc64 s390x sparc64
Provides:	libXm.so.1()(64bit)
Provides:	libXm.so.2()(64bit)
Provides:	libXm.so.3()(64bit)
%else
Provides:	libXm.so.1
Provides:	libXm.so.2
Provides:	libXm.so.3
%endif

%description compat
Fake OpenMotif compat libraries (symlinks to current libXm library,
_some_ old programs may work with them).

%description compat -l pl.UTF-8
Dowiązania udające biblioteki kompatybilności OpenMotif (dowiązania
symboliczne do nowej wersji biblioteki libXm, _niektóre_ stare
programy mogą z nimi działać).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__libtoolize}
%{__aclocal} -I .
%{__autoconf}
%{__autoheader}
%{__automake}
%{__autoconf}

%configure \
	--enable-shared \
	--enable-static \
	--enable-xft \
	--enable-jpeg \
	--enable-png \
	--with-fontconfig-config="pkg-config fontconfig"

%{__make} clean
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/motif,%{_datadir}/xsessions} \
	$RPM_BUILD_ROOT{/etc/{sysconfig/wmstyle,X11/mwm},%{_aclocaldir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	bmdir=%{xbitmapsdir} \
	binddir=%{xlibdir}/bindings

cd demos
%{__make} clean
cp -a * $RPM_BUILD_ROOT%{_examplesdir}/motif
rm -rf $RPM_BUILD_ROOT%{_datadir}/Xm
cd ..
mv -f $RPM_BUILD_ROOT%{_bindir}/{,openmotif-}column || :
mv -f $RPM_BUILD_ROOT%{_bindir}/{,openmotif-}tree || :

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/X11/mwm/system.mwmrc

install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/wmstyle/mwm.sh
install %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/xsessions/mwm.desktop
install %{SOURCE6} $RPM_BUILD_ROOT%{_aclocaldir}

ln -sf libXm.so.4.0.1 $RPM_BUILD_ROOT%{_libdir}/libXm.so.3
ln -sf libXm.so.4.0.1 $RPM_BUILD_ROOT%{_libdir}/libXm.so.2
ln -sf libXm.so.4.0.1 $RPM_BUILD_ROOT%{_libdir}/libXm.so.1

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs	-p /sbin/ldconfig
%postun	libs	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE COPYRIGHT.MOTIF RELNOTES
%{xbitmapsdir}/*
%{xlibdir}/bindings

%files clients
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/uil*
%attr(755,root,root) %{_bindir}/xmbind
%{_mandir}/man1/uil.1*
%{_mandir}/man1/xmbind.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libMrm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libMrm.so.4
%attr(755,root,root) %{_libdir}/libUil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libUil.so.4
%attr(755,root,root) %{_libdir}/libXm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libXm.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libMrm.so
%attr(755,root,root) %{_libdir}/libUil.so
%attr(755,root,root) %{_libdir}/libXm.so
%{_libdir}/libMrm.la
%{_libdir}/libUil.la
%{_libdir}/libXm.la
%{_includedir}/Mrm
%{_includedir}/Xm
%{_includedir}/uil
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_aclocaldir}/ac_find_motif.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/libMrm.a
%{_libdir}/libUil.a
%{_libdir}/libXm.a

%files demos
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/DNDDemo
%attr(755,root,root) %{_bindir}/airport
%attr(755,root,root) %{_bindir}/autopopups
%attr(755,root,root) %{_bindir}/bboxdemo
%attr(755,root,root) %{_bindir}/colordemo
%attr(755,root,root) %{_bindir}/openmotif-column
%attr(755,root,root) %{_bindir}/combo
%attr(755,root,root) %{_bindir}/draw
%attr(755,root,root) %{_bindir}/earth
%attr(755,root,root) %{_bindir}/ext18list
%attr(755,root,root) %{_bindir}/filemanager
%attr(755,root,root) %{_bindir}/fileview
%attr(755,root,root) %{_bindir}/fontsel
%attr(755,root,root) %{_bindir}/getsubres
%attr(755,root,root) %{_bindir}/helloint
%attr(755,root,root) %{_bindir}/hellomotif
%attr(755,root,root) %{_bindir}/i18ninput
%attr(755,root,root) %{_bindir}/iconbuttondemo
%attr(755,root,root) %{_bindir}/outline
%attr(755,root,root) %{_bindir}/paned
%attr(755,root,root) %{_bindir}/panner
%attr(755,root,root) %{_bindir}/periodic
%attr(755,root,root) %{_bindir}/piano
%attr(755,root,root) %{_bindir}/sampler2_0
%attr(755,root,root) %{_bindir}/setDate
%attr(755,root,root) %{_bindir}/simpledrop
%attr(755,root,root) %{_bindir}/tabstack
%attr(755,root,root) %{_bindir}/todo
%attr(755,root,root) %{_bindir}/tooltips
%attr(755,root,root) %{_bindir}/openmotif-tree
%attr(755,root,root) %{_bindir}/wsm
%attr(755,root,root) %{_bindir}/xmanimate
%{_examplesdir}/motif

%files mwm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mwm
%dir %{_sysconfdir}/X11/mwm
%config %{_sysconfdir}/X11/mwm/*
%attr(755,root,root) /etc/sysconfig/wmstyle/*.sh
%{_datadir}/xsessions/mwm.desktop
%{_mandir}/man1/mwm.1*
%{_mandir}/man4/*

%files compat
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXm.so.1
%attr(755,root,root) %{_libdir}/libXm.so.2
%attr(755,root,root) %{_libdir}/libXm.so.3
