# Please update release notes:
# make -C SOURCES release-notes.{html,txt}
#
%bcond_with bootstrap

%define new_distribution OpenMandriva Lx
%define new_vendor OpenMandriva
%define new_product OpenMandriva Lx
# (tpg) use codename from here https://wiki.openmandriva.org/en/policies/codename
%define new_codename Nickel
%define vendor_tag %(echo %{new_vendor} |tr A-Z a-z)
%define distribution_tag %(echo %{new_distribution} |tr A-Z a-z |sed -e 's,[ /!?],_,g')
%define product_tag %(echo %{new_product} |tr A-Z a-z |sed -e 's,[ /!?],_,g')
%define shorttag omv
%define new_disturl http://openmandriva.org/
%define new_bugurl https://github.com/OpenMandrivaAssociation/distribution/issues/

%define am_i_cooker 1
%undefine am_i_rolling
%if 0%?am_i_cooker
%define distrib Cooker
%else
%if 0%?am_i_rolling
%define distrib Rolling
%else
%define distrib Rock
%endif
%endif
%define _distribution %(echo %{new_distribution} | tr A-Z a-z |sed -e 's#[ /()!?]#_#g')
%define product_type Basic
%if 0%?am_i_cooker
%define product_branch Devel
%else
%define product_branch Rock
%endif
%define product_release 1
%define product_arch %{_target_cpu}

# The Distribution release, what is written on box
%define distro_release %{version}

# The distro branch: Cooker, Rolling or Rock
%define distro_branch %{distrib}

# The distro arch, notice: using %_target_cpu is bad
# elsewhere because this depend of the config of the packager
# _target_cpu => package build for
# distro_arch => the distribution we are using
%define distro_arch %{_target_cpu}

%define major %(printf %u %(echo %{version}|cut -d. -f1 |sed -e 's,^0*,,'))
%define minor %([ -z "%(echo %{version}|cut -d. -f2)" ] && echo 0 || printf %u %(echo %{version}|cut -d. -f2 |sed -e 's,^0*,,'))
%define subminor %([ -z "%(echo %{version}|cut -d. -f3)" ] && echo 0 || printf %u %(echo %{version}|cut -d. -f3 |sed -e 's,^0*,,'))
%if 0%?am_i_cooker || 0%?am_i_rolling
# 22.12 looks better as omv2212 than omv22012...
%define distro_tag %(echo $((%{major}*100+%{minor})))
%define version_tag %(echo $((%{major}*1000000+%{minor}*1000+%{subminor})))
%else
%define distro_tag %(echo $((%{major}*1000+%{minor})))
%define version_tag %(echo $((%{major}*1000000+%{minor}*1000+%{subminor})))
%endif
%define mdkver %{version_tag}

%ifarch %{x86_64}
%global secondary_distarch i686
%else
%ifarch %{aarch64}
%global secondary_distarch armv7hnl
%endif
%endif

Summary:	%{new_distribution} release file
Name:		distro-release-desktop-Plasma6
Version:	23.90
# (tpg) something needs to be done to make comparision 3.0 > 2015.0 came true
# 3001 = 3.1
# 3001 = 3.2 etc.
DistTag:	%{shorttag}%{distro_tag}
Release:	4
License:	GPLv2+
URL:		https://github.com/OpenMandrivaSoftware/distro-release
Source0:	https://github.com/OpenMandrivaSoftware/distro-release/archive/%{?am_i_cooker:refs/heads/master}%{!?am_i_cooker:%{version}/%{name}-%{version}}.tar.gz
Group:		System/Configuration/Other
BuildRequires:	cmake(ECM)
Requires:	distro-release-desktop >= %{version}
Requires:	distro-release-theme >= %{version}
Requires:	plasma6-breeze
Requires:	plasma6-breeze-gtk
Requires:	kf6-breeze-icons
Requires:	noto-sans-fonts
BuildArch:	noarch

%description
%{distribution} release file for Plasma 6

%prep
%autosetup -p1 %{?am_i_cooker:-n distro-release-master}

