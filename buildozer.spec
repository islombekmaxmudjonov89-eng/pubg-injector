[app]
# Ilova ma'lumotlari
title = PUBG Injector
package.name = pubginjector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Requirements (Flask va Kivy)
requirements = python3,kivy==2.3.0,flask,jinja2,werkzeug,itsdangerous,click

# Ekran sozlamalari
orientation = portrait
fullscreen = 1

# Ruxsatnomalar (Server ishlashi uchun)
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# API sozlamalari (Buildozer buni o'zi boshqaradi, versiyalar o'chirildi)
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

# Arxitektura
android.archs = armeabi-v7a, arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
