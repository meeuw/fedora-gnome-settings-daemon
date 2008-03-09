Name:		gnome-settings-daemon
Version:	2.21.92
Release:	3%{?dist}
Summary:	The daemon sharing settings from GNOME to GTK+/KDE applications

Group:		System Environment/Daemons
License:	GPLv2+
URL:		http://ftp.gnome.org/pub/gnome/sources/%{name}
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/2.21/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre): GConf2 >= 2.14
Requires(preun): GConf2 >= 2.14
Requires(post): GConf2 >= 2.14

BuildRequires:	dbus-glib-devel
BuildRequires:	GConf2-devel
BuildRequires:	gtk2-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	gnome-desktop-devel >= 2.21.91
BuildRequires:	libglade2-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	libgnome-devel
BuildRequires:	xorg-x11-proto-devel
BuildRequires:	gstreamer-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	libgnomekbd-devel
BuildRequires:	gettext
BuildRequires:	perl(XML::Parser)

Patch1:         add-randr-12.patch
Patch2:         gnome-settings-daemon-2.21.91-ignore-model-if-evdev.patch

%description
A daemon to share settings from GNOME to other applications. It also
handles global keybindings, as well as a number of desktop-wide settings.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	dbus-glib-devel

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%patch1 -p1 -b .add-randr-12
%patch2 -p1 -b .ignore-layout-if-using-evdev

%build
%configure --enable-static=no
make %{?_smp_mflags}

cd po
# clean up .po files
make %{name}.pot
for p in *.po; do
  msgmerge -U $p %{name}.pot
done
# regenerate .gmo files
make
cd ..

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
	%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_default_editor.schemas \
	%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_keybindings.schemas \
	%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_screensaver.schemas \
	%{_sysconfdir}/gconf/schemas/desktop_gnome_font_rendering.schemas \
	%{_sysconfdir}/gconf/schemas/gnome-settings-daemon.schemas \
	>& /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
	export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
	gconftool-2 --makefile-uninstall-rule \
		%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_default_editor.schemas \
		%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_keybindings.schemas \
		%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_screensaver.schemas \
		%{_sysconfdir}/gconf/schemas/desktop_gnome_font_rendering.schemas \
		%{_sysconfdir}/gconf/schemas/gnome-settings-daemon.schemas \
		>& /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
	export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
	gconftool-2 --makefile-uninstall-rule \
		%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_default_editor.schemas \
		%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_keybindings.schemas \
		%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_screensaver.schemas \
		%{_sysconfdir}/gconf/schemas/desktop_gnome_font_rendering.schemas \
		%{_sysconfdir}/gconf/schemas/gnome-settings-daemon.schemas \
		>& /dev/null || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS
%{_sysconfdir}/gconf/schemas/*
%{_libdir}/gnome-settings-daemon-2.0
%{_libexecdir}/gnome-settings-daemon
%{_datadir}/gnome-settings-daemon/
%{_datadir}/dbus-1/services/org.gnome.SettingsDaemon.service

%files devel
%defattr(-,root,root,-)
%{_includedir}/gnome-settings-daemon-2.0
%{_libdir}/pkgconfig/gnome-settings-daemon.pc

%changelog
* Sun Mar  9 2008 Ray Strode <rstrode@redhat.com> - 2.21.92-3
- Don't set keyboard model on startup from gconf if evdev is being used.
  Evdev needs to use its own keyboard model to work right.

* Sun Mar  2 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.92-2
- Update randr patch to handle video key

* Fri Feb 29 2008 Jon McCann <jmccann@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Tue Feb 12 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.91-3
- Add patch to make the xrandr plugin listen for client messages from
  the control panel and reread the configuration file.

* Mon Feb 11 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-2
- Remove obsolete control-center translations

* Mon Feb 11 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.91-1
- Update to 2.21.91
- Remove obsolete patches

* Thu Feb  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90.1-3
- Load xkb settings initially

* Thu Jan 31 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.90.1-2
- Fix the path for g-s-d, from upstream patch

* Tue Jan 29 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.90.1-1
- Update to 2.21.90.1

* Tue Jan 29 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Tue Jan 15 2008  Matthias Clasen <mclasen@redhat.com> - 2.21.5.2-2
- Incorporate review feedback (#428833)

* Tue Jan 15 2008  Matthias Clasen <mclasen@redhat.com> - 2.21.5.2-1
- Update to 2.21.5.2

* Tue Jan 15 2008  Matthias Clasen <mclasen@redhat.com> - 2.21.5.1-1
- Update to 2.21.5.1
- Fix up BuildRequires

* Thu Dec 06 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.5-1
- First package

