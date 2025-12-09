[app]
title = Telegram Bot (Root)
package.name = telegrambotroot
package.domain = com.telegrambot
version = 1.0.0
version.code = 1
source.dir = .
source.main = main.py
requirements = python3, kivy==2.2.1, requests, pillow, telethon
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.minapi = 21
android.targetapi = 34
android.archs = arm64-v8a, armeabi-v7a
p4a.bootstrap = sdl2
android.accept_sdk_license = True
android.allow_backup = True
android.usesCleartextTraffic = True

# Extra Python modules
android.gradle_dependencies = 
android.add_jars = 
android.add_aars = 
android.add_jar_dir = 
android.add_aar_dir = 

[buildozer]
log_level = 2