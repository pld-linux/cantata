# TODO
# - handle /usr/share/cantata/fonts/fontawesome-4.3.0.ttf
#
# Conditional build:
%bcond_with	ffmpeg		# FFmpeg for ReplayGain support
%bcond_with	mpg123		# libmpg123 for ReplayGain support
%bcond_with	musicbrainz	# MusicBrainz for AudioCD support
%bcond_without	udisks		# UDisks2 support via udev+dbus

# 6.5.0 required by 3rdparty/knotifications
%define		qt_ver	6.5.0

Summary:	Music Player Daemon (MPD) graphical client
Summary(pl.UTF-8):	Graficzny klient demona odtwarzania muzyki MPD
Name:		cantata
Version:	3.5.0
Release:	1
License:	GPL v2+
Group:		Applications/Multimedia
#Source0Download: https://github.com/nullobsi/cantata/releases
Source0:	https://github.com/nullobsi/cantata/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3249b3501176c8f0a8677854d713aed8
URL:		https://github.com/nullobsi/cantata
BuildRequires:	Qt6Concurrent-devel >= %{qt_ver}
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6DBus-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Network-devel >= %{qt_ver}
BuildRequires:	Qt6Qml-devel >= %{qt_ver}
BuildRequires:	Qt6Sql-devel >= %{qt_ver}
BuildRequires:	Qt6Svg-devel >= %{qt_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	Qt6Xml-devel >= %{qt_ver}
BuildRequires:	avahi-devel
# 3.5 in top, but 3.16 in 3rdparty/knotifications
BuildRequires:	cmake >= 3.16
BuildRequires:	desktop-file-utils
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel}
BuildRequires:	kf6-karchive-devel >= 6
BuildRequires:	kf6-kitemviews-devel >= 6
BuildRequires:	libcddb-devel
# preferred; or cdioparanoia-III-devel with -DENABLE_CDIOPARANOIA=OFF
BuildRequires:	libcdio-paranoia-devel
%{?with_mpg123:BuildRequires:	libmpg123-devel}
BuildRequires:	libmtp-devel >= 1.1.0
%{?with_musicbrainz:BuildRequires:	libmusicbrainz5-devel}
# C++11
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
BuildRequires:	qt6-build >= %{qt_ver}
BuildRequires:	qt6-linguist >= %{qt_ver}
BuildRequires:	rpmbuild(find_lang) >= 1.37
BuildRequires:	rpmbuild(macros) >= 2.047
BuildRequires:	sed >= 4.0
BuildRequires:	taglib-devel >= 2.0
BuildRequires:	udev-devel
# for MPD HTTP stream playback; or Qt6Multimedia-devel with -DENABLE_LIBVLC=OFF
BuildRequires:	vlc-devel
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	Qt6Concurrent%{?_isa} >= %{qt_ver}
Requires:	Qt6Core%{?_isa} >= %{qt_ver}
Requires:	Qt6DBus%{?_isa} >= %{qt_ver}
Requires:	Qt6Gui%{?_isa} >= %{qt_ver}
Requires:	Qt6Network%{?_isa} >= %{qt_ver}
Requires:	Qt6Qml%{?_isa} >= %{qt_ver}
Requires:	Qt6Sql%{?_isa} >= %{qt_ver}
Requires:	Qt6Sql-sqldriver-sqlite3%{?_isa} >= %{qt_ver}
Requires:	Qt6Svg%{?_isa} >= %{qt_ver}
Requires:	Qt6Widgets%{?_isa} >= %{qt_ver}
Requires:	Qt6Xml%{?_isa} >= %{qt_ver}
Requires:	hicolor-icon-theme
Requires:	libmtp%{?_isa} >= 1.1.0
Requires:	media-player-info
Requires:	taglib%{?_isa} >= 2.0
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
- Ability to calculate ReplayGain tags.
- Dynamic playlists.
- Online services; Jamendo, Magnatune, SoundCloud, and Podcasts.
- Radio stream support - with the ability to search for streams via
  TuneIn, ShoutCast, or Dirble.
- USB-Mass-Storage and MTP device support.
- Audio CD ripping and playback.
- Playback of non-MPD songs, via simple in-built HTTP server.
- MPRISv2 DBus interface.
- Ratings support.
- "Partitions" support.

%description -l pl.UTF-8
Cantata to graficzny klient demona odtwarzania muzyki MPD.

Funkcjonalność:
- wiele kolekcj MPD
- konfigurowalny wygląd
- grupowanie utworów albumami w kolejce odtwarzania
- widok kontekstowy pokazujący informacje o artyście, albumie i
  utworze dla bieżącej ścieżki
- prosty edytor znaczników
- organizator plików i folderów na podstawie znaczników
- wyliczanie znaczników ReplayGain
- dynamiczne listy odtwarzania
- usługi sieciowe: Jamendo, Magnatune, SoundCloud i Podcasts
- obsługa strumieni radiowych, z możliwością wyszukiwania przez
  TuneIn i ShoutCast
- obsługa urządzeń USB-Mass-Storage i MTP
- ściąganie ścieżek i odtwarzanie CD
- odtwarzanie utworów nie-MPD poprzez prosty, wbudowany serwer HTTP
- interfejs DBus MPRISv2
- obsługa ocen
- obsługa "partycji"

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env perl$,%{__perl},' playlists/cantata-dynamic.cmake

%{__rm} -r 3rdparty/karchive
%{__rm} -r 3rdparty/kcategorizedview
%{__rm} -r 3rdparty/qtsingleapplication

%build
%cmake -B build \
	-DENABLE_FFMPEG:BOOL=%{__ON_OFF ffmpeg} \
	-DENABLE_LIBVLC:BOOL=ON \
	-DENABLE_MPG123:BOOL=%{__ON_OFF mpg123} \
	-DENABLE_MUSICBRAINZ:BOOL=%{__ON_OFF musicbrainz} \
	-DENABLE_UDISKS2:BOOL=%{__ON_OFF udisks}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-qm

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/dog.unix.cantata.Cantata.desktop

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
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/cantata
%dir %{_libexecdir}/Cantata
%attr(755,root,root) %{_libexecdir}/Cantata/cantata-tags
%dir %{_datadir}/Cantata
%dir %{_datadir}/Cantata/translations
%{_datadir}/Cantata/icons
%{_datadir}/Cantata/scripts
%{_datadir}/metainfo/dog.unix.cantata.Cantata.metainfo.xml
%{_desktopdir}/dog.unix.cantata.Cantata.desktop
%{_iconsdir}/hicolor/*x*/apps/dog.unix.cantata.Cantata.png
%{_iconsdir}/hicolor/scalable/apps/dog.unix.cantata.Cantata.svg
%{_iconsdir}/hicolor/symbolic/apps/dog.unix.cantata.Cantata-symbolic.svg
