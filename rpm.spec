Name:           mesa-panfrost
Version:        23.0.0
Release:        1%{?dist}
Summary:        Mesa Panfrost driver for aarch64 (no Vulkan, no LLVM)

License:        MIT
URL:            https://gitlab.freedesktop.org/mesa/mesa

# 仅适用于 aarch64
BuildArch:      aarch64

%description
Custom-built Mesa with Panfrost driver enabled, Vulkan and LLVM disabled.
Built for aarch64 platforms (e.g. Rockchip, Allwinner) with DRM/KMS support.

%package runtime
Summary:        Panfrost DRI driver and runtime libraries for aarch64
Requires:       libdrm, expat

%description runtime
Runtime libraries required to run OpenGL ES/EGL/GLES applications
using the Panfrost driver on aarch64 devices.
Includes:
- libEGL, libGLESv2, libGL, libgbm
- rockchip_dri.so
- Default drirc configuration


%post runtime
/sbin/ldconfig

%postun runtime
/sbin/ldconfig

%package devel
Summary:        Development headers and pkgconfig files for Mesa Panfrost
Requires:       %{name}-runtime = %{version}-%{release}

%description devel
Header files and pkg-config files for developing graphics applications
with EGL, OpenGL ES, and GBM on aarch64 using the Panfrost driver.

%prep
# 创建空目录结构，不编译
mkdir -p %{_topdir}/BUILD/%{name}-%{version}
%{nil}

%build
# 无需构建

%install
# 清空 buildroot
rm -rf %{buildroot}
mkdir -p %{buildroot}

# 假设你的安装产物在 ../dist/usr 下
cp -ar %{_specdir}/../install/usr %{buildroot}/

# 可选：清理其他 DRI 驱动（防止误打包）
# rm -f %{buildroot}/usr/lib64/dri/*_dri.so
# 重新放入 rockchip_dri.so（确保它是 Panfrost）
# 如果你的驱动是 panfrost_dri.so，替换 rockchip_dri.so
# cp %{_specdir}/../dist/usr/lib64/dri/panfrost_dri.so %{buildroot}/usr/lib64/dri/

%files
%defattr(-,root,root,-)
/usr/share/drirc.d/00-mesa-defaults.conf

%files runtime
%defattr(-,root,root,-)
/usr/lib64/libEGL.so.1*
/usr/lib64/libGLESv2.so.2*
/usr/lib64/libGLESv1_CM.so.1*
/usr/lib64/libGL.so.1*
/usr/lib64/libglapi.so.0*
/usr/lib64/libgbm.so.1*
/usr/lib64/libexpat.so.1*
/usr/lib64/dri/rockchip_dri.so

%files devel
%defattr(-,root,root,-)
/usr/include/EGL/
/usr/include/GL/
/usr/include/GLES/
/usr/include/GLES2/
/usr/include/GLES3/
/usr/include/KHR/
/usr/include/gbm.h
/usr/lib64/pkgconfig/*.pc
/usr/lib64/libEGL.so
/usr/lib64/libGLESv2.so
/usr/lib64/libGLESv1_CM.so
/usr/lib64/libGL.so
/usr/lib64/libglapi.so
/usr/lib64/libgbm.so
/usr/lib64/libexpat.so

%changelog
* Wed Jul 30 2025 wqhot <wqhot@outlook.com> - 23.0.0-1.aarch64
- Built for aarch64 with Panfrost only
- LLVM disabled, Vulkan disabled, Wayland disabled
- Subpackages: runtime and devel