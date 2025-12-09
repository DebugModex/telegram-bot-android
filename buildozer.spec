[app]
title = Telegram Bot
package.name = mytelegramapp
package.domain = com.example
version = 1.0.0
version.code = 1

source.dir = .
source.main = main.py

requirements = python3, kivy==2.1.0, requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.minapi = 21
android.targetapi = 33
android.archs = arm64-v8a

p4a.bootstrap = sdl2
android.accept_sdk_license = True

[buildozer]
log_level = 2
