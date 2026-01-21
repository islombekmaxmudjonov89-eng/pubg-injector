[app]
title = AIGen Hybrid
package.name = aigen.hybrid.injector
package.domain = uz.aigen
source.dir = .
source.include_exts = py,png,jpg,html,js,css
version = 3.1.0

# BU YERDA KERAKLI KUTUBXONALAR
requirements = python3, kivy, flask, frida-tools, threading

# ANDROID RUXSATNOMALARI
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# ANDROID XUSUSIYATLARI
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

# WEBVIEW ISHLASHI UCHUN
p4a.branch = master