%define rev 906

Summary:	PAM module for AppArmor
Name:		pam_apparmor
Version:	2.3
Release:	%mkrel 1.%{rev}.1
License:	GPL
Group:		System/Libraries
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	pam_apparmor-%{version}-%{rev}.tar.gz
Patch:          pam_apparmor-2.1.2-906-ldflags.patch
BuildRequires:  libapparmor-devel
BuildRequires:  libpam-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

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
rm -rf %{buildroot}

%{makeinstall_std} SECDIR=%{buildroot}/%{_lib}/security

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README COPYING
%attr(0755,root,root) /%{_lib}/security/*.so

