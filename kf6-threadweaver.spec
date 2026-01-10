#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.22
%define		qtver		5.15.2
%define		kfname		threadweaver

Summary:	Helper for multithreaded programming
Name:		kf6-%{kfname}
Version:	6.22.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	d81f838c9319849b6d88d3bf51dafa20
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
ThreadWeaver is a helper for multithreaded programming. It uses a
job-based interface to queue tasks and execute them in an efficient
way.

You simply divide the workload into jobs, state the dependencies
between the jobs and ThreadWeaver will work out the most efficient way
of dividing the work between threads within a set of resource limits.

See the information on [use cases](@ref usecases) and [why
multithreading can help](@ref multithreading), as well as the usage
section below, for more detailed information.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6ThreadWeaver.so.6
%{_libdir}/libKF6ThreadWeaver.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/ThreadWeaver
%{_libdir}/cmake/KF6ThreadWeaver
%{_libdir}/libKF6ThreadWeaver.so
