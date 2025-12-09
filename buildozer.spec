[app]
title = Telegram Account Creator
package.name = telegramaccountcreator
package.domain = com.telegram.bot
version = 1.0.0
version.code = 1

source.dir = .
source.main = main.py

requirements = python3, kivy==2.1.0, requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.minapi = 21
android.targetapi = 33
android.archs = arm64-v8a

p4a.bootstrap = sdl2
android.accept_sdk_license = True
android.allow_backup = True
android.usesCleartextTraffic = True

[buildozer]
log_level = 1
warn_on_root = 0
