Summary:	OpenMotif -
Summary(pl):	OpenMotif -
Name:		openmotif
Version:	2.1.30
Release:	4
Copyright:	Open Group Public License
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
Source0:	ftp://ftp.uk.linux.org/pub/linux/openmotif/source/%{name}-%{version}-src.tgz
Source1:	openmotif-2.1.30-icsextra.tgz
Source2:	mwmrc
Source3:	mwm.RunWM
Source4:	mwm.wm_style
Patch0:		openmotif-makedepend.patch
Patch1:		openmotif-build.patch
Patch2:		openmotif-mwm.patch
Patch3:		openmotif-mwmrc.patch
BuildRequires:	XFree86-devel
BuildRequires:	byacc
Requires:	XFree86-libs
# Not restricted, lesstif provided library version 1.0.2
# OpenMotif provide library version 2.1
#Obsoletes:	lesstif
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Motif is the user interface standart in the Enterprise for applications
that run on UNIX platforms for Sun, HP, IBM, Compaq, SGI, and others.

%description -l pl
Motif jest standartem wygl±du interfejsu graficznego dla aplikacji
dzia³aj±cych w ¶rodowiskach UNIX takich jak Sun, HP, IBM, Compaq, SGI i inne.


%package clients
Summary:	Motif clients
Group:		X11/Applications
Group(pl):	X11/Aplikacje
Requires:	%{name} = %{version}
Obsoletes:	lesstif-clients

%description clients
Uil and xmbind.

%package devel
Summary:	OpenMotif devel
Summary(pl):	OpenMotif devel
Group:		X11/Development/Libraries
Group(pl):	X11/Programowanie/Biblioteki
Requires:	%{name} = %{version}
Provides:	motif-devel
Obsoletes:	lesstif-devel

%description devel

%description -l pl devel

%package static
Summary:	OpenMotif static
Summary(pl):	OpenMotif static
Group:		X11/Development/Libraries
Group(pl):	X11/Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}
Provides:	motif-static
Obsoletes:	lesstif-static

%description static

%description -l pl static

%package demos
Summary:	OpenMotif demos
Summary(pl):	OpenMotif demos
Group:		X11/Development/Libraries
Group(pl):	X11/Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description demos

%description -l pl demos

%package mwm
Summary:	Motif window manager
Group:		X11/Window Managers
Group(pl):	X11/Zarz±dcy Okien
Requires:	%{name} = %{version}
Requires:	wmconfig >= 0.9.9-5
Requires:	xinitrc >= 3.0
Obsoletes:	lesstif-mwm

%description mwm
A BETA release of mwm.  It is derived from fvwm, with a new parser that
understands mwmrc syntax, and a general understanding of Mwm resources.

%prep
%setup -q -n motif
%setup -q -n motif -T -D -b 1
rm -f config/cf/host.def
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

