[app]
title = Telegram Bot
package.name = telegrambot$(date +%s)  # یا یک نام ثابت منحصربفرد
package.domain = com.example
version = 1.0.0
version.code = 1

source.dir = .
source.main = main.py

requirements = python3, kivy==2.1.0

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.minapi = 21
android.targetapi = 33
android.archs = arm64-v8a

p4a.bootstrap = sdl2
android.accept_sdk_license = True

[buildozer]
log_level = 1
warn_on_root = 0  # این خط مهم!
