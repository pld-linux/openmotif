Summary:	OpenMotif
Summary(pl):	OpenMotif
Name:		openmotif
Version:	2.2.3
Release:	2
License:	Open Group Public License
Group:		X11/Libraries
Source0:	http://ftp.ics.com/pub/Products/Motif/om%{version}/src/openMotif-%{version}.tar.gz
# Source0-md5:	94c96a0f94ee0d5e41d3dba2188b263d
#Source1:	%{name}-%{version}-icsextra.tgz
Source2:	mwmrc
Source3:	mwm.RunWM
Source4:	mwm.wm_style
Source5:	mwm-xsession.desktop
Source6:	ac_find_motif.m4
Patch0:		%{name}-makedepend.patch
Patch1:		%{name}-am-uil.patch
Patch2:		%{name}-mwmrc.patch
Patch3:		%{name}-gcc34.patch
#Patch1:	%{name}-build.patch
#Patch2:	%{name}-mwm.patch
#Patch4:	%{name}-ppc_fix.patch
#Patch5:	%{name}-ac-fixes.patch
#Patch6:	%{name}-am-demos.patch
#Patch8:	%{name}-am-animate.patch
URL:		http://www.openmotif.org/
BuildRequires:	XFree86
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	libtool
Requires:	%{name}-libs = %{version}-%{release}
Provides:	motif = 2.2
# Not restricted, lesstif provided library version 1.2
# OpenMotif provide library version 2.1
#Obsoletes:	lesstif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# FHS compliance
# (software must not be installed through /usr/{lib,include}/X11 links)
%define		xbitmapsdir	/usr/X11R6/include/X11/bitmaps
%define		xlibdir		/usr/X11R6/lib/X11

%description
Motif is the user interface standart in the Enterprise for
applications that run on UNIX platforms for Sun, HP, IBM, Compaq, SGI,
and others.

%description -l pl
Motif jest standardem wygl±du interfejsu graficznego dla aplikacji
dzia³aj±cych w ¶rodowiskach UNIX takich jak Sun, HP, IBM, Compaq, SGI
i inne.

%package clients
Summary:	OpenMotif clients
Summary(pl):	OpenMotif - programy klienckie
Group:		X11/Applications
Requires:	%{name} = %{version}
Obsoletes:	lesstif-clients

%description clients
Uil and xmbind.

%description clients -l pl
uil i xmbind.

%package devel
Summary:	OpenMotif devel
Summary(pl):	Pliki nag³ówkowe OpenMotif
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	XFree86-devel
Provides:	motif-devel = 2.1
Obsoletes:	lesstif-devel

%description devel
Header files for OpenMotif.

%description devel -l pl
Pliki nag³ówkowe dla bibliotek OpenMotif.

%package static
Summary:	OpenMotif static
Summary(pl):	Statyczne biblioteki OpenMotif
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}
Provides:	motif-static
Obsoletes:	lesstif-static

%description static
OpenMotif static libraries.

%description static -l pl
Biblioteki statyczne OpenMotif.

%package demos
Summary:	OpenMotif demos
Summary(pl):	Programy demonstracyjne do OpenMotif
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description demos
OpenMotif demos.

%description demos -l pl
Programy demonstracyjne do OpenMotif.

%package libs
Summary:	OpenMotif shared libraries
Summary(pl):	Biblioteki wspó³dzielone OpenMotif
Group:		Libraries
Conflicts:	openmotif < 2.2.3-0.3

%description libs
OpenMotif shared libraries.

%description libs -l pl
Biblioteki wspó³dzielone OpenMotif.

%package mwm
Summary:	Motif window manager
Summary(pl):	Motifowy zarz±dca okien
Group:		X11/Window Managers
Requires:	%{name} = %{version}
Requires:	xinitrc >= 3.0
Obsoletes:	lesstif-mwm

%description mwm
A BETA release of mwm. It is derived from fvwm, with a new parser that
understands mwmrc syntax, and a general understanding of Mwm
resources.

%description mwm -l pl
Wersja BETA mwm. Pochodzi z fvwm, ma nowy parser rozumiej±cy sk³adniê
mwmrc oraz zasoby Mwm.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}

%configure \
	--enable-shared \
	--enable-static

%{__make} clean
%{__make}

