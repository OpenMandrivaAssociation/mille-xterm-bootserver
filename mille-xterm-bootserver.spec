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

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc Changelog README AUTHORS COPYING INSTALL
%config(noreplace) %{_sysconfdir}/mille-xterm/bootserver.ini
%{_bindir}/install-kernel


