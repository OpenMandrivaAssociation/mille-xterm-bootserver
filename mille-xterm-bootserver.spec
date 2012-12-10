%define svn 2141

Summary:	Mille-xterm boot server component
Name:		mille-xterm-bootserver
Version:	1.0
Release:	%mkrel 0.%{svn}.7
License:	GPL
Group:		System/Servers
URL:		http://mille-xterm.revolutionlinux.com/mille-xterm
Source0:	%{name}-%{version}.tar.bz2
Patch0:		fix_python_scripts.patch
Requires:	python >= 2.4
Requires:	mille-xterm-busybox
Requires:	nfs-server
Requires:	pci_scan
Requires:	mille-xterm-loadbalancer-lbserver
Requires:	rsync
Requires:	xinetd
BuildRequires:	python-devel >= 2.4
BuildRequires:	perl
Conflicts:	clusternfs
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%define py_ver %(python -c "import sys; v=sys.version_info[:2]; print '%%d.%%d'%%v" 2>/dev/null || echo PYTHON-NOT-FOUND)
%define py_prefix %(python -c "import sys; print sys.prefix" 2>/dev/null || echo PYTHON-NOT-FOUND)
%define py_libdir %{py_prefix}/lib/python%{py_ver}

%description
The mille-xterm boot server is the component that handle the boot of linux
terminals. There are scripts to build boot media and configure de terminal
root, accessible by NFS. 

%prep

%setup -q
%patch0 -p0

perl -pi -e "s/devfsd/locales-en/;g" src/rpmlist.mdv2006

find . -type f | xargs perl -pi -e "s|/usr/lib/python2\.4|%{py_libdir}|g"

%build
python setup.py build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}

cp src/install-kernel %{buildroot}%{_bindir}
python setup.py install --root=%{buildroot} --record=INSTALLED_FILES
chmod 755 %{buildroot}%{py_libdir}/site-packages/mxterm/*.py

%clean
rm -rf %{buildroot}

%post
echo -e "\nInstallation complete !\nNow you can execute : mille-xterm-bootserver autoconfigure"
echo -e "This command will help you to configure this bootserver\n"

%files
%defattr(-,root,root)
%doc Changelog README AUTHORS COPYING INSTALL
%config(noreplace) %{_sysconfdir}/mille-xterm/bootserver.ini
%{_bindir}/*
%{py_puresitedir}/*
%{_localstatedir}/lib/mille-xterm-bootserver


%changelog
* Fri Nov 19 2010 Funda Wang <fwang@mandriva.org> 1.0-0.2141.7mdv2011.0
+ Revision: 598844
- update filelist

  + Bogdano Arendartchuk <bogdano@mandriva.com>
    - rebuild for python 2.7

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 1.0-0.2141.6mdv2010.0
+ Revision: 439805
- rebuild

* Tue Jan 06 2009 Funda Wang <fwang@mandriva.org> 1.0-0.2141.5mdv2009.1
+ Revision: 325769
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 1.0-0.2141.4mdv2008.1
+ Revision: 136579
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Aug 01 2007 Olivier Blin <oblin@mandriva.com> 1.0-0.2141.4mdv2008.0
+ Revision: 57698
- drop console-tools require (it's in basesystem)


* Sun Feb 25 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.2141.3mdv2007.0
+ Revision: 125554
- fix api compat (Mikael Andersson)

* Sun Feb 25 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.2141.2mdv2007.1
+ Revision: 125525
- fix hardcoded python version

* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.2141.1mdv2007.1
+ Revision: 117965
- fix python libdir
- Import mille-xterm-bootserver

* Fri Sep 29 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.2141.1mdk
- initial Mandriva package (mille-xterm import)