# workaround - don't let rebuild onHelp with wrong options during %%install
#touch demos/lib/Xmd/onHelp.o demos/lib/Xmd/onHelp

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
cd ..

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/X11/mwm/system.mwmrc

install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/wmstyle/mwm.sh
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/wmstyle/mwm.names
install %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/xsessions/mwm.desktop
install %{SOURCE6} $RPM_BUILD_ROOT%{_aclocaldir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs	-p /sbin/ldconfig
%postun	libs	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE COPYRIGHT.MOTIF OPENBUGS RELNOTES
#%dir %{_libdir}/X11/uid
%{xbitmapsdir}/*
%{xlibdir}/bindings

%files clients
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/uil*
%attr(755,root,root) %{_bindir}/xmbind
%{_mandir}/man1/uil.1*
%{_mandir}/man1/xmbind.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/Mrm
%{_includedir}/Xm
%{_includedir}/uil
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_aclocaldir}/*.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files demos
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/DNDDemo
%attr(755,root,root) %{_bindir}/airport
%attr(755,root,root) %{_bindir}/autopopups
#%attr(755,root,root) %{_bindir}/dainput
#%attr(755,root,root) %{_bindir}/dogs
%attr(755,root,root) %{_bindir}/draw
%attr(755,root,root) %{_bindir}/earth
#%attr(755,root,root) %{_bindir}/exm_in_c
#%attr(755,root,root) %{_bindir}/exm_in_uil
%attr(755,root,root) %{_bindir}/filemanager
%attr(755,root,root) %{_bindir}/fileview
%attr(755,root,root) %{_bindir}/getsubres
%attr(755,root,root) %{_bindir}/helloint
%attr(755,root,root) %{_bindir}/hellomotif
%attr(755,root,root) %{_bindir}/i18ninput
#%attr(755,root,root) %{_bindir}/motifshell
#%attr(755,root,root) %{_bindir}/onHelp
%attr(755,root,root) %{_bindir}/panner
%attr(755,root,root) %{_bindir}/periodic
%attr(755,root,root) %{_bindir}/piano
%attr(755,root,root) %{_bindir}/sampler2_0
%attr(755,root,root) %{_bindir}/setDate
#%attr(755,root,root) %{_bindir}/simpleDemo
%attr(755,root,root) %{_bindir}/simpledrop
%attr(755,root,root) %{_bindir}/todo
%attr(755,root,root) %{_bindir}/wsm
%attr(755,root,root) %{_bindir}/xmanimate
#%attr(755,root,root) %{_bindir}/xmapdef
#%attr(755,root,root) %{_bindir}/xmfonts
#%attr(755,root,root) %{_bindir}/xmforc
#%attr(755,root,root) %{_bindir}/xmform
#%%{_libdir}/X11/app-defaults/Fileview
#%%{_libdir}/X11/app-defaults/Xmd*
#%%{_libdir}/X11/uid/*
#%%{_mandir}/man1/DNDDemo.1*
#%%{_mandir}/man1/autopopups.1*
#%%{_mandir}/man1/draw.1*
#%%{_mandir}/man1/earth.1*
#%%{_mandir}/man1/exm_in_c.1*
#%%{_mandir}/man1/exm_in_uil.1*
#%%{_mandir}/man1/filemanager.1*
#%%{_mandir}/man1/getsubres.1*
#%%{_mandir}/man1/helloint.1*
#%%{_mandir}/man1/i18ninput.1*
#%%{_mandir}/man1/panner.1*
#%%{_mandir}/man1/periodic.1*
#%%{_mandir}/man1/piano.1*
#%%{_mandir}/man1/sampler2_0.1*
#%%{_mandir}/man1/setDate.1*
#%%{_mandir}/man1/simpleDemo.1*
#%%{_mandir}/man1/simpledrop.1*
#%%{_mandir}/man1/todo.1*
#%%{_mandir}/man1/wsm.1*
#%%{_mandir}/man1/xmanimate.1*
%{_examplesdir}/motif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files mwm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mwm
%dir %{_sysconfdir}/X11/mwm
%config %{_sysconfdir}/X11/mwm/*
%attr(755,root,root) /etc/sysconfig/wmstyle/*.sh
/etc/sysconfig/wmstyle/*.names
%{_datadir}/xsessions/mwm.desktop
%{_mandir}/man1/mwm.1*
%{_mandir}/man4/*
