%define rev 1076

%define major 1
%define libname %mklibname apparmor %{major}
%define develname %mklibname apparmor -d

Summary:	AppArmor security framework
Name:		apparmor
Version:	2.1
Release:	%mkrel 1.%{rev}.2
License:	GPL
Group:		System/Libraries
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	apparmor-%{version}-%{rev}.tar.bz2
Source1:        B15_mod_apparmor.conf
Source2:        sbin.rpcbind
Patch:          apparmor-2.1-961-ldflags.patch
Patch1:         apparmor-2.1-961-condreload.patch
BuildRequires:  flex
BuildRequires:  latex2html
BuildRequires:  bison
BuildRequires:  perl-devel
BuildRequires:  libpam-devel
BuildRequires:  apache-devel
BuildRequires:  swig
BuildRequires:  libpanel-applet-2-devel
BuildRequires:  libaudit-devel
BuildRequires:  pkgconfig
BuildRequires:  libdbus-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
AppArmor is a security framework that proactively protects the operating system
and applications from external or internal threats, even zero-day attacks, by
enforcing good program behavior and preventing even unknown software flaws from
being exploited. AppArmor security profiles completely define what system
resources individual programs can access, and with what privileges.

%package -n	%{libname}
Summary:	Main libraries for %{name}
Group:		System/Libraries
License:        LGPL

%description -n	%{libname}
This package contains the AppArmor library.

%package -n	%{develname}
Summary:	Development files for %{name}
Summary(pt_BR):	Arquivos de desenvolvimento para %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libapparmor-devel = %{version}-%{release}
Provides:	apparmor-devel = %{version}-%{release}
Obsoletes:	%{mklibname apparmor 1 -d}

%description -n %{develname}
This package contains development files for %{name}.

%package -n     perl-libapparmor
Summary:        AppArmor module for perl
Group:          Development/Perl
Requires:       %{libname} = %{version}

%description -n perl-libapparmor
This package contains the AppArmor module for perl.

%package        profiles
Summary:        Base AppArmors profiles
License:        GPL
Group:          System/Base
Requires:       apparmor-parser
Requires(post): apparmor-parser

%description profiles
Base AppArmor profiles (aka security policy).

%package        parser
Summary:        AppArmor userlevel parser utility
License:        GPL
Group:          System/Base
Requires(preun): rpm-helper
Requires(post): rpm-helper

%description parser
AppArmor Parser is a userlevel program that is used to load in program
profiles to the AppArmor Security kernel module.

%package -n     pam_apparmor
Summary:        PAM module for AppArmor
License:        GPL
Group:          System/Libraries

%description -n pam_apparmor
The pam_apparmor module provides the means for any pam applications that call
pam_open_session() to automatically perform an AppArmor change_hat operation in
order to switch to a user-specific security policy.

%package        utils
Summary:        AppArmor userlevel utilities
License:        GPL
Group:          System/Base
Obsoletes:      apparmor-docs < 2.1

%description utils
This package contains programs to help create and manage AppArmor
profiles.

%package -n     apache-mod_apparmor
Summary:        Fine-grained AppArmor confinement for apache
License:        LGPL
Group:          System/Servers

%description -n apache-mod_apparmor
apache-mod_apparmor adds support to apache to provide AppArmor confinement
to individual cgi scripts handled by apache modules like mod_php and mod_perl.
This package is part of a suite of tools that used to be named SubDomain.

%package        dbus
Summary:        D-Bus support for AppArmor
License:        GPL
Group:          System/Servers

%description dbus
D-Bus support for AppArmor.

%package        applet-gnome
Summary:        An AppArmor applet for Gnome
Group:          Graphical desktop/GNOME

%description applet-gnome
This package contains an AppArmor applet for Gnome.

%prep
%setup -q -n %{name}-%{version}-%{rev}
pushd changehat/pam_apparmor
%patch -p0 -b .ldflags
popd
pushd parser
%patch1 -p0 -b .condrestart
popd

%build
%serverbuild

# library
pushd changehat/libapparmor
./autogen.sh
%configure --with-perl
%make CFLAGS="$RPM_OPT_FLAGS" TESTBUILDDIR=$(pwd)
cd src
# so including <sys/apparmor.h> in the next builds works
ln -s . sys
# same for <aalogparse/aalogparse.h>
ln -s . aalogparse
popd

