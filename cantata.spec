# TODO
# - handle /usr/share/cantata/fonts/fontawesome-4.3.0.ttf
#
# Conditional build:
%bcond_without	udisks	# UDisks support
%bcond_with	musicbrainz	# musicbrainz5

%define		qtver	5.11

Summary:	Music Player Daemon (MPD) graphical client
Name:		cantata
Version:	2.4.2
Release:	1
License:	GPL v2+
Group:		Applications/Multimedia
# https://github.com/CDrummond/cantata/releases
Source0:	https://github.com/CDrummond/cantata/releases/download/v%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	83b6a2504f1fa40e88d06272aab9f512
Patch0:		%{name}-lrelease.patch
Patch101:	system-qtiocompressor.patch
Patch105:	icons_crash.patch
Patch106:	libdir.patch
URL:		https://github.com/cdrummond/cantata
BuildRequires:	Qt5Concurrent-devel >= %{qtver}
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5IOCompressor-devel
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Sql-devel >= %{qtver}
BuildRequires:	Qt5Svg-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	avahi-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	desktop-file-utils
BuildRequires:	libcddb-devel
BuildRequires:	libcdio-paranoia-devel
BuildRequires:	libmtp-devel >= 1.1.0
%{?with_musicbrainz:BuildRequires:	libmusicbrainz5-devel}
# C++11
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	media-player-info
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	qt5-qmake >= %{qtver}
BuildRequires:	rpmbuild(find_lang) >= 1.37
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	systemd-devel
BuildRequires:	taglib-devel >= 1.6
BuildRequires:	vlc-devel
BuildRequires:	zlib-devel
Requires:	Qt5Concurrent >= %{qtver}
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5DBus >= %{qtver}
Requires:	Qt5Gui >= %{qtver}
Requires:	Qt5Network >= %{qtver}
Requires:	Qt5Sql >= %{qtver}
Requires:	Qt5Sql-sqldriver-sqlite3 >= %{qtver}
Requires:	Qt5Svg >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}
Requires:	Qt5Xml >= %{qtver}
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	libmtp >= 1.1.0
Requires:	media-player-info
Requires:	taglib >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cantata is a graphical client for the music player daemon (MPD).

Features:
- Multiple MPD collections.
- Highly customisable layout.
- Songs grouped by album in play queue.
- Context view to show artist, album, and song information of current
  track.
- Simple tag editor.
- File organizer - use tags to organize files and folders.
- Ability to calculate ReplyGain tags.
- Dynamic playlists.
- Online services; Jamendo, Magnatune, SoundCloud, and Podcasts.
- Radio stream support - with the ability to search for streams via
  TuneIn and ShoutCast.
- USB-Mass-Storage and MTP device support.
- Audio CD ripping and playback.
- Playback of non-MPD songs, via simple in-built HTTP server.
- MPRISv2 DBUS interface.
- Support for KDE global shortcuts (KDE builds), GNOME media keys, and
  generic media keys (via Qxt support)
- Ubuntu/ambiance theme integration.

%prep
%setup -q
%patch0 -p1

%patch101 -p1
rm -rfv 3rdparty/{qjson,qtiocompressor}

rm -rfv 3rdparty/{qtsingleapplication,qxt}
sed -i.system-qxt-headers -e 's|^#include "qxt/qxtglobalshortcut.h"|#include <QxtGlobalShortcut>|g' \
	gui/qxtmediakeys.cpp

#%patch105 -p1
%patch106 -p1

%build
install -d build
cd build
CXXFLAGS="%{rpmcxxflags} -I/usr/include/qt5/QtSolutions"
%cmake \
	-DCANTATA_HELPERS_LIB_DIR=%{_lib} \
	-DENABLE_FFMPEG:BOOL=OFF \
	-DENABLE_LIBVLC=ON \
	-DENABLE_MPG123:BOOL=OFF \
	-DENABLE_MUSICBRAINZ=%{?with_musicbrainz:ON}%{!?with_musicbrainz:OFF} \
	-DENABLE_UDISKS2:BOOL=%{?with_udisks:ON}%{!?with_udisks:OFF} \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install/fast -C build \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-qm

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cantata.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README TODO
%attr(755,root,root) %{_bindir}/cantata
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/cantata-tags
%{_desktopdir}/cantata.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/translations
#%{_datadir}/%{name}/config
%{_datadir}/%{name}/icons
#%{_datadir}/%{name}/mpd
%{_datadir}/%{name}/scripts
#%{_datadir}/%{name}/themes
