[app]

# (str) Title of your application
title = PUBG Injector

# (str) Package name
package.name = pubginjector

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Flask ishlashi uchun barcha kerakli kutubxonalar kiritildi
requirements = python3,kivy,flask,jinja2,werkzeug,itsdangerous,click

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions
# Server ishlashi uchun internet ruxsati shart
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded)
# android.ndk_path = 

# (list) Architecture to build for
android.archs = armeabi-v7a, arm64-v8a

# (bool) indicates whether the screen should stay on
# (uncomment to keep screen on)
# android.keep_screen_on = True

# (bool) If True, then skip the automatic update of the SDK/NDK
android.skip_update = False

# (bool) If True, then accept the SDK license agreement
android.accept_sdk_license = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