# parser
pushd parser
%make CFLAGS="$RPM_OPT_FLAGS" TESTBUILDDIR=$(pwd)
popd

# pam
pushd changehat/pam_apparmor
%make   LDFLAGS="-L../libapparmor/src/.libs" \
        TESTBUILDDIR=$(pwd) \
        CFLAGS="$RPM_OPT_FLAGS -I../libapparmor/src"
popd

# utils
pushd utils
%make TESTBUILDDIR=$(pwd) CFLAGS="$RPM_OPT_FLAGS"
popd

# mod_apparmor
pushd changehat/mod_apparmor
%make   LIBAPPARMOR_FLAGS="-L../libapparmor/src/.libs -lapparmor -I../libapparmor/src" \
        TESTBUILDDIR=$(pwd)
popd

# dbus
pushd management/apparmor-dbus
./autogen.sh
export LDFLAGS="-L../../changehat/libapparmor/src/.libs -L../../../changehat/libapparmor/src/.libs"
export CFLAGS="$RPM_OPT_FLAGS -I../../changehat/libapparmor/src -I../../../changehat/libapparmor/src"
%configure
%make 
popd

# gnome applet
pushd management/applets/apparmorapplet-gnome
./autogen.sh --prefix=%{_prefix} --libexecdir=%{_libexecdir}
%make
popd

%install
rm -rf %{buildroot}

# lib
pushd changehat/libapparmor
%makeinstall_std LIB=%{_lib} LIBDIR=%{_libdir}
mkdir -p %{buildroot}%{perl_vendorarch}
# XXX - for some reason, on i586 builds this file is not copied
install -m 0644 swig/perl/LibAppArmor.pm %{buildroot}%{perl_vendorarch}
# fix some perms
find %{buildroot} -type f -exec chmod 0644 {} \;
popd

# parser
pushd parser
%{makeinstall_std} DISTRO=redhat TESTBUILDDIR=$(pwd)
popd

# profiles
pushd profiles
%{makeinstall_std} EXTRASDIR=%{buildroot}%{_sysconfdir}/apparmor/profiles/extras
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/apparmor.d/
popd

# pam
pushd changehat/pam_apparmor
%{makeinstall_std} SECDIR=%{buildroot}/%{_lib}/security
popd

# utils
pushd utils
%{makeinstall_std} PERLDIR=%{buildroot}%{_libdir}/perl5/vendor_perl/Immunix
popd

# mod_apparmor
pushd changehat/mod_apparmor
%{makeinstall_std} APXS_INSTALL_DIR=%{_libdir}/apache-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/modules.d/
popd

# dbus
pushd management/apparmor-dbus
%{makeinstall_std}
popd

# gnome applet
pushd management/applets/apparmorapplet-gnome
%{makeinstall_std}
popd

# remove profiles shipped elsewhere
rm -f   %{buildroot}%{_sysconfdir}/apparmor.d/sbin.rpcbind \
        %{buildroot}%{_sysconfdir}/apparmor.d/usr.sbin.traceroute \
        %{buildroot}%{_sysconfdir}/apparmor.d/bin.ping \
        %{buildroot}%{_sysconfdir}/apparmor.d/bin.netstat \
        %{buildroot}%{_sysconfdir}/apparmor.d/sbin.syslogd \
        %{buildroot}%{_sysconfdir}/apparmor.d/sbin.klogd \
        %{buildroot}%{_sysconfdir}/apparmor.d/usr.sbin.ntpd
        

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%post parser
%_post_service apparmor
%_post_service aaeventd

%preun parser
%_preun_service apparmor
%_preun_service aaeventd

%post -n apache-mod_apparmor
if [ -f /var/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2;
fi

%postun -n apache-mod_apparmor
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/httpd ]; then
                %{_initrddir}/httpd restart 1>&2
        fi
fi

