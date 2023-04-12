%global kf5_version 5.104.0

Name: opt-kf5-purpose
Summary: Framework for providing abstractions to get the developer's purposes fulfilled
Version: 5.104.0
Release: 1%{?dist}

# KDE e.V. may determine that future GPL versions are accepted
# most files LGPLv2+, configuration.cpp is KDE e.V. GPL variant
License: GPLv2 or GPLv3
URL:     https://invent.kde.org/frameworks/purpose

Source0: %{name}-%{version}.tar.bz2

BuildRequires: opt-extra-cmake-modules >= %{kf5_version}
BuildRequires: gettext
BuildRequires: intltool

BuildRequires: opt-kf5-rpm-macros
BuildRequires: opt-kf5-kconfig-devel >= %{kf5_version}
BuildRequires: opt-kf5-kcoreaddons-devel >= %{kf5_version}
BuildRequires: opt-kf5-ki18n-devel >= %{kf5_version}
BuildRequires: opt-kf5-kio-devel >= %{kf5_version}
BuildRequires: opt-kf5-kirigami2-devel >= %{kf5_version}

BuildRequires: cmake(KF5Kirigami2)

# optional sharefile plugin
BuildRequires: cmake(KF5KIO)
BuildRequires: cmake(KF5Notifications)

BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Qml)

%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires: kaccounts-integration-devel
# runtime dep?
BuildRequires: kde-connect
BuildRequires: pkgconfig(accounts-qt5)
BuildRequires: pkgconfig(libaccounts-glib)
%endif

%description
Purpose offers the possibility to create integrate services and actions on
any application without having to implement them specifically. Purpose will
offer them mechanisms to list the different alternatives to execute given the
requested action type and will facilitate components so that all the plugins
can receive all the information they need.

%package  devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: cmake(KF5CoreAddons)
%description devel
%{summary}.


%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

mkdir -p build
pushd build

%_opt_cmake_kf5 ../
%make_build

popd

%install
pushd build
make DESTDIR=%{buildroot} install
popd

%find_lang %{name} --all-name

## unpackaged files
# omit (unused?) conflicting icons with older kamoso (rename to "google-youtube"?)
rm -fv %{buildroot}%{_datadir}/icons/hicolor/*/actions/kipiplugin_youtube.png


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc README.md
%license LICENSES/*.txt
%{_opt_kf5_datadir}/qlogging-categories5/purpose.*
%{_opt_kf5_libdir}/libKF5Purpose.so.5*
%{_opt_kf5_libdir}/libKF5PurposeWidgets.so.5*
%{_opt_kf5_libdir}/libPhabricatorHelpers.so.5*
%{_opt_kf5_libdir}/libReviewboardHelpers.so.5*
%{_opt_kf5_libexecdir}/purposeprocess
%{_opt_kf5_datadir}/purpose/
%{_opt_kf5_plugindir}/purpose/
%dir %{_opt_kf5_plugindir}/kfileitemaction/
%{_opt_kf5_plugindir}/kfileitemaction/sharefileitemaction.so
%{_opt_kf5_qmldir}/org/kde/purpose/
# this conditional may require adjusting too (e.g. wrt %%twitter)
%if 0%{?fedora} || 0%{?rhel} > 7
%{_opt_kf5_datadir}/accounts/services/kde/google-youtube.service
%{_opt_kf5_datadir}/accounts/services/kde/nextcloud-upload.service
%endif
%{_datadir}/icons/hicolor/*/apps/*-purpose.*
#{_datadir}/icons/hicolor/*/actions/google-youtube.*

%files devel
%{_opt_kf5_libdir}/libKF5Purpose.so
%{_opt_kf5_libdir}/libKF5PurposeWidgets.so
%{_opt_kf5_includedir}/KF5/purpose/
%{_opt_kf5_includedir}/KF5/purposewidgets/
%{_opt_kf5_libdir}/cmake/KDEExperimentalPurpose/
%{_opt_kf5_libdir}/cmake/KF5Purpose/
