%define pkgname	mozjs
%define api			24.2
%define libmozjs24		%mklibname %{pkgname} %{api}
%define libmozjs24_devel	%mklibname %{pkgname} %{api} -d

Summary:	JavaScript interpreter and libraries
Name:		mozjs24
Version:	24.2.0
Release:	1%{?dist}
License:	MPLv2.0

URL:		http://www.mozilla.org/js/
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/mozjs-%{version}.tar.bz2
BuildRequires:	pkgconfig(nspr)
BuildRequires:	readline-devel
BuildRequires:	zip
BuildRequires:	python-devel

Patch0:		js17-build-fixes.patch
Patch1:		mozjs24-0001-Add-AArch64-support.patch

%description
JavaScript is the Netscape-developed object scripting language used in millions
of web pages and server applications worldwide. Netscape's JavaScript is a
super set of the ECMA-262 Edition 3 (ECMAScript) standard scripting language,
with only mild differences from the published standard.

%package -n %{libmozjs24}
Provides:	mozjs24 = %{EVRD}
Summary:	JavaScript engine library

%description -n %{libmozjs24}
JavaScript is the Netscape-developed object scripting language used in millions
of web pages and server applications worldwide. Netscape's JavaScript is a
super set of the ECMA-262 Edition 3 (ECMAScript) standard scripting language,
with only mild differences from the published standard.

%package -n %{libmozjs24_devel}
Summary: Header files, libraries and development documentation for %{name}
Provides:	mozjs24-devel = %{EVRD}
Requires: %{libmozjs24} = %{EVRD}

%description -n %{libmozjs24_devel}
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n mozjs-%{version}
# Delete bundled sources
rm js/src/editline -rf
rm js/src/ctypes/libffi -rf
%patch0 -p1
%patch1 -p1
chmod a+x configure

%build
%configure \
  --disable-static \
  --with-system-nspr \
  --enable-threadsafe \
  --enable-readline \
  --enable-xterm-updates
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
# For some reason the headers and pkg-config file are executable
find %{buildroot}%{_includedir} -type f -exec chmod a-x {} \;
chmod a-x  %{buildroot}%{_libdir}/pkgconfig/*.pc
# Upstream does not honor --disable-static yet
rm -f %{buildroot}%{_libdir}/*.a
# This is also statically linked; once that is fixed that we could
# consider shipping it.
rm -f %{buildroot}%{_bindir}/js24

# However, delete js-config since everything should use
# the pkg-config file.
rm -f %{buildroot}%{_bindir}/js24-config

%files -n %{libmozjs24}
%doc LICENSE README
%{_libdir}/*.so

%files -n %{libmozjs24_devel}
%{_libdir}/pkgconfig/*.pc
%{_includedir}/mozjs-24
