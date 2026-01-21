[app]
title = PUBG Injector
package.name = pubginjector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,js
version = 0.1
requirements = python3,kivy,flask,jinja2,werkzeug,itsdangerous,click,hostpython3

orientation = portrait
fullscreen = 1
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

