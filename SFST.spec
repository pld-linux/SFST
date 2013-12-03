Summary:	Stuttgart Finite State Transducer Tools
Summary(pl.UTF-8):	Stuttgart Finite State Transducer Tools - narzędzia do automatów skończonych
Name:		SFST
Version:	1.4.6g
Release:	2
License:	GPL v2+
Group:		Development/Tools
Source0:	ftp://ftp.ims.uni-stuttgart.de/pub/corpora/SFST/%{name}-%{version}.tar.gz
# Source0-md5:	574f124731ab1b87696fdd9b8a6e4a7d
Patch0:		build.patch
URL:		http://www.ims.uni-stuttgart.de/projekte/gramotron/SOFTWARE/SFST.html
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libstdc++-devel
BuildRequires:	m4
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SFST is a toolbox for the implementation of morphological analysers
and other tools which are based on finite state transducer technology.

The SFST tools comprise:
- a compiler which translates transducer programs into minimised
  transducers
- interactive and batch-mode analysis programs
- tools for comparing and printing transducers
- an efficient C++ transducer library

%description -l pl.UTF-8
SFST to zestaw narzędzi do implementowania analizatorów
morfologicznych i innych narzędzi opartych na automatach skończonych z
wyjściem.

Narzędzia SFST obejmują:
- kompilator tłumaczący programy na zminimalizowane automaty skończone
  z wyjściem
- interaktywne i wsadowe programy do analizy
- narzędzia do porównywania i wypisywania automatów
- wydajną bibliotekę automatów skończonych z wyjściem dla C++

%package devel
Summary:	Header files for SFST library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SFST
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for SFST library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SFST.

%prep
%setup -q -n %{name}
%patch0 -p1

sed -i -e '/^	strip/d' src/Makefile

%build
%{__make} -C src libsfst.so \
	CC="%{__cxx}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcxxflags} \$(WARNING) -DSGI__gnu_cxx -DREADLINE -fPIC" \
	LDFLAGS="%{rpmldflags}"

%{__make} -C src \
	CC="%{__cxx}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcxxflags} \$(WARNING) -DSGI__gnu_cxx -DREADLINE" \
	LDFLAGS="%{rpmldflags}" \
	LREADLINE="-lreadline"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix}/

%{__make} -C src maninstall \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_datadir}/

install -D src/libsfst.so $RPM_BUILD_ROOT%{_libdir}/libsfst.so

%{__make} -C src hfiles \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}/

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README doc/{SFST-Manual,SFST-Tutorial}.pdf
%attr(755,root,root) %{_bindir}/fst-*
%attr(755,root,root) %{_libdir}/libsfst.so
%{_mandir}/man1/fst-*.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/sfst
