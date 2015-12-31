#
# Conditional build:
%bcond_with	kde		# KDE
%bcond_with	qt4		# Qt4
%bcond_without	qt5		# Qt5
%bcond_without	udisks	# UDisks support
%bcond_with	musicbraninz	# musicbrainz5

Summary:	Music Player Daemon (MPD) graphical client
Name:		cantata
Version:	1.5.2
Release:	1
License:	GPL v2+
Group:		Applications/Multimedia
# https://github.com/CDrummond/cantata/wiki/Previous-%28Google-Code%29-Downloads
Source0:	https://drive.google.com/uc?export=download&id=0Bzghs6gQWi60LV9rM3RMQk85Z1E&/%{name}-%{version}.tar.bz2
# Source0-md5:	0b29d30f1b03ecac23eb608309fbeaa1
Patch101:	system-qtiocompressor.patch
Patch102:	system-qxt.patch
Patch103:	kde4_includes.patch
Patch104:	libsolid_static.patch
Patch105:	icons_crash.patch
URL:		https://github.com/cdrummond/cantata
BuildRequires:	cdparanoia-III-devel
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
%{?with_kde:BuildRequires:	kde4-kdelibs-devel >= 4.7}
BuildRequires:	rpmbuild(macros) >= 1.596
%if %{with qt4} || %{with kde}
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtIOCompressor-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtSingleApplication-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	QtXml-devel
BuildRequires:	libqxt-devel
BuildRequires:	phonon-devel
BuildRequires:	qjson-devel
%endif
%if %{with qt5}
BuildRequires:	Qt5Concurrent-devel
BuildRequires:	Qt5DBus-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5Svg-devel
BuildRequires:	Qt5WebKit-devel
BuildRequires:	Qt5Xml-devel
BuildRequires:	phonon-qt5-devel
%endif
BuildRequires:	libcddb-devel
BuildRequires:	libmtp-devel
%{?with_musicbrainz:BuildRequires:	libmusicbrainz5-devel}
BuildRequires:	media-player-info
BuildRequires:	phonon-devel
BuildRequires:	systemd-devel
BuildRequires:	taglib-devel
BuildRequires:	taglib-extras-devel
Requires:	media-player-info
%if %{with kde}
# http://bugzilla.redhat.com/1134333
Requires:	kde4-icons-oxygen
%endif
Requires:	Qt5Gui-platform-xcb
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
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

# No qt5 qjson,qtiocompressor... yet
%if %{without qt5}
%patch101 -p1
rm -rfv 3rdparty/{qjson,qtiocompressor}/
sed -i.system-qtiocompressor-headers -e 's|^#include "qtiocompressor/qtiocompressor.h"|#include <QtIOCompressor>|g' \
	context/albumview.cpp \
	context/artistview.cpp \
	context/songview.cpp \
	context/wikipediasettings.cpp \
	models/dirviewmodel.cpp \
	models/musiclibrarymodel.cpp \
	models/musiclibraryitempodcast.cpp \
	models/musiclibraryitemroot.cpp \
	models/streamsmodel.cpp \
	online/onlineservice.cpp \
	scrobbling/scrobbler.cpp \
	streams/tar.cpp
%endif

%patch102 -p1
rm -rfv 3rdparty/{qtsingleapplication,qxt}
sed -i.system-qxt-headers -e 's|^#include "qxt/qxtglobalshortcut.h"|#include <QxtGlobalShortcut>|g' \
  gui/qxtmediakeys.cpp

%patch103 -p1
%patch104 -p1
%patch105 -p1

%build
install -d build
cd build
CXXFLAGS="%{rpmcxxflags} -I/usr/include/QtSolutions" # see bug 1077936
%cmake \
	-DENABLE_KDE:BOOL=%{?with_kde:ON}%{!?with_kde:OFF} \
	-DENABLE_QT5:BOOL=%{?with_qt5:ON}%{!?with_qt5:OFF} \
	-DENABLE_FFMPEG:BOOL=OFF \
	-DENABLE_MPG123:BOOL=OFF \
	-DENABLE_MUSICBRAINZ=%{?with_musicbrainz:ON}%{!?with_musicbrainz:OFF} \
	-DENABLE_UDISKS2:BOOL=%{?with_udisks:ON}%{!?with_udisks:OFF} \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install/fast -C build \
	DESTDIR=$RPM_BUILD_ROOT

#%find_lang %{name} --with-qt --with-kde --all-name

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/cantata.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README TODO
%attr(755,root,root) %{_bindir}/cantata
%{_prefix}/lib/cantata/
%{_desktopdir}/cantata.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%dir %{_datadir}/cantata
%{_datadir}/cantata/config
%{_datadir}/cantata/icons
%{_datadir}/cantata/mpd
%{_datadir}/cantata/scripts
%{_datadir}/cantata/themes
%if %{with kde}
#%dir %{_kde4_appsdir}/solid/
#%dir %{_kde4_appsdir}/solid/actions/
#%{_kde4_appsdir}/solid/actions/cantata-play-audiocd.desktop
%else
#%dir %{_datadir}/cantata/translations/
%endif
