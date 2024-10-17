%define url_ver %(echo %{version} | cut -d. -f1-2)
%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1

%define major 0
%define api 3
%define girmajor 3.0

%define libname %mklibname %{name} %{api} %{major}
%define develname %mklibname %{name} %{api} -d
%define girname %mklibname %{name}-gir %{girmajor}

Summary:		Integrated development environment for C and C++ (Linux)
Name:			anjuta
Version:		3.34.0
Release:		2
License:		GPLv2+
Group:			Development/Other
URL:			https://anjuta.sourceforge.net/
Source0:		http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Source1:		anjuta.rpmlintrc

BuildRequires:	autogen
BuildRequires:	itstool
BuildRequires:	bison
BuildRequires:	desktop-file-utils
BuildRequires:	flex
BuildRequires:	gnome-common
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	imagemagick
BuildRequires:	intltool
BuildRequires:	openldap-devel
BuildRequires:	vala
BuildRequires:	gettext-devel
BuildRequires:	subversion-devel >= 1.5.0
BuildRequires:	vala-devel
BuildRequires:	pkgconfig(apr-1)
BuildRequires:	pkgconfig(apr-util-1)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) >= 2.0.0
BuildRequires:	pkgconfig(gdl-3.0) >= 2.91.4
BuildRequires:	pkgconfig(gladeui-2.0) >= 3.9.2
BuildRequires:	pkgconfig(glib-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gnome-doc-utils) >= 0.4.2
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires:	pkgconfig(gtksourceview-3.0) >= 2.91.8
BuildRequires:	pkgconfig(libdevhelp-3.0) >= 3.0.0
BuildRequires:	pkgconfig(libgda-5.0)
BuildRequires:	pkgconfig(libcgraph) >= 1.0
BuildRequires:	pkgconfig(libgvc) >= 1.0
BuildRequires:	pkgconfig(libxml-2.0) >= 2.4.23
BuildRequires:	pkgconfig(neon)
BuildRequires:	pkgconfig(vte-2.91) >= 0.29.0
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	yelp-tools yelp yelp-devel
BuildRequires:	python3dist(rope)

Requires:	autogen
Requires:	python-rope
#Requires:	typelib(St)

%description
Anjuta DevStudio is a versatile Integrated Development Environment (IDE)
on GNOME Desktop Environment and features a number of advanced
programming facilities. These include project management, application and
class wizards, an on-board interactive debugger, powerful source editor,
syntax highlighting, intellisense autocompletions, symbol navigation,
version controls, integrated GUI designing and other tools.

%package -n %{libname}
Summary:	Anjuta libraries
Group:		System/Libraries
Conflicts:	%{mklibname %{name} 0} < 3.1.3

%description -n %{libname}
Anjuta libraries.

%package -n %{develname}
Summary:	Anjuta devel files
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Anjuta devel files.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%prep
%setup -q
%autopatch -p1

%build
%configure \
	--enable-introspection=yes \
	--enable-compile-warnings=no

%make_build LIBS="-lrt -lutil"

%install
%make_install

desktop-file-install --vendor="" \
	--remove-key='Encoding' \
	--add-category="IDE" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

%find_lang %{name} --with-gnome --all-name

#we don't want these
find %{buildroot} -name "*.la" -exec rm -rf {} \;

#let files section handle docs
rm -fr %{buildroot}%{_docdir}/%{name}

%files -f %{name}.lang
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/metainfo/anjuta.appdata.xml
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/applications/*.desktop
%{_mandir}/man1/%{name}*.1*
%{_datadir}/mime/packages/anjuta.xml
%{_datadir}/pixmaps/%{name}
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/mimetypes/*

%files -n %{libname}
%{_libdir}/lib%{name}-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Anjuta-%{girmajor}.typelib
%{_libdir}/girepository-1.0/IAnjuta-%{girmajor}.typelib

%files -n %develname
%doc %{_datadir}/gtk-doc/html/lib%{name}
%{_libdir}/lib%{name}-%{api}.so
%{_includedir}/lib%{name}-3.0
%{_libdir}/pkgconfig/lib%{name}-3.0.pc
%{_datadir}/gir-1.0/Anjuta-%{girmajor}.gir
%{_datadir}/gir-1.0/IAnjuta-%{girmajor}.gir