mkdir -p imports/x11
cd imports/x11
ln -s /usr/X11R6/include .
ln -s /usr/X11R6/lib .
cd ../../config/cf
mkdir OPENGROUP
mv *.tmpl *.rules *.def OPENGROUP
ln -s /usr/X11R6/lib/X11/config/* .
rm Motif.tmpl Motif.rules host.def
mv OPENGROUP/{Motif.tmpl,Motif.rules,host.def} .

%build
%{__make} World \
	IMAKE_DEFINES="-DYaccCmd=yacc" \
	"BOOTSTRAPCFLAGS=$RPM_OPT_FLAGS" \
	"CDEBUGFLAGS=" "CCOPTIONS=$RPM_OPT_FLAGS" \
	"CXXDEBUGFLAGS=" "CXXOPTIONS=$RPM_OPT_FLAGS" \
	"RAWCPP=/lib/cpp"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/motif,/etc/{sysconfig/wmstyle,X11/mwm}}

%{__make} "DESTDIR=$RPM_BUILD_ROOT" \
	"INSTBINFLAGS=-m 755" \
	"INSTPGMFLAGS=-m 755" \
	"RAWCPP=/lib/cpp" \
	install install.man

strip --strip-unneeded $RPM_BUILD_ROOT%{_bindir}/* || :
strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*

cp -a doc/man/* $RPM_BUILD_ROOT%{_mandir}
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/animate.1x \
	$RPM_BUILD_ROOT%{_mandir}/man1/xmanimate.1x

(cd demos
%{__make} clean
cp -a * $RPM_BUILD_ROOT%{_examplesdir}/motif/)

(cd doc/ps
find -name \*.Z -print | xargs uncompress
find -name \*.ps -print | xargs gzip -9nf)

install %{SOURCE2} $RPM_BUILD_ROOT/etc/X11/mwm/system.mwmrc

install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/wmstyle/mwm.sh
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/wmstyle/mwm.names

gzip -9nf doc/ps/README* LICENSE COPYRIGHT.MOTIF OPENBUGS README.ICS \
	doc/ics/*.txt RELNOTES \
	$RPM_BUILD_ROOT%{_mandir}/man*/*

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.gz COPYRIGHT.MOTIF.gz OPENBUGS.gz README.ICS.gz
%doc doc/ics/*.gz RELNOTES.gz
%dir %{_libdir}/X11/uid
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_includedir}/bitmaps/*
%{_libdir}/X11/bindings

%files clients
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/uil*
%attr(755,root,root) %{_bindir}/xmbind
%{_mandir}/man1/uil.1*
%{_mandir}/man1/xmbind.1*

%files devel
%defattr(644,root,root,755)
%doc doc/ps/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/Mrm
%{_includedir}/Xm
%{_includedir}/uil
%{_mandir}/man3/*
%{_mandir}/man5/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files demos
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/DNDDemo
%attr(755,root,root) %{_bindir}/airport
%attr(755,root,root) %{_bindir}/autopopups
%attr(755,root,root) %{_bindir}/dainput
%attr(755,root,root) %{_bindir}/dogs
%attr(755,root,root) %{_bindir}/draw
%attr(755,root,root) %{_bindir}/earth
%attr(755,root,root) %{_bindir}/exm_in_c
%attr(755,root,root) %{_bindir}/exm_in_uil
%attr(755,root,root) %{_bindir}/filemanager
%attr(755,root,root) %{_bindir}/fileview
%attr(755,root,root) %{_bindir}/getsubres
%attr(755,root,root) %{_bindir}/helloint
%attr(755,root,root) %{_bindir}/hellomotif
%attr(755,root,root) %{_bindir}/i18ninput
%attr(755,root,root) %{_bindir}/motifshell
%attr(755,root,root) %{_bindir}/onHelp
%attr(755,root,root) %{_bindir}/panner
%attr(755,root,root) %{_bindir}/periodic
%attr(755,root,root) %{_bindir}/piano
%attr(755,root,root) %{_bindir}/sampler2_0
%attr(755,root,root) %{_bindir}/setDate
%attr(755,root,root) %{_bindir}/simpleDemo
%attr(755,root,root) %{_bindir}/simpledrop
%attr(755,root,root) %{_bindir}/todo
%attr(755,root,root) %{_bindir}/wsm
%attr(755,root,root) %{_bindir}/xmanimate
%attr(755,root,root) %{_bindir}/xmapdef
%attr(755,root,root) %{_bindir}/xmfonts
%attr(755,root,root) %{_bindir}/xmforc
%attr(755,root,root) %{_bindir}/xmform
%{_libdir}/X11/app-defaults/Fileview
%{_libdir}/X11/app-defaults/Xmd*
%{_libdir}/X11/uid/*
%{_mandir}/man1/DNDDemo.1*
%{_mandir}/man1/autopopups.1*
%{_mandir}/man1/draw.1*
%{_mandir}/man1/earth.1*
%{_mandir}/man1/exm_in_c.1*
%{_mandir}/man1/exm_in_uil.1*
%{_mandir}/man1/filemanager.1*
%{_mandir}/man1/getsubres.1*
%{_mandir}/man1/helloint.1*
%{_mandir}/man1/i18ninput.1*
%{_mandir}/man1/panner.1*
%{_mandir}/man1/periodic.1*
%{_mandir}/man1/piano.1*
%{_mandir}/man1/sampler2_0.1*
%{_mandir}/man1/setDate.1*
%{_mandir}/man1/simpleDemo.1*
%{_mandir}/man1/simpledrop.1*
%{_mandir}/man1/todo.1*
%{_mandir}/man1/wsm.1*
%{_mandir}/man1/xmanimate.1*
%{_examplesdir}/motif

%files mwm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mwm
%dir /etc/X11/mwm
%config /etc/X11/mwm/*
%attr(755,root,root) /etc/sysconfig/wmstyle/*.sh
/etc/sysconfig/wmstyle/*.names
%{_libdir}/X11/app-defaults/Mwm
%{_mandir}/man1/mwm.1*
%{_mandir}/man4/*
