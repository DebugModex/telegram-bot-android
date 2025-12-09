[app]
title = Telegram Bot Pro
package.name = telegrambotpro
package.domain = com.telegram
version = 1.0.0
version.code = 1

source.dir = .
source.main = main.py

requirements = python3, kivy==2.1.0, requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.minapi = 21
android.targetapi = 33
android.archs = arm64-v8a

p4a.bootstrap = sdl2
android.accept_sdk_license = True
android.allow_backup = True
android.usesCleartextTraffic = True

[buildozer]
log_level = 1
