Name:		gnome-settings-daemon
Version:	2.23.91
Release:	3%{?dist}
Summary:	The daemon sharing settings from GNOME to GTK+/KDE applications

Group:		System Environment/Daemons
License:	GPLv2+
URL:		http://ftp.gnome.org/pub/gnome/sources/%{name}
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/2.23/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre): GConf2 >= 2.14
Requires(preun): GConf2 >= 2.14
Requires(post): GConf2 >= 2.14

BuildRequires:	dbus-glib-devel
BuildRequires:	GConf2-devel
BuildRequires:	gtk2-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	gnome-desktop-devel >= 2.23.91-3
BuildRequires:	libglade2-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	libgnome-devel
BuildRequires:	xorg-x11-proto-devel
BuildRequires:	gstreamer-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:	libgnomekbd-devel
BuildRequires:	libnotify-devel
BuildRequires:	gettext
BuildRequires:	perl(XML::Parser)
BuildRequires:  autoconf, automake, libtool, intltool

Patch2:         gnome-settings-daemon-2.21.91-ignore-model-if-evdev.patch
Patch6:		gnome-settings-daemon-2.23.4-drop-sample-cache.patch
Patch7:		gnome-settings-daemon-2.23.91-fnf7-cycle.patch

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

%patch2 -p1 -b .ignore-layout-if-using-evdev
%patch6 -p1 -b .drop-sample-cache
%patch7 -p0 -b .fnf7-cycle

%build
aclocal
automake
autoconf

%configure --enable-static=no --enable-profiling --disable-esd
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
rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-2.0/libsound.so
rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-2.0/sound.gnome-settings-plugin

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
	%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_keybindings.schemas \
	%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_screensaver.schemas \
	%{_sysconfdir}/gconf/schemas/desktop_gnome_font_rendering.schemas \
	%{_sysconfdir}/gconf/schemas/gnome-settings-daemon.schemas \
	>& /dev/null || :
touch %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%pre
if [ "$1" -gt 1 ]; then
	export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
	if [ -f %{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_default_editor.schemas ] ; then
		gconftool-2 --makefile-uninstall-rule \
			%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_default_editor.schemas \
			>& /dev/null || :
	fi
	gconftool-2 --makefile-uninstall-rule \
		%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_keybindings.schemas \
		%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_screensaver.schemas \
		%{_sysconfdir}/gconf/schemas/desktop_gnome_font_rendering.schemas \
		%{_sysconfdir}/gconf/schemas/gnome-settings-daemon.schemas \
		>& /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
	export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
	if [ -f %{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_default_editor.schemas ] ; then
		gconftool-2 --makefile-uninstall-rule \
			%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_default_editor.schemas \
			>& /dev/null || :
	fi
	gconftool-2 --makefile-uninstall-rule \
		%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_keybindings.schemas \
		%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_screensaver.schemas \
		%{_sysconfdir}/gconf/schemas/desktop_gnome_font_rendering.schemas \
		%{_sysconfdir}/gconf/schemas/gnome-settings-daemon.schemas \
		>& /dev/null || :
fi

%postun
touch %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS
%{_sysconfdir}/gconf/schemas/*
%{_libdir}/gnome-settings-daemon-2.0
%{_libexecdir}/gnome-settings-daemon
%{_datadir}/gnome-settings-daemon/
%{_datadir}/dbus-1/services/org.gnome.SettingsDaemon.service
%{_sysconfdir}/xdg/autostart/gnome-settings-daemon.desktop
%{_datadir}/icons/hicolor/*/apps/gsd-xrandr.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/gnome-settings-daemon-2.0
%{_libdir}/pkgconfig/gnome-settings-daemon.pc

%changelog
* Wed Sep 03 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.91-3
- Bump gnome-desktop requirement

* Wed Sep 03 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.91-2
- Add patch to do fn-f7 cycling

* Mon Sep 01 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Thu Aug 28 2008 Jon McCann <jmccann@redhat.com> - 2.23.91-0.2008.08.28.2
- BuildRequires libnotify-devel

* Thu Aug 28 2008 Jon McCann <jmccann@redhat.com> - 2.23.91-0.2008.08.28.1
- Update to snapshot

* Fri Aug 22 2008 Matthias Clasen <mclasne@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Thu Aug 14 2008 Lennart Poettering <lpoetter@redhat.com> - 2.23.6-3
- Rerun autotools after patching configure.ac

* Thu Aug 14 2008 Lennart Poettering <lpoetter@redhat.com> - 2.23.6-2
- Apply patch from gnome bug 545386. This hasn't been accepted in this form yet
  by upstream, will however very likely be merged in a similar form.
- Disable esd/sounds module since we don't need it to start PA anymore

* Tue Aug  5 2008 Matthias Clasen <mclasne@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Fri Jul 25 2008 Matthias Clasen <mclasne@redhat.com> - 2.23.5-3
- Use standard icon names in the volume OSD
 
* Fri Jul 25 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.5-2
- Fix build, call gtk-update-icon-cache as required

* Thu Jul 24 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Wed Jun 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Tue Jun 17 2008 Colin Walters <walters@redhat.com> - 2.23.3-2
- Add (now upstreamed) patch to legacy ESD preference; see
  http://bugzilla.gnome.org/show_bug.cgi?id=533198
  https://bugzilla.redhat.com/show_bug.cgi?id=430624

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Wed May 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-0.2008.05.14.2
- Fix BuildRequires

* Wed May 14 2008 Jon McCann <jmccann@redhat.com> - 2.23.2-0.2008.05.14.1
- Build snapshot

* Tue May 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1-5
- Rebuild

* Mon May  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1-4
- Pick up the keyboard layout from the login screen

* Mon May  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1-3
- Fix background drawing without nautilus

* Tue Apr 29 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.1.1-2
- Add patch from upstream to avoid the Stop button triggering an Eject (#346201)

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1.1-1
- Update to 2.23.1.1

* Tue Apr 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-2008.03.26.6
- Make the xrandr plugin survive the absence of Xrandr

* Sat Apr 5 2008 - Soren Sandmann <sandmann@redhat.com> - 2.22.1-2008.03.26.5
- Update randr plugin

* Mon Mar 31 2008 - Ray Strode <rstrode@redhat.com> - 2.22.1-0.2008.03.26.4
- Over the releases we've accumulated default.png, default-wide.png default-5_4.png
  and default.jpg.  We haven't been able to drop them because it would leave some
  users with white backgrounds on upgrade.  This patch just falls back to the
  default image if the user's background doesn't exist.

* Wed Mar 26 2008 - Bastien Nocera <bnocera@redhat.com> - 2.22.1-0.2008.03.26.3
- Add patch for the mouse plugin not to eat multimedia key events (#438942)

* Wed Mar 26 2008 Jon McCann <jmccann@redhat.com> - 2.22.1-0.2008.03.26.2
- Rebuild

* Wed Mar 26 2008 Jon McCann <jmccann@redhat.com> - 2.22.1-0.2008.03.26.1
- Update to snapshot
- Enable profiling

* Wed Mar 26 2008 - Bastien Nocera <bnocera@redhat.com> - 2.22.0-3
- apps_gnome_settings_daemon_default_editor.schemas is obsolete (#438937)

* Thu Mar 20 2008 Matthias Clasen <mclasen@redhat.com> 2.22.0-2
- Fix interaction between "Locate Pointer" and volume keys

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> 2.22.0-1
- Update to 2.22.0

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

