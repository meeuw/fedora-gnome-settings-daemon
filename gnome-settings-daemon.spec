Name:           gnome-settings-daemon
Version:        3.3.3.1
Release:        2%{?dist}
Summary:        The daemon sharing settings from GNOME to GTK+/KDE applications

Group:          System Environment/Daemons
License:        GPLv2+
URL:            http://download.gnome.org/sources/%{name}
#VCS: git:git://git.gnome.org/gnome-settings-daemon
Source:         http://download.gnome.org/sources/%{name}/3.3/%{name}-%{version}.tar.xz

# Fedora specific patch
Patch0: gsd-calculator.patch

Requires: control-center-filesystem

BuildRequires:  dbus-glib-devel
BuildRequires:  gtk3-devel >= 2.99.3
BuildRequires:  gnome-desktop3-devel >= 3.1.4
BuildRequires:  xorg-x11-proto-devel libXxf86misc-devel
BuildRequires:  xorg-x11-proto-devel libXxf86misc-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libgnomekbd-devel
BuildRequires:  libnotify-devel
BuildRequires:  gettext intltool
BuildRequires:  fontconfig-devel
BuildRequires:  libcanberra-devel
BuildRequires:  polkit-devel
# BuildRequires:  autoconf automake libtool
BuildRequires:  libxklavier-devel
BuildRequires:  gsettings-desktop-schemas-devel >= 0.1.7
BuildRequires:  PackageKit-glib-devel
BuildRequires:  cups-devel
BuildRequires:  upower-devel
BuildRequires:  libgudev1-devel
BuildRequires:  nss-devel
BuildRequires:  colord-devel >= 0.1.12
BuildRequires:  lcms2-devel >= 2.2
BuildRequires:  libXi-devel libXfixes-devel
BuildRequires:  libwacom-devel

%description
A daemon to share settings from GNOME to other applications. It also
handles global keybindings, as well as a number of desktop-wide settings.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       dbus-glib-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .calc

rm data/gnome-settings-daemon.desktop.in

autoreconf -i -f

%build
%configure --disable-static \
           --enable-profiling \
           --enable-packagekit
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Remove the useless xrdb plugin
#rm -rf $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-3.0/*xrdb* \
#        $RPM_BUILD_ROOT%{_sysconfdir}/xrdb/

%find_lang %{name} --with-gnome

mkdir $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-3.0/gtk-modules

%post
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS
%dir %{_sysconfdir}/gnome-settings-daemon
%dir %{_sysconfdir}/gnome-settings-daemon/xrandr

# list plugins explicitly, so we notice if one goes missing
# some of these don't have a separate gschema
%{_libdir}/gnome-settings-daemon-3.0/a11y-keyboard.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/liba11y-keyboard.so

# The automount plugin is a separate executable used in fallback
# mode only
%{_libexecdir}/gnome-fallback-mount-helper
%{_sysconfdir}/xdg/autostart/gnome-fallback-mount-helper.desktop

%{_libdir}/gnome-settings-daemon-3.0/background.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libbackground.so

%{_libdir}/gnome-settings-daemon-3.0/clipboard.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libclipboard.so

%{_libdir}/gnome-settings-daemon-3.0/housekeeping.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libhousekeeping.so
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.housekeeping.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/keyboard.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libkeyboard.so
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.keyboard.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/media-keys.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libmedia-keys.so
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.media-keys.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/mouse.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libmouse.so

%{_libexecdir}/gsd-backlight-helper
%{_datadir}/polkit-1/actions/org.gnome.settings-daemon.plugins.power.policy
%{_libdir}/gnome-settings-daemon-3.0/power.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libpower.so
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.power.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/print-notifications.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libprint-notifications.so
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.print-notifications.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/smartcard.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libsmartcard.so

%{_libdir}/gnome-settings-daemon-3.0/sound.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libsound.so

%{_libdir}/gnome-settings-daemon-3.0/updates.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libupdates.so
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.updates.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/wacom.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libgsdwacom.so
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.peripherals.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.peripherals.wacom.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/xrandr.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libxrandr.so
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.xrandr.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/xsettings.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libxsettings.so
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.xsettings.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/a11y-settings.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/liba11y-settings.so

