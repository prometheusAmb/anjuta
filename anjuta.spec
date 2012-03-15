%define url_ver %(echo %{version} | cut -c 1-3)
%define major	0
%define api		3
%define gir_major	3.0

%define libname		%mklibname %{name} %{api} %{major}
%define develname	%mklibname %{name} %{api} -d
%define girname		%mklibname %{name}-gir %{gir_major}

Summary:	Integrated development environment for C and C++ (Linux)
Name:		anjuta
Version:	3.2.2
Release:	1
License:	GPLv2+
Group:		Development/Other
URL:		http://anjuta.sourceforge.net/
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		anjuta-3.2.1-format-strings.patch

BuildRequires:	autogen
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gnome-common
BuildRequires:	gettext-devel
BuildRequires:  gtk-doc
BuildRequires:  gnome-doc-utils
BuildRequires:  imagemagick
BuildRequires:  intltool
BuildRequires:	gobject-introspection-devel
BuildRequires:	subversion-devel
BuildRequires:	vala-devel
BuildRequires:	desktop-file-utils
BuildRequires:  pkgconfig(apr-1)
BuildRequires:  pkgconfig(apr-util-1)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gdl-3.0)
BuildRequires:  pkgconfig(gladeui-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtksourceview-3.0)
BuildRequires:  pkgconfig(libdevhelp-3.0)
BuildRequires:  pkgconfig(libgda-4.0)
BuildRequires:  pkgconfig(libgraph)
BuildRequires:  pkgconfig(libgvc)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(neon)
BuildRequires:  pkgconfig(vte-2.90)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xrender)

Requires:       autogen
Requires:       python-rope

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

%description -n %{libname}
Anjuta libraries

%package -n %{develname}
Summary:	Anjuta devel files
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Anjuta devel files

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
    --disable-static \
    --enable-introspection=yes

%make LIBS='-lgmodule-2.0 -lutil'

%install
rm -rf %{buildroot}
%makeinstall_std

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
%{_libdir}/glade/modules/libgladeanjuta.so
%{_datadir}/glade/catalogs/anjuta-glade.xml
%{_datadir}/%{name}
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/applications/*.desktop
%{_datadir}/icons/gnome/*/mimetypes/*
%{_mandir}/man1/%{name}*.1*
%{_datadir}/mime/packages/anjuta.xml
%{_datadir}/pixmaps/%{name}
%{_datadir}/icons/hicolor/*/apps/*

%files -n %{libname}
%{_libdir}/lib%{name}-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Anjuta-%{gir_major}.typelib
%{_libdir}/girepository-1.0/IAnjuta-%{gir_major}.typelib

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/lib%{name}
%{_libdir}/lib%{name}-%{api}.so
%{_includedir}/lib%{name}-3.0
%{_libdir}/pkgconfig/lib%{name}-3.0.pc
%{_datadir}/gir-1.0/Anjuta-%{gir_major}.gir
%{_datadir}/gir-1.0/IAnjuta-%{gir_major}.gir

