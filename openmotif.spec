Summary:	OpenMotif -
Summary(pl):	OpenMotif -
Name:		openmotif
Version:	2.1.30
Release:	1
Copyright:	Open Group Public License
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
Source0:	ftp://ftp.uk.linux.org/pub/linux/openmotif/source/%{name}-%{version}-src.tgz
Patch0:		openmotif-makedepend.patch
BuildRequires:	XFree86-devel
#Requires:	
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Motif is the user interface standart in the Enterprise for applications
that run on UNIX platforms for Sun, HP, IBM, Compaq, SGI, and others.

%description -l pl
Motif jest standartem wygl±du interfejsu graficznego dla aplikacji
dzia³aj±cych w ¶rodowiskach UNIX takich jak Sun, HP, IBM, Compaq, SGI i inne.


%package devel
Summary:	OpenMotif devel
Summary(pl):	OpenMotif devel
Group:		X11/Development/Libraries
Group(pl):	X11/Programowanie/Biblioteki
%description devel
%description -l pl devel

%package static
Summary:	OpenMotif static
Summary(pl):	OpenMotif static
Group:		X11/Development/Libraries
Group(pl):	X11/Programowanie/Biblioteki
%description static
%description -l pl static

%prep
%setup -q -n motif
%patch0 -p1

mkdir -p exports/{doc,include,lib,localized}
mkdir -p imports/x11
cd imports/x11
ln -s /usr/X11R6/bin bin                                   
ln -s /usr/X11R6/include include                          
ln -s /usr/X11R6/lib lib
cd ../../config/cf
ln -s /usr/X11R6/lib/X11/config/* . || :
cd ../..
mv Imakefile Imakefile.bak
sed -e 's/	\$(RM) -r \$(BUILDINCDIR)//' \
	-e 's/	\$(RM) -r \$(BUILDLIBDIR)//' \
	-e 's/	\$(RM) -r \$(BUILDDOCDIR)//' \
	-e 's/	\$(RM) -r \$(BUILDLOCDIR)//' \
	-e 's/WORLDOPTS =.*/WORLDOPTS = -S/' Imakefile.bak > Imakefile

%build
CXXEXTRA_DEFINES="-O2 -mpentium"
export CXXEXTRA_DEFINES
make World \
	IMAKE_DEFINES="-I/usr/X11R6/lib/X11/config -Dlinux -Di386" \
	"BOOTSTRAPCFLAGS=$RPM_OPT_FLAGS" \
	"CDEBUGFLAGS=" "CCOPTIONS=$RPM_OPT_FLAGS" \
	"CXXDEBUGFLAGS=" "CXXOPTIONS=$RPM_OPT_FLAGS" \
	"RAWCPP=/lib/cpp"

%install
rm -rf $RPM_BUILD_ROOT
make "DESTDIR=$RPM_BUILD_ROOT" \
	"INSTBINFLAGS=-m 755" \
	"INSTPGMFLAGS=-m 755" \
	"RAWCPP=/lib/cpp" \
	install install.man

%clean
rm -rf $RPM_BUILD_ROOT

%post devel
/sbin/ldconfig

%postun devel
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc
%attr(,,)

%files devel
%defattr(644,root,root,755)
%doc
%attr(,,)

%files static
%defattr(644,root,root,755)
%doc
%attr(,,)