%{_libdir}/gnome-settings-daemon-3.0/color.gnome-settings-plugin
%{_libdir}/gnome-settings-daemon-3.0/libcolor.so
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.color.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/liborientation.so
%{_libdir}/gnome-settings-daemon-3.0/orientation.gnome-settings-plugin
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.orientation.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/libcursor.so
%{_libdir}/gnome-settings-daemon-3.0/cursor.gnome-settings-plugin

%{_libexecdir}/gnome-settings-daemon
%{_libexecdir}/gsd-locate-pointer
%{_libexecdir}/gsd-printer

%{_datadir}/gnome-settings-daemon/
%{_datadir}/dbus-1/services/org.gnome.SettingsDaemon.service
%{_sysconfdir}/xdg/autostart/gnome-settings-daemon.desktop
%{_datadir}/icons/hicolor/*/apps/gsd-xrandr.*
%{_libexecdir}/gsd-datetime-mechanism
%{_sysconfdir}/dbus-1/system.d/org.gnome.SettingsDaemon.DateTimeMechanism.conf
%{_datadir}/dbus-1/system-services/org.gnome.SettingsDaemon.DateTimeMechanism.service
%{_datadir}/polkit-1/actions/org.gnome.settingsdaemon.datetimemechanism.policy
%{_datadir}/GConf/gsettings/gnome-settings-daemon.convert

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.gschema.xml

%{_datadir}/dbus-1/interfaces/org.gnome.SettingsDaemonUpdates.xml


%{_datadir}/man/man1/gnome-settings-daemon.1.gz


%files devel
%{_includedir}/gnome-settings-daemon-3.0
%{_libdir}/pkgconfig/gnome-settings-daemon.pc
%dir %{_datadir}/gnome-settings-daemon-3.0
%{_datadir}/gnome-settings-daemon-3.0/input-device-example.sh

%changelog
* Tue Dec 27 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3.1-2
- Fix a path problem in the gnome-settings-daemon autostart file

* Fri Dec 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3.1-1
- Update to 3.3.3.1

* Wed Dec 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Fri Nov 11 2011 Bastien Nocera <bnocera@redhat.com> 3.2.2-1
- Update to 3.2.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-4
- Rebuilt for glibc bug#747377

* Tue Oct 25 2011 Marek Kasik <mkasik@redhat.com> - 3.2.1-3
- Fix a typo in registration of an object on DBus (#747318)

* Mon Oct 24 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-2
- Fix calculator keybinding (#745367)

* Mon Oct 17 2011 Bastien Nocera <bnocera@redhat.com> 3.2.1-1
- Update to 3.2.1

* Wed Oct 12 2011 Adam Williamson <awilliam@redhat.com> - 3.2.0-2
- backport some greatest hits from git to stop the same bugs being
  reported over and over (all will be in 3.2.1)

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Tue Jul 26 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.1.4-2
- Add a patch to make the fallback mounter to build correctly
- Include the new power plugin

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Fri Jul 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.3-2
- Add support for chrony (#723212)

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Tue Jun 21 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-2
- Fix fortify fail in gsd-color-manager.c (#714625)

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Wed Jun 15 2011 Bastien Nocera <bnocera@redhat.com> 3.1.1-3
- Rebuild for new gnome-desktop3 libs

* Mon Jun 13 2011 Marek Kasik <mkasik@redhat.com> 3.1.1-2
- Remove requirement of system-config-printer-udev (#704381)

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.1-5
- Update gsettings schema scriptlet

* Mon May  2 2011 Matthias Clasen <mclasen@redhat.com> 3.0.1-4
- Try to fix a crash (#698533)

* Thu Apr 28 2011 Bastien Nocera <bnocera@redhat.com> 3.0.1-2
- Fix setting ntpd usage with SystemD

* Tue Apr 26 2011 Bastien Nocera <bnocera@redhat.com> 3.0.1-1
- Update to 3.0.1

* Wed Apr 06 2011 Bastien Nocera <bnocera@redhat.com> 3.0.0.1-1
- Update to 3.0.0.1

* Mon Apr 04 2011 Bastien Nocera <bnocera@redhat.com> 3.0.0-1
- Update to 3.0.0

* Wed Mar 30 2011 Marek Kasik <mkasik@redhat.com> 2.91.93-2
- Make CUPS' subscriptions expirable

* Fri Mar 25 2011 Bastien Nocera <bnocera@redhat.com> 2.91.93-1
- Update to 2.91.93

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92-1
- Update 2.91.92

* Wed Mar 16 2011 Richard Hughes <rhughes@redhat.com> 2.91.91-3
- Add a patch from upstream to fix the updates plugin.

* Fri Mar 11 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91-2
- Add libXxf86misc-devel requires so that key repeat/delay works

* Tue Mar 08 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91-1
- Update to 2.91.91

* Fri Feb 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-4
- Fix undefined symbols in the updates plugin

* Wed Feb 23 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-3
- BR PackageKit and cups
- Explicitly list plugins so we notice if they go missing

* Wed Feb 23 2011 Cosimo Cecchi <cosimoc@redhat.com> - 2.91.90-2
- Include an upstream patch to fix a possible crasher

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> 2.91.90-1
- Update to 2.91.90

* Wed Feb 16 2011 Bastien Nocera <bnocera@redhat.com> 2.91.9-6
- Fix crasher when media keys GSettings value changes

* Sun Feb 13 2011 Christopher Aillon <caillon@redhat.com> - 2.91.9-5
- Rebuild for new libxklavier

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.9-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Bastien Nocera <bnocera@redhat.com> 2.91.9-2
- Fix setting timezones in the date & time panel (#674999)

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.9-1
- 2.91.9

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.8-1
- 2.91.8

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.7-2
- Own %%{_libdir}/gnome-settings-daemon-3.0/gtk-modules

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.7-1
- Update to 2.91.7

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6.2-1
- Update to 2.91.6.2

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.5.1-1
- Update to 2.91.5.1

* Thu Dec  2 2010 Dan Williams <dcbw@redhat.com> - 2.91.5-4
- Re-add patch handling org.gnome.media-handling gsettings schema rename

* Wed Dec  1 2010 Dan Williams <dcbw@redhat.com> - 2.91.5-3
- Fix various cases of forgetting to draw the background

* Tue Nov 30 2010 Owen Taylor <otaylor@redhat.com> - 2.91.5-2
- Add a patch handling org.gnome.media-handling gsettings schema rename

* Tue Nov 30 2010 Tomas Bzatek <tbzatek@redhat.com> 2.91.5-1
- Update to 2.91.5

* Fri Nov 26 2010 Bastien Nocera <bnocera@redhat.com> 2.91.4-2
- Fix crasher on startup

* Thu Nov 25 2010 Bastien Nocera <bnocera@redhat.com> 2.91.4-1
- Update to 2.91.4

* Wed Nov 17 2010 Richard Hughes <richard@hughsie.com> 2.91.3-1
- Update to 2.91.3

* Wed Nov 10 2010 Bastien Nocera <bnocera@redhat.com> 2.91.2.1-0.4.
- Update to 2.91.2.1

* Wed Nov  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.2-0.4.20101102
- Rebuild against new libnotify

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.2-0.3.20101102
- Make theme changing work

* Tue Nov 02 2010 Richard Hughes <richard@hughsie.com> 2.91.2-0.2.20101102
- Add BR gsettings-desktop-schemas-devel

* Tue Nov 02 2010 Richard Hughes <richard@hughsie.com> 2.91.2-0.1.20101102
- Update to a git snapshot to fix rawhide.

* Wed Oct 06 2010 Richard Hughes <rhughes@redhat.com> 2.91.0-3
- Fix the pkgconfig file manually

* Wed Oct 06 2010 Richard Hughes <rhughes@redhat.com> 2.91.0-2
- Rebuild against the new libgnomekbd library

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 jkeating - 2.90.1-2
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Bastien Nocera <bnocera@redhat.com> 2.90.1-1
- Update to 2.90.1

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> 2.31.91-1
- Update to 2.31.91

* Fri Aug 27 2010 Matthias Clasen <mclasen@redhat.com> 2.31.6-2
- Fix a problem with warning bubbles in virtual machines (#624624)

* Tue Aug  3 2010 Matthias Clasen <mclasen@redhat.com> 2.31.6-1
- Update to 2.31.6

* Tue Jul 13 2010 Matthias Clasen <mclasen@redhat.com> 2.31.5.1-1
- Update to 2.31.5.1

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> 2.31.5-1
- Update to 2.31.5

* Wed Jun 30 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4.2-1
- Update to 2.31.4.2

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4.1-1
- Update to 2.31.4.1

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4-1
- Update to 2.31.4

* Mon Jun 28 2010 Bastien Nocera <bnocera@redhat.com> 2.31.3-3
- Don't remove the sound plugin if we want the caches to be
  updated

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> 2.31.3-1
- Update to 2.31.3

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> 2.31.2-1
- Update to 2.31.2

* Sun May 16 2010 Matthias Clasen <mclasen@redhat.com> 2.31.1-1
- Update to 2.31.1

* Fri Apr 30 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-4
- Waah, one more mistake in these macros

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-3
- Nobody understands macro processors...

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-2
- Fix a typo

* Mon Apr 26 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1
- Spec file cleanups

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Mon Mar 22 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-3
- Disable the font plugin by default

* Wed Mar 10 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-2
- Remove unneeded icons, already upstream

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Sat Feb 27 2010 Matthias Clasen <mclasen@redhat.com> 2.29.91.1-2
- Fix Fn-F8 OSD icon
- Modernize scriptlets

* Wed Feb 24 2010 Matthias Clasen <mclasen@redhat.com> 2.29.91.1-1
- Update to 2.29.91.1

* Wed Feb 17 2010 Matthias Clasen <mclasen@redhat.com> 2.29.90-2
- Set a name for the keyboard statusicon

* Wed Feb 10 2010 Tomas Bzatek <tbzatek@redhat.com> 2.29.90-1
- Update to 2.29.90

* Tue Jan 26 2010 Matthias Clasen <mclasen@redhat.com> 2.29.6-1
- Update to 2.29.6

* Fri Dec 18 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-10
- Avoid warning messages from the OSD code

* Tue Dec 15 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-9
- Survive when running without XKB (#547780)

* Thu Nov 12 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-8
- Avoid a 'whitespace leak' around the display statusicon (gnome #601696)

* Mon Nov  9 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-7
- React to screen changes when showing the background (gnome #601203)

* Thu Nov 05 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-6
- Fix the volume going over 100% in the OSD

* Wed Oct 28 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-5
- Update OSD code again

* Tue Oct 27 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-4
- Fix bluriness in OSD

* Mon Oct 26 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-3
- Change default font rendering to use slight hinting

* Mon Oct 26 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.28.1-2
- left-handed-touchpad.patch: change physical touchpad buttons to
  left-handed, not tapping though (#498249)

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Thu Oct  1 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-4
- Fix keyboard variant handling

* Fri Sep 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-3
- Align the OSD visuals with the notification theme

* Tue Sep 22 2009 Adam Jackson <ajax@redhat.com> 2.28.0-2
- BuildRequires: libcanberra-devel

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Wed Sep 09 2009 Bastien Nocera <bnocera@redhat.com> 2.27.92-2
- Update left-hand touchpad patch

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Sun Aug 30 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-3
- Make 'Locate Pointer' work with metacity again

* Wed Aug 26 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.27.91-2
- buttonmapping.patch: Don't check for IsXExtensionDevice, only skip button
  mappings for core devices instead (#502129).

* Mon Aug 24 2009 Bastien Nocera <bnocera@redhat.com> 2.27.91-1
- Update to 2.27.91

* Fri Aug 14 2009 Bastien Nocera <bnocera@redhat.com> 2.27.90-2
- Update gnome-volume-control code

* Fri Aug 14 2009 Bastien Nocera <bnocera@redhat.com> 2.27.90-1
- Update to 2.27.90

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-3
- Make locate-pointer not interfere with media keys

* Wed Jul 15 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-2
- Rebuild against new libgnomekbd

* Tue Jul 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-1
- Update ot 2.27.4

* Tue Jun 30 2009 Matthias Clasen <mclasen@redhat.com> 2.27.3-2
- Rebuild against new libxklavier

* Tue Jun 16 2009 Matthias Clasen <mclasen@redhat.com> 2.27.3-1
- Update to 2.27.3

* Mon Jun  8 2009 Matthias Clasen <mclasen@redhat.com> 2.27.1-2
- Make the 'locate pointer' effect cope with changing compositing
  managers

* Sat May 16 2009 Matthias Clasen <mclasen@redhat.com> 2.27.1-1
- Update to 2.27.1

* Fri May 08 2009 Bastien Nocera <bnocera@redhat.com> 2.26.1-4
- Remove useless patch, see:
http://bugzilla.gnome.org/show_bug.cgi?id=580761 for details

* Wed Apr 29 2009 Bastien Nocera <bnocera@redhat.com> 2.26.1-3
- Don't set touchpads to be left-handed, otherwise the tap
  behaves like the 2nd mouse button (#483639)

* Mon Apr 27 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.1-2
- Don't drop schemas translations from po files

* Tue Apr 14 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Wed Apr  8 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.0-2
- Support touchpads

* Mon Mar 16 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb  5 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.90-2
- Fix a warning (#484132)

* Wed Feb  4 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Mon Jan 19 2009 - Ray Strode <rstrode@redhat.com> - 2.25.3-4
- Update fade patch for new gnome-desktop release

* Thu Dec 18 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-3
- Rebuild

* Thu Dec 18 2008 - Ray Strode <rstrode@redhat.com> - 2.25.3-2
- Drop touchpad patch for now

* Thu Dec 18 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-1
- Update to 2.25.3

* Thu Dec 18 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.2-11
- Fix touchpad patches

* Wed Dec 17 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.2-10
- Rebuild against new gnome-desktop

* Wed Dec 10 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-9
- Don't call SetPointerMapping when using Xinput since
  it duplicates effort but gets touchpads wrong (bug 324721)

* Wed Dec 10 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-8
- Shutdown cleanly when bus goes away (bug 445898 again)

* Wed Dec 10 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-7
- Don't map touch pad tap to right-click for left-handed
  users (bug 324721)

* Wed Dec 10 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-6
- Listen for DeviceAdded signals when configuring mouse
  (in addition to DeviceEnabled).  This may help with
  bug 474758.

* Tue Dec  9 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-5
- Shutdown cleanly on TERM signal (bug 445898)

* Sun Dec  7 2008 Behdad Esfahbod <besfahbo@redhat.com> - 2.25.2-4
- Add gnome-settings-daemon-2.24.1-umask.patch

* Thu Dec  4 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-2
- Rebase fade patch to apply with Behdad's updates to
  g-s-d

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Ypdate to 2.25.2

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-4
- Rebuild

* Wed Nov 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-2
- Update to 2.25.1

* Fri Oct 24 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-14
- At fontconfig-devel buildrequires (bug 468304)

* Wed Oct 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-13
- Save some space

* Tue Oct 14 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-12
- Hold off on settings-daemon fade if nautilus is going to do
  it anyway.

* Tue Oct 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-11
- Show the shutdown dialog when the power button is pressed

* Tue Oct 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-9
- Drop a patch that is no longer needed with the evdev ruleset
  in xkeyboard-config

* Sun Oct 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-7
- Try harder not to override peoples configured keyboard layouts

* Sun Oct 12 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-6
- Update fade patch to skip crossfade when changing frames in
  slideshow background.

* Fri Oct 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-5
- Fix the picking up of the gdm keyboard layout even more

* Tue Sep 30 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-3
- Fix the picking up of the gdm keyboard layout

* Wed Sep 28 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-2
- Don't draw background twice at startup

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Thu Sep 18 2008 Ray Strode <rstrode@redhat.com> - 2.23.92-3
- When switching desktop backgrounds fade between them

* Thu Sep 11 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.92-2
- Fix various bugs in the fn-F7 support

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Fri Sep  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-5
- Try harder to use the keyboard layout that gdm tells us

* Tue Sep 04 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.91-4
- Use the fn-F7 key, not the F7 key.

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

