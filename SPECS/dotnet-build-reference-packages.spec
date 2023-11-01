%global debug_package %{nil}

%global commit 045b2888ccfaf4c203c945a09b3f41f0e6393d1c
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           dotnet-build-reference-packages
Version:        0
Release:        11.20211215git%{shortcommit}%{?dist}
Summary:        Reference packages needed by the .NET Core SDK build

License:        MIT
URL:            https://github.com/dotnet/source-build-reference-packages
Source0:        https://github.com/dotnet/source-build-reference-packages/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

%if 0%{?fedora} > 32 || 0%{?rhel} > 8
ExclusiveArch:  aarch64 x86_64
%else
ExclusiveArch:  x86_64
%endif

BuildRequires:  dotnet-sdk-3.1
BuildRequires:  dotnet-sdk-3.1-source-built-artifacts

# The files of dotnet5.0-build-reference-packages and this package
# conflict. They install to the same location and cointain a shared
# (sub)set of files. These packages aren't really meant to be used by
# end-users and a single .NET build will not require both.
Conflicts:      dotnet5.0-build-reference-packages

%description
This contains references packages used for building .NET Core.

This is not meant to be used by end-users.


%prep
%setup -q -n source-build-reference-packages-%{commit}

find -name '*.nupkg' -type f -delete
find -name '*.dll' -type f -delete
find -name '*.so' -type f -delete
find -name '*.tar.gz' -type f -delete

%build
find -iname 'nuget.config' -exec echo {} \; -exec cat {} \;

%{_libdir}/dotnet/dotnet --info

./build.sh \
  --with-sdk %{_libdir}/dotnet \
  --with-packages %{_libdir}/dotnet/source-built-artifacts/*.tar.gz

pushd artifacts/reference-packages
tar cvzf Private.SourceBuild.ReferencePackages.%{version}.tar.gz *.nupkg
popd
mv artifacts/reference-packages/Private.SourceBuild.ReferencePackages.%{version}.tar.gz .

%install
mkdir -p %{buildroot}/%{_libdir}/dotnet
cp -a artifacts/reference-packages %{buildroot}/%{_libdir}/dotnet/
cp -a Private.SourceBuild.ReferencePackages.%{version}.tar.gz %{buildroot}/%{_libdir}/dotnet/reference-packages/


%files
%dir %{_libdir}/dotnet/
%{_libdir}/dotnet/reference-packages/
%license LICENSE.txt


%changelog
* Wed Dec 15 2021 Omair Majid <omajid@redhat.com> - 0-11.20211215git045b288
- Update to upstream commit 045b288
- Related: RHBZ#2031429

* Wed Jun 09 2021 Omair Majid <omajid@redhat.com> - 0-10.20200608gitcd5a8c6
- Add Conflicts for dotnet5.0-build-reference-packages
- Resolves: RHBZ#1949264

* Wed May 26 2021 Omair Majid <omajid@redhat.com> - 0-9.20200608gitcd5a8c6
- Add gating tests

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-8.20200608gitcd5a8c6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-7.20200608gitcd5a8c6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Omair Majid <omajid@redhat.com> - 0-6.20200608gitcd5a8c6
- Update to upstream commit cd5a8c6

* Mon Jul 20 2020 Omair Majid <omajid@redhat.com> - 0-5.20200608git1b1a695
- Update to upstream commit 1b1a695

* Fri Jun 19 2020 Omair Majid <omajid@redhat.com> - 0-4.20200608git5aaf20d
- Enable building on aarch64

* Mon Jun 08 2020 Chris Rummel <crummel@microsoft.com> - 0-3.20200608git5aaf20d
- Updated to upstream commit 5aaf20d

* Tue Jun 02 2020 Omair Majid <omajid@redhat.com> - 0-3.20200528git6e2aee66e2aee6
- Updated to upstream commit 6e2aee6

* Wed Feb 19 2020 Radka Janekova <rjanekov@redhat.com> - 0-2.20200108git9cc7dad
- Added license reference
* Tue Feb 11 2020 Omair Majid <omajid@redhat.com> - 0-1.20200108git9cc7dad
- Initial package