%install
### DESKTOP PLASMA6 ###
mkdir -p %{buildroot}%{_sysconfdir}/xdg
mkdir -p %{buildroot}%{_sysconfdir}/xdg/KDE
mkdir -p %{buildroot}%{_sysconfdir}/xdg/QtProject
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart-scripts
mkdir -p %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env
mkdir -p %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/shutdown
mkdir -p %{buildroot}%{_datadir}/kservices5
mkdir -p %{buildroot}%{_datadir}/plasma/shells/org.kde.plasma.desktop/contents
mkdir -p %{buildroot}%{_datadir}/plasma/look-and-feel
mkdir -p %{buildroot}%{_datadir}/plasma/layout-templates/org.om.plasma6.desktop.defaultPanel/contents
mkdir -p %{buildroot}%{_datadir}/konsole

for i in kcmdisplayrc kcmfonts kcminputrc kdeglobals kscreenlockerrc ksplashrc kwinrc startupconfig startupconfigfiles kcm-about-distrorc ksmserverrc kiorc dolphinrc konsolerc klaunchrc plasma_workspace.notifyrc powermanagementprofilesrc PlasmaUserFeedback plasma-org.kde.plasma.desktop-appletsrc startupconfigkeys; do
    install -m 0644 desktops/Plasma6/$i %{buildroot}%{_sysconfdir}/xdg/$i
done

install -m 0644 desktops/Plasma6/plasma-firstsetup.sh %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/plasma-firstsetup.sh
ln -sf %{_sysconfdir}/xdg/plasma-workspace/env/plasma-firstsetup.sh %{buildroot}%{_sysconfdir}/xdg/autostart-scripts/plasma-firstsetup.sh
install -m 0644 desktops/Plasma6/Sonnet.conf %{buildroot}%{_sysconfdir}/xdg/KDE/Sonnet.conf
install -m 0644 desktops/Plasma6/kdeglobals.sh %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/kdeglobals.sh
ln -sf %{_sysconfdir}/xdg/plasma-workspace/env/kdeglobals.sh %{buildroot}%{_sysconfdir}/xdg/autostart-scripts/kdeglobals.sh
install -m 0644 desktops/Plasma6/qtlogging.ini %{buildroot}%{_sysconfdir}/xdg/QtProject/qtlogging.ini
install -m 0644 desktops/Plasma6/OM.profile %{buildroot}%{_datadir}/konsole/OM.profile
cp -a desktops/Plasma6/org.openmandriva6.desktop %{buildroot}%{_datadir}/plasma/look-and-feel/org.openmandriva6.desktop
# (rugyada)
install -m 0644 desktops/Plasma6/metadata-omP6panel.desktop %{buildroot}%{_datadir}/plasma/layout-templates/org.om.plasma6.desktop.defaultPanel/metadata.desktop
install -m 0644 desktops/Plasma6/metadata-omP6panel.json %{buildroot}%{_datadir}/plasma/layout-templates/org.om.plasma6.desktop.defaultPanel/metadata.json
install -m 0644 desktops/Plasma6/metadata-omP6panel.desktop %{buildroot}%{_datadir}/kservices5/plasma-layout-template-org.om.plasma6.desktop.defaultPanel.desktop
install -m 0644 desktops/Plasma6/metadata-omP6panel.json %{buildroot}%{_datadir}/kservices5/plasma-layout-template-org.om.plasma6.desktop.defaultPanel.json
install -m 0644 desktops/Plasma6/org.kde.plasma.desktop-layout.js %{buildroot}%{_datadir}/plasma/shells/org.kde.plasma.desktop/contents/layout.js
install -m 0644 desktops/Plasma6/org.om.plasma6.desktop.defaultPanel-layout.js %{buildroot}%{_datadir}/plasma/layout-templates/org.om.plasma6.desktop.defaultPanel/contents/layout.js
### DESKTOP PLASMA6 END ###

%files
%{_sysconfdir}/xdg/*
%{_datadir}/konsole/OM.profile
%{_datadir}/kservices5/plasma-layout-template-org.om.plasma6.desktop.defaultPanel.desktop
%{_datadir}/kservices5/plasma-layout-template-org.om.plasma6.desktop.defaultPanel.json
%{_datadir}/plasma/layout-templates/org.om.plasma6.desktop.defaultPanel
%{_datadir}/plasma/look-and-feel/org.openmandriva6.desktop
%{_datadir}/plasma/shells/org.kde.plasma.desktop/contents/layout.js
