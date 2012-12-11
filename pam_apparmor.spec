%define rev 906

Summary:	PAM module for AppArmor
Name:		pam_apparmor
Version:	2.3
Release:	%mkrel 1.%{rev}.6
License:	GPL
Group:		System/Libraries
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	pam_apparmor-%{version}-%{rev}.tar.gz
Patch0:         pam_apparmor-2.1.2-906-ldflags.patch
BuildRequires:  apparmor-devel
BuildRequires:  pam-devel

%description
AppArmor is a security framework that proactively protects the operating system
and applications.

This package contains the pam_apparmor module, which provides the means for any
pam applications that call pam_open_session() to automatically perform an
AppArmor change_hat operation in order to switch to a user-specific security
policy.


%prep
%setup -q
#%patch -p0 -b .ldflags

%build
%serverbuild

%make	CFLAGS="$RPM_OPT_FLAGS" \
        TESTBUILDDIR=$(pwd)

%install
%{makeinstall_std} SECDIR=%{buildroot}/%{_lib}/security

%files
%doc README COPYING
%attr(0755,root,root) /%{_lib}/security/*.so



%changelog
* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3-1.906.5mdv2011.0
+ Revision: 614469
- the mass rebuild of 2010.1 packages

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3-1.906.4mdv2010.1
+ Revision: 523545
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.3-1.906.3mdv2010.0
+ Revision: 426351
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 2.3-1.906.2mdv2009.1
+ Revision: 351655
- rebuild

* Wed Aug 06 2008 Luiz Fernando Capitulino <lcapitulino@mandriva.com> 2.3-1.906.1mdv2009.0
+ Revision: 264750
- updated to version 2.3

* Wed Feb 27 2008 Andreas Hasenack <andreas@mandriva.com> 2.1.2-1.906.1mdv2008.1
+ Revision: 175814
- updated pam_apparmor to 2.1.2-906
- copied to pam_apparmor

* Thu Jan 17 2008 Thierry Vignaud <tv@mandriva.org> 2.1-1.1076.2mdv2008.1
+ Revision: 154124
- rebuild for new perl

* Tue Jan 08 2008 Andreas Hasenack <andreas@mandriva.com> 2.1-1.1076.1mdv2008.1
+ Revision: 146893
- updated to svn revision 1076

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Sep 19 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.5mdv2008.0
+ Revision: 91191
- remove more profiles from standard package: they are shipped in their own packages now

* Wed Sep 19 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.4mdv2008.0
+ Revision: 91061
- drop rpcbind profile, it's shipped in the rpcbind package now

* Fri Sep 14 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.3mdv2008.0
+ Revision: 85766
- bonobo file is under a noarch libdir
- build dbus and gnome applet packages

* Fri Sep 14 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.1mdv2008.0
+ Revision: 85546
- install perl module in arch dir as the makefile does for x86_64 (doesn't seem right, though)
- make it not require an installed libapparmor-devel to build
- added swig to buildrequires
- added profile for rpcbind
- fix default syslog profile
- obsolete apparmor-docs (manpages are in each package now)
- better place for the LibAppArmor module
- build apache-mod_apparmor package
- install LibAppArmor.pm
- added utils subpackage
- Import apparmor

