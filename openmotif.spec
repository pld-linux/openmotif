Summary:	OpenMotif -
Summary(pl):	OpenMotif -
Name:		openmotif
Version:	2.1.30
Release:	1
Copyright:	Open Group Public License
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
Source0:	ftp://ftp.uk.linux.org/pub/linux/openmotif/source/%{name}-%{version}-src.tgz
#Patch0:		
#BuildRequires:	
#Requires:	
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_prefix	/usr

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

#%patch

%build
CXXEXTRA_DEFINES="-O2 -mpentium"
export CXXEXTRA_DEFINES
imake -DUseInstalled -I/usr/X11R6/lib/X11/config -Iconfig/cf
#xmkmf
(cd config/util;imake -DUseInstalled -I/usr/X11R6/lib/X11/config -I../cf;make)
make Makefiles
#make depend
#make World
#./configure --prefix=%{_prefix}
#make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{_prefix} install

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