%posttrans profiles
/sbin/service apparmor condreload

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc changehat/libapparmor/COPYING.LGPL
%attr(0755,root,root) /%{_libdir}/*.so.*

%files -n perl-libapparmor
%defattr(-,root,root)
%{perl_vendorarch}/auto/LibAppArmor
%{perl_vendorarch}/LibAppArmor.pm

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/aalogparse/
%attr(0644,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.la
%attr(0644,root,root) %{_libdir}/*.a
%attr(0644,root,root) %{_includedir}/sys/*.h
%attr(0644,root,root) %{_mandir}/man2/aa_change_hat.2*

%files profiles
%defattr(-,root,root)
%dir %{_sysconfdir}/apparmor.d
%config(noreplace) %{_sysconfdir}/apparmor.d/usr.*
%config(noreplace) %{_sysconfdir}/apparmor.d/sbin.*
%dir %{_sysconfdir}/apparmor.d/abstractions
%dir %{_sysconfdir}/apparmor.d/program-chunks
%dir %{_sysconfdir}/apparmor.d/tunables
%config(noreplace) %{_sysconfdir}/apparmor.d/abstractions/*
%config(noreplace) %{_sysconfdir}/apparmor.d/program-chunks/*
%config(noreplace) %{_sysconfdir}/apparmor.d/tunables/*
%dir %{_sysconfdir}/apparmor
%dir %{_sysconfdir}/apparmor/profiles
%dir %{_sysconfdir}/apparmor/profiles/extras
%{_sysconfdir}/apparmor/profiles/extras/README
%config(noreplace) %{_sysconfdir}/apparmor/profiles/extras/usr.*
%config(noreplace) %{_sysconfdir}/apparmor/profiles/extras/etc.*
%config(noreplace) %{_sysconfdir}/apparmor/profiles/extras/sbin.*
%config(noreplace) %{_sysconfdir}/apparmor/profiles/extras/bin.*

%files parser
%defattr(-,root,root)
%doc parser/COPYING.GPL parser/README
%dir %{_sysconfdir}/apparmor
%config(noreplace) %{_sysconfdir}/apparmor/subdomain.conf
%{_sysconfdir}/init.d/aaeventd
%{_sysconfdir}/init.d/apparmor
# no lib64
%dir /lib/apparmor
/lib/apparmor/rc.apparmor.functions
/sbin/*
%{_datadir}/locale/*/*/apparmor-parser.mo
%{_mandir}/man5/apparmor.d.5*
%{_mandir}/man5/apparmor.vim.5*
%{_mandir}/man5/subdomain.conf.5*
%{_mandir}/man7/apparmor.7*
%{_mandir}/man8/apparmor_parser.8*
%{_var}/lib/apparmor

%files -n pam_apparmor
%defattr(-,root,root)
%doc changehat/pam_apparmor/README changehat/pam_apparmor/COPYING
%attr(0755,root,root) /%{_lib}/security/*.so

%files utils
%defattr(-,root,root)
%dir %{_sysconfdir}/apparmor
%config(noreplace) %{_sysconfdir}/apparmor/logprof.conf
%config(noreplace) %{_sysconfdir}/apparmor/severity.db
%{_datadir}/locale/*/*/apparmor-utils.mo
%{_sbindir}/*
%{_libdir}/perl5/vendor_perl/Immunix
%{_var}/log/apparmor
%{_mandir}/man5/logprof.conf.5*
%{_mandir}/man8/aa-autodep.8*
%{_mandir}/man8/aa-complain.8*
%{_mandir}/man8/aa-enforce.8*
%{_mandir}/man8/aa-genprof.8*
%{_mandir}/man8/aa-logprof.8*
%{_mandir}/man8/aa-status.8*
%{_mandir}/man8/aa-unconfined.8*
%{_mandir}/man8/apparmor_status.8*
%{_mandir}/man8/autodep.8*
%{_mandir}/man8/complain.8*
%{_mandir}/man8/enforce.8*
%{_mandir}/man8/genprof.8*
%{_mandir}/man8/logprof.8*
%{_mandir}/man8/unconfined.8*
%{_mandir}/man8/aa-audit.8*
%{_mandir}/man8/audit.8*

%files -n apache-mod_apparmor
%defattr(-,root,root,-)
%doc changehat/mod_apparmor/COPYING.LGPL
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/B15_mod_apparmor.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_apparmor.so
%attr(0644,root,root) %{_mandir}/man8/mod_apparmor.8*

%files dbus
%defattr(-,root,root)
%doc management/apparmor-dbus/README management/apparmor-dbus/AUTHORS
%doc management/apparmor-dbus/COPYING
%{_bindir}/apparmor-dbus

%files applet-gnome
%defattr(-,root,root)
%{_prefix}/lib/bonobo/servers/*
%{_libexecdir}/apparmorapplet
%{_datadir}/pixmaps/*

