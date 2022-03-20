# TODO: package python3-curio and enable curio test
#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	Sniff out which async library your code is running under
Summary(pl.UTF-8):	Podsłuchiwanie, którą bibliotekę asynchroniczną wykorzystuje kod
Name:		python3-sniffio
Version:	1.2.0
Release:	1
License:	MIT or Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sniffio/
Source0:	https://files.pythonhosted.org/packages/source/s/sniffio/sniffio-%{version}.tar.gz
# Source0-md5:	2d7cc6c3a94d3357d333a4ade4a83de8
URL:		https://pypi.org/project/sniffio/
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
#BuildRequires:	python3-curio
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sniff out which async library your code is running under.

%description -l pl.UTF-8
Podsłuchiwanie, którą bibliotekę asynchroniczną wykorzystuje kod.

%package apidocs
Summary:	API documentation for Python sniffio module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sniffio
Group:		Documentation

%description apidocs
API documentation for Python sniffio module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sniffio.

%prep
%setup -q -n sniffio-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest sniffio/_tests -k 'not test_curio'
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/sniffio/_tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.MIT README.rst
%{py3_sitescriptdir}/sniffio
%{py3_sitescriptdir}/sniffio-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
