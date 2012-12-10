%define url_ver %(echo %{version} | cut -c 1-3)

%define major		0
%define api		3
%define girmajor	3.0

%define libname		%mklibname %{name} %{api} %{major}
%define develname	%mklibname %{name} %{api} -d
%define girname		%mklibname %{name}-gir %{girmajor}

Summary:        Integrated development environment for C and C++ (Linux)
Name:           anjuta
Version:        3.6.2
Release:        1
License:        GPLv2+
Group:          Development/Other
URL:            http://anjuta.sourceforge.net/
Source0:        http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	autogen
BuildRequires:	itstool
BuildRequires:	bison
BuildRequires:	desktop-file-utils
BuildRequires:	flex
BuildRequires:	gnome-common
BuildRequires:  gtk-doc >= 1.0
BuildRequires:  imagemagick
BuildRequires:  intltool
BuildRequires:  vala
BuildRequires:	gettext-devel
BuildRequires:	subversion-devel >= 1.5.0
BuildRequires:	vala-devel
BuildRequires:  pkgconfig(apr-1)
BuildRequires:  pkgconfig(apr-util-1)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.0.0
BuildRequires:  pkgconfig(gdl-3.0) >= 2.91.4
BuildRequires:  pkgconfig(gladeui-2.0) >= 3.9.2
BuildRequires:  pkgconfig(glib-2.0) >= 2.28.0
BuildRequires:  pkgconfig(gnome-doc-utils) >= 0.4.2
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires:  pkgconfig(gtksourceview-3.0) >= 2.91.8
BuildRequires:  pkgconfig(libdevhelp-3.0) >= 3.0.0
BuildRequires:  pkgconfig(libgda-4.0) >= 4.2.0
BuildRequires:  pkgconfig(libgraph) >= 1.0
BuildRequires:  pkgconfig(libgvc) >= 1.0
BuildRequires:  pkgconfig(libxml-2.0) >= 2.4.23
BuildRequires:  pkgconfig(neon)
BuildRequires:  pkgconfig(vte-2.90) >= 0.27.6
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
Summary:        Anjuta libraries
Group:          System/Libraries
Conflicts:	%{mklibname %{name} 0} < 3.1.3

%description -n %{libname}
Anjuta libraries

%package -n %{develname}
Summary:        Anjuta devel files
Group:          Development/Other
Requires:       %{libname} = %{version}-%{release}
Requires:       %{girname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{develname}
Anjuta devel files

%package -n %{girname}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%prep
%setup -q

%build
%configure2_5x \
    --disable-static \
    --enable-introspection=yes
%make

%install
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
%{_libdir}/girepository-1.0/Anjuta-%{girmajor}.typelib
%{_libdir}/girepository-1.0/IAnjuta-%{girmajor}.typelib

%files -n %develname
%doc %{_datadir}/gtk-doc/html/lib%{name}
%{_libdir}/lib%{name}-%{api}.so
%{_includedir}/lib%{name}-3.0
%{_libdir}/pkgconfig/lib%{name}-3.0.pc
%{_datadir}/gir-1.0/Anjuta-%{girmajor}.gir
%{_datadir}/gir-1.0/IAnjuta-%{girmajor}.gir



%changelog
* Wed Aug 01 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.4-1
+ Revision: 811506
- update to new version 3.4.4

* Tue May 22 2012 Götz Waschk <waschk@mandriva.org> 3.4.3-1
+ Revision: 799991
- update to new version 3.4.3

* Fri May 18 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.2-1
+ Revision: 799454
- update to new version 3.4.2

  + Alexander Khrukin <akhrukin@mandriva.org>
    - verson update 3.4.1

* Thu Mar 15 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.2.2-1
+ Revision: 785034
- imported package anjuta

