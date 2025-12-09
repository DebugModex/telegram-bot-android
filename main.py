"""
📱 Telegram Account Creator - Android App (Root Version)
کامل خودکار با دسترسی روت برای کنترل ADB
"""

import os
import sys
import json
import re
import time
import requests
import threading
import asyncio
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.utils import get_color_from_hex
from kivy.lang import Builder

# Telethon import
try:
    from telethon import TelegramClient
    from telethon.tl.types import UpdateShortMessage
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False
    print("Telethon not available")

# Check if running on Android
ON_ANDROID = sys.platform == 'android'

if ON_ANDROID:
    from android.permissions import request_permissions, Permission
    from android.storage import app_storage_path
    from jnius import autoclass
    
    # Request permissions
    request_permissions([
        Permission.INTERNET,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE
    ])
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')

# ADB Functions for Rooted Android
def execute_command(cmd):
    """اجرای دستور شل با دسترسی سوپر‌یوزر"""
    try:
        if ON_ANDROID:
            # اجرای دستور با su
            full_cmd = f'su -c "{cmd}"'
            result = subprocess.run(
                full_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        else:
            # روی دسکتاپ
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), -1

def tap(x, y):
    """کلیک روی مختصات"""
    cmd = f'input tap {x} {y}'
    execute_command(cmd)

def type_text(text):
    """تایپ متن"""
    # فرار کردن کاراکترهای خاص
    text = text.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
    cmd = f'input text "{text}"'
    execute_command(cmd)

def input_keyevent(keycode):
    """ارسال رویداد کیبورد"""
    cmd = f'input keyevent {keycode}'
    execute_command(cmd)

def swipe(x1, y1, x2, y2, duration=300):
    """سوایپ"""
    cmd = f'input swipe {x1} {y1} {x2} {y2} {duration}'
    execute_command(cmd)

def get_ui_dump():
    """گرفتن دامپ رابط کاربری"""
    try:
        # ذخیره دامپ در حافظه داخلی
        dump_path = '/data/local/tmp/ui_dump.xml'
        cmd = f'uiautomator dump {dump_path}'
        execute_command(cmd)
        
        # خواندن فایل
        cmd = f'cat {dump_path}'
        output, error, code = execute_command(cmd)
        
        if output and '<?xml' in output:
            return output
        return None
    except:
        return None

def find_ui_element(text=None, desc=None, resource_id=None):
    """یافتن المان در رابط کاربری"""
    xml_content = get_ui_dump()
    if not xml_content:
        return None
    
    try:
        root = ET.fromstring(xml_content)
        
        for node in root.iter('node'):
            match = False
            
            if text and node.attrib.get('text') == text:
                match = True
            elif desc and node.attrib.get('content-desc') == desc:
                match = True
            elif resource_id and node.attrib.get('resource-id') == resource_id:
                match = True
            
            if match:
                bounds = node.attrib.get('bounds', '')
                coords = list(map(int, re.findall(r'\d+', bounds)))
                if len(coords) == 4:
                    x1, y1, x2, y2 = coords
                    return ((x1 + x2) // 2, (y1 + y2) // 2)
    except:
        pass
    
    return None

def wait_and_tap(text=None, desc=None, resource_id=None, timeout=15):
    """انتظار و کلیک روی المان"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        pos = find_ui_element(text=text, desc=desc, resource_id=resource_id)
        if pos:
            tap(pos[0], pos[1])
            return True
        time.sleep(1)
    return False

def clear_phone_input():
    """پاک کردن فیلد شماره"""
    # پیدا کردن فیلد شماره
    pos = find_ui_element(resource_id="org.telegram.messenger:id/phone_input")
    if pos:
        tap(pos[0], pos[1])
    else:
        tap(500, 500)
    
    time.sleep(0.5)
    
    # پاک کردن با space و delete
    for _ in range(2):
        input_keyevent(62)  # KEYCODE_SPACE
        time.sleep(0.1)
    
    for _ in range(15):
        input_keyevent(67)  # KEYCODE_DEL
        time.sleep(0.05)

# UI Code
Builder.load_string('''
<TelegramBotAppUI>:
    orientation: 'vertical'
    padding: 10
    spacing: 8
    
    BoxLayout:
        size_hint: 1, 0.12
        orientation: 'horizontal'
        
        Label:
            text: '[size=28][b]🤖 Telegram Bot[/b][/size]'
            markup: True
            color: 0, 0.533, 0.8, 1
            halign: 'center'
    
    ProgressBar:
        id: main_progress
        size_hint: 1, 0.03
        max: 100
        value: 0
    
    TabbedPanel:
        do_default_tab: False
        size_hint: 1, 0.65
        
        TabbedPanelItem:
            text: '🔐 API'
            BoxLayout:
                orientation: 'vertical'
                padding: 10
                spacing: 10
                
                Label:
                    text: '[size=18][b]Telegram API[/b][/size]'
                    markup: True
                    size_hint: 1, 0.15
                
                GridLayout:
                    cols: 2
                    spacing: 5
                    size_hint: 1, 0.4
                    
                    Label:
                        text: 'API ID:'
                        halign: 'right'
                    
                    TextInput:
                        id: api_id_input
                        hint_text: '123456'
                        input_filter: 'int'
                    
                    Label:
                        text: 'API Hash:'
                        halign: 'right'
                    
                    TextInput:
                        id: api_hash_input
                        hint_text: 'a1b2c3d4...'
                        password: True
                
                Label:
                    text: '[size=16][b]Phone API[/b][/size]'
                    markup: True
                    size_hint: 1, 0.1
                
                GridLayout:
                    cols: 2
                    spacing: 5
                    size_hint: 1, 0.25
                    
                    Label:
                        text: 'API Key:'
                        halign: 'right'
                    
                    TextInput:
                        id: phone_api_input
                        text: '0a110d41-5fcb-4d3f-9a17-bcab60aaf13b'
                    
                    Label:
                        text: 'Country:'
                        halign: 'right'
                    
                    Spinner:
                        id: country_spinner
                        text: 'Uzbekistan (40)'
                        values: ['Uzbekistan (40)', 'Russia (0)', 'USA (1)', 'Ukraine (3)', 'Kazakhstan (7)', 'Iran (109)']
                
                Button:
                    text: '💾 Save All Settings'
                    background_color: 0.298, 0.686, 0.314, 1
                    size_hint: 1, 0.1
                    on_press: root.save_settings()
        
        TabbedPanelItem:
            text: '📱 Control'
            ScrollView:
                GridLayout:
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    padding: 10
                    spacing: 10
                    
                    Label:
                        text: '[size=18][b]Bot Control Panel[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 40
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 50
                        
                        Button:
                            text: '📞 Get Number'
                            background_color: 0.129, 0.588, 0.953, 1
                            on_press: root.get_phone_number()
                        
                        Button:
                            text: '📧 Get Email'
                            background_color: 0.611, 0.161, 0.69, 1
                            on_press: root.get_temp_email()
                    
                    Label:
                        id: phone_label
                        text: '[i]No phone number[/i]'
                        markup: True
                        size_hint_y: None
                        height: 40
                    
                    Label:
                        id: email_label
                        text: '[i]No email[/i]'
                        markup: True
                        size_hint_y: None
                        height: 40
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 50
                        
                        Button:
                            text: '⏱️ Wait SMS Code'
                            background_color: 1, 0.596, 0, 1
                            on_press: root.wait_sms_code()
                        
                        Button:
                            text: '📨 Wait Email Code'
                            on_press: root.wait_email_code()
                    
                    Label:
                        id: sms_code_label
                        text: 'SMS Code: --'
                        markup: True
                        size_hint_y: None
                        height: 30
                    
                    Label:
                        id: email_code_label
                        text: 'Email Code: --'
                        markup: True
                        size_hint_y: None
                        height: 30
                    
                    Button:
                        text: '🚀 START FULL PROCESS'
                        background_color: 0.298, 0.686, 0.314, 1
                        font_size: '18sp'
                        size_hint_y: None
                        height: 70
                        on_press: root.start_full_process()
                    
                    Button:
                        text: '⏹️ STOP'
                        background_color: 0.957, 0.263, 0.212, 1
                        size_hint_y: None
                        height: 50
                        disabled: True
                        id: stop_btn
                        on_press: root.stop_process()
        
        TabbedPanelItem:
            text: '⚙️ Tools'
            BoxLayout:
                orientation: 'vertical'
                padding: 10
                spacing: 10
                
                Label:
                    text: '[size=18][b]Tools & Utilities[/b][/size]'
                    markup: True
                    size_hint: 1, 0.1
                
                Button:
                    text: '📱 Open Telegram'
                    size_hint: 1, 0.15
                    on_press: root.open_telegram()
                
                Button:
                    text: '🧹 Clear Phone Field'
                    size_hint: 1, 0.15
                    on_press: root.clear_phone_field()
                
                Button:
                    text: '🔍 Check Root Access'
                    size_hint: 1, 0.15
                    on_press: root.check_root()
                
                Button:
                    text: '📊 Device Info'
                    size_hint: 1, 0.15
                    on_press: root.get_device_info()
                
                Button:
                    text: '💾 Export Session'
                    size_hint: 1, 0.15
                    on_press: root.export_session()
                
                Button:
                    text: '🗑️ Clear Logs'
                    size_hint: 1, 0.15
                    on_press: root.clear_logs()
    
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 0.2
        
        Label:
            text: '[b]📝 Activity Log[/b]'
            markup: True
            size_hint: 1, 0.2
        
        ScrollView:
            size_hint: 1, 0.8
            
            TextInput:
                id: log_text
                text: 'Telegram Bot Started\\n'
                multiline: True
                readonly: True
                background_color: 0.05, 0.05, 0.05, 1
                foreground_color: 1, 1, 1, 1
                font_name: 'monospace'
                font_size: '12sp'
                size_hint_y: None
                height: 300
''')

class TelegramBotAppUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
    
    # UI Methods
    def save_settings(self):
        self.app.save_settings()
    
    def get_phone_number(self):
        self.app.get_phone_number()
    
    def get_temp_email(self):
        self.app.get_temp_email()
    
    def wait_sms_code(self):
        self.app.wait_for_sms_code()
    
    def wait_email_code(self):
        self.app.wait_for_email_code()
    
    def start_full_process(self):
        self.app.start_full_automation()
    
    def stop_process(self):
        self.app.stop_automation()
    
    def open_telegram(self):
        self.app.open_telegram_app()
    
    def clear_phone_field(self):
        self.app.clear_phone_input_field()
    
    def check_root(self):
        self.app.check_root_access()
    
    def get_device_info(self):
        self.app.get_device_information()
    
    def export_session(self):
        self.app.export_telegram_session()
    
    def clear_logs(self):
        self.app.clear_log_messages()

class TelegramBotApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Settings
        self.api_id = ""
        self.api_hash = ""
        self.phone_api_key = "0a110d41-5fcb-4d3f-9a17-bcab60aaf13b"
        self.email_api_key = "1487353688:GyYrgArQOJWOMQzfjMKK"
        
        # Runtime data
        self.phone_number = ""
        self.phone_request_id = ""
        self.email_address = ""
        self.email_request_id = ""
        self.sms_code = ""
        self.email_code = ""
        
        # Status
        self.is_running = False
        self.log_messages = []
        
        # ADB device info
        self.device_width = 1080
        self.device_height = 1920
        
    def build(self):
        self.title = "Telegram Bot (Root)"
        return TelegramBotAppUI()
    
    def add_log(self, message, msg_type='info'):
        """افزودن پیام به لاگ"""
        colors = {
            'info': '#FFFFFF',
            'success': '#00FF00',
            'error': '#FF0000',
            'warning': '#FFFF00',
            'debug': '#888888'
        }
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = colors.get(msg_type, '#FFFFFF')
        log_entry = f"[{timestamp}] {message}"
        
        self.log_messages.insert(0, log_entry)
        if len(self.log_messages) > 100:
            self.log_messages.pop()
        
        # Update UI
        if hasattr(self, 'root'):
            self.root.ids.log_text.text = '\n'.join(self.log_messages)
    
    def save_settings(self):
        """ذخیره تنظیمات"""
        try:
            self.api_id = self.root.ids.api_id_input.text.strip()
            self.api_hash = self.root.ids.api_hash_input.text.strip()
            self.phone_api_key = self.root.ids.phone_api_input.text.strip()
            
            if not self.api_id or not self.api_hash:
                self.show_popup("Error", "Please enter API ID and Hash")
                return
            
            # Save to file
            settings = {
                'api_id': self.api_id,
                'api_hash': self.api_hash,
                'phone_api_key': self.phone_api_key,
                'saved_at': datetime.now().isoformat()
            }
            
            if ON_ANDROID:
                storage_path = app_storage_path()
                settings_file = os.path.join(storage_path, 'telegram_bot_settings.json')
            else:
                settings_file = 'telegram_bot_settings.json'
            
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            self.add_log("✅ Settings saved successfully", 'success')
            self.show_popup("Success", "All settings saved!")
            
        except Exception as e:
            self.add_log(f"❌ Error saving settings: {str(e)}", 'error')
    
    def get_phone_number(self):
        """دریافت شماره از API"""
        if self.is_running:
            self.add_log("⚠️ Another process is running", 'warning')
            return
        
        threading.Thread(target=self._get_phone_thread).start()
    
    def _get_phone_thread(self):
        """ترد دریافت شماره"""
        try:
            self.add_log("📞 Requesting phone number from API...", 'info')
            
            # Parse country
            country_text = self.root.ids.country_spinner.text
            country_id = re.search(r'\((\d+)\)', country_text)
            country_id = int(country_id.group(1)) if country_id else 40
            
            # API call
            params = {
                'action': 'getNumber',
                'api_key': self.phone_api_key,
                'service': 'tg',
                'country': country_id
            }
            
            response = requests.get(
                "https://i.dropsms.cc/stubs/handler_api.php",
                params=params,
                timeout=30
            )
            
            result = response.text.strip()
            self.add_log(f"API Response: {result}", 'debug')
            
            if result.startswith("ACCESS_NUMBER"):
                _, req_id, raw_phone = result.split(':')
                phone = '+' + raw_phone.strip()
                
                # Check prefixes
                if phone.startswith(('+99899', '+99895', '+99897')):
                    self.phone_number = phone
                    self.phone_request_id = req_id
                    
                    Clock.schedule_once(lambda dt: self.root.ids.phone_label.__setattr__(
                        'text', f'📱 [b]{phone}[/b]'
                    ))
                    
                    self.add_log(f"✅ Number received: {phone}", 'success')
                    self.add_log(f"📋 Request ID: {req_id}", 'info')
                    
                    # Copy to clipboard
                    if ON_ANDROID:
                        Clipboard.copy(phone)
                        self.add_log("📋 Copied to clipboard", 'info')
                else:
                    self.add_log(f"⚠️ Number {phone} not in allowed prefixes", 'warning')
            else:
                self.add_log(f"❌ API Error: {result}", 'error')
                
        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}", 'error')
    
    def get_temp_email(self):
        """دریافت ایمیل موقت"""
        threading.Thread(target=self._get_email_thread).start()
    
    def _get_email_thread(self):
        """ترد دریافت ایمیل"""
        try:
            self.add_log("📧 Requesting temporary email...", 'info')
            
            url = f"https://venusads.ir/api/V1/email/getEmail/?key={self.email_api_key}&server=1"
            
            response = requests.get(url, timeout=30)
            data = response.json()
            
            self.add_log(f"Email API Response: {data}", 'debug')
            
            if data.get('status') in ['success', 200]:
                self.email_address = data.get('email')
                self.email_request_id = data.get('requestID')
                
                Clock.schedule_once(lambda dt: self.root.ids.email_label.__setattr__(
                    'text', f'📧 [b]{self.email_address}[/b]'
                ))
                
                self.add_log(f"✅ Email received: {self.email_address}", 'success')
                self.add_log(f"📋 Request ID: {self.email_request_id}", 'info')
                
                if ON_ANDROID:
                    Clipboard.copy(self.email_address)
            else:
                self.add_log(f"❌ Email API Error: {data.get('message')}", 'error')
                
        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}", 'error')
    
    def wait_for_sms_code(self):
        """انتظار برای کد SMS"""
        if not self.phone_request_id:
            self.show_popup("Error", "Get a phone number first!")
            return
        
        threading.Thread(target=self._wait_sms_thread).start()
    
    def _wait_sms_thread(self):
        """ترد انتظار برای کد SMS"""
        try:
            self.add_log("⏱️ Waiting for SMS code...", 'info')
            
            url = f"https://i.dropsms.cc/stubs/handler_api.php?action=getStatus&api_key={self.phone_api_key}&id={self.phone_request_id}"
            
            for i in range(30):  # 30 attempts
                response = requests.get(url, timeout=10)
                result = response.text.strip()
                
                self.add_log(f"Check {i+1}: {result}", 'debug')
                
                if result.startswith("STATUS_OK"):
                    _, code_text = result.split(':')
                    code_match = re.search(r'\b(\d{5,6})\b', code_text)
                    
                    if code_match:
                        self.sms_code = code_match.group(1)
                        Clock.schedule_once(lambda dt: self.root.ids.sms_code_label.__setattr__(
                            'text', f'SMS Code: [b][color=00ff00]{self.sms_code}[/color][/b]'
                        ))
                        
                        self.add_log(f"✅ SMS Code: {self.sms_code}", 'success')
                        
                        if ON_ANDROID:
                            Clipboard.copy(self.sms_code)
                            self.add_log("📋 Code copied to clipboard", 'info')
                        return
                
                Clock.schedule_once(lambda dt: self.root.ids.main_progress.__setattr__(
                    'value', (i + 1) * 3.33
                ))
                
                time.sleep(7)  # Check every 7 seconds
            
            self.add_log("❌ Timeout: No SMS code received", 'error')
            
        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}", 'error')
    
    def wait_for_email_code(self):
        """انتظار برای کد ایمیل"""
        if not self.email_request_id:
            self.show_popup("Error", "Get an email first!")
            return
        
        threading.Thread(target=self._wait_email_thread).start()
    
    def _wait_email_thread(self):
        """ترد انتظار برای کد ایمیل"""
        try:
            self.add_log("📨 Waiting for email code...", 'info')
            
            url = f"https://venusads.ir/api/V1/email/getCode/?key={self.email_api_key}&id={self.email_request_id}"
            
            for i in range(40):  # 40 attempts
                response = requests.get(url, timeout=10)
                data = response.json()
                
                if data.get('status') in ['success', 200]:
                    code_text = data.get('code', '')
                    code_match = re.search(r'\b(\d{5,6})\b', str(code_text))
                    
                    if code_match:
                        self.email_code = code_match.group(1)
                        Clock.schedule_once(lambda dt: self.root.ids.email_code_label.__setattr__(
                            'text', f'Email Code: [b][color=00ff00]{self.email_code}[/color][/b]'
                        ))
                        
                        self.add_log(f"✅ Email Code: {self.email_code}", 'success')
                        
                        if ON_ANDROID:
                            Clipboard.copy(self.email_code)
                        return
                
                Clock.schedule_once(lambda dt: self.root.ids.main_progress.__setattr__(
                    'value', (i + 1) * 2.5
                ))
                
                time.sleep(3)  # Check every 3 seconds
            
            self.add_log("❌ Timeout: No email code received", 'error')
            
        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}", 'error')
    
    def start_full_automation(self):
        """شروع فرآیند کامل اتوماسیون"""
        if not self.phone_number:
            self.show_popup("Error", "Get a phone number first!")
            return
        
        if not self.api_id or not self.api_hash:
            self.show_popup("Error", "Enter API ID and Hash first!")
            return
        
        self.is_running = True
        self.root.ids.stop_btn.disabled = False
        
        self.add_log("🚀 Starting full automation process...", 'success')
        
        # Start automation in separate thread
        threading.Thread(target=self._automation_thread).start()
    
    def _automation_thread(self):
        """ترد اتوماسیون اصلی"""
        try:
            # Step 1: Launch Telegram
            self.add_log("📱 Launching Telegram...", 'info')
            self._launch_telegram()
            time.sleep(5)
            
            # Step 2: Tap Start Messaging
            self.add_log("👆 Tapping 'Start Messaging'...", 'info')
            if not wait_and_tap(text="Start Messaging", timeout=10):
                self.add_log("⚠️ Could not find Start Messaging, trying coordinates", 'warning')
                tap(540, 1600)  # Center of screen
            
            time.sleep(3)
            
            # Step 3: Clear phone field
            self.add_log("🧹 Clearing phone field...", 'info')
            clear_phone_input()
            time.sleep(1)
            
            # Step 4: Enter phone number
            self.add_log(f"⌨️ Entering phone: {self.phone_number}", 'info')
            type_text(self.phone_number)
            time.sleep(1)
            
            # Step 5: Press Enter
            self.add_log("↵ Pressing Enter...", 'info')
            input_keyevent(66)  # KEYCODE_ENTER
            time.sleep(2)
            
            # Step 6: Handle banned number
            self.add_log("🔍 Checking for banned number...", 'info')
            if self._check_banned_number():
                self.add_log("🚫 Number is banned, trying next...", 'error')
                return
            
            # Step 7: Check for email verification
            self.add_log("📧 Checking email verification...", 'info')
            if self._check_email_screen():
                self._handle_email_verification()
            
            # Step 8: Wait for SMS code
            self.add_log("⏱️ Waiting for SMS code...", 'info')
            sms_code = self._get_sms_code_from_api()
            
            if sms_code:
                self.add_log(f"✅ SMS Code: {sms_code}", 'success')
                
                # Step 9: Enter SMS code
                self.add_log("⌨️ Entering SMS code...", 'info')
                self._enter_verification_code(sms_code)
                time.sleep(3)
                
                # Step 10: Enter name
                self.add_log("👤 Setting up profile...", 'info')
                self._enter_profile_info()
                time.sleep(2)
                
                # Step 11: Complete registration
                self.add_log("✅ Registration completed!", 'success')
                
                # Step 12: Export session
                self.add_log("💾 Exporting Telegram session...", 'info')
                self._export_telegram_session()
                
                self.add_log("🎉 ALL DONE! Account created successfully!", 'success')
            else:
                self.add_log("❌ Failed to get SMS code", 'error')
            
        except Exception as e:
            self.add_log(f"❌ Automation error: {str(e)}", 'error')
        finally:
            self.is_running = False
            Clock.schedule_once(lambda dt: self.root.ids.stop_btn.__setattr__('disabled', True))
    
    def _launch_telegram(self):
        """باز کردن تلگرام"""
        cmd = 'monkey -p org.telegram.messenger 1'
        execute_command(cmd)
    
    def _check_banned_number(self):
        """بررسی بن شدن شماره"""
        banned_texts = ["banned", "blocked", "مسدود"]
        for text in banned_texts:
            if find_ui_element(text=text):
                self.add_log(f"🚫 Banned detected: {text}", 'error')
                
                # Tap OK
                if wait_and_tap(text="OK", timeout=3) or wait_and_tap(text="بله", timeout=3):
                    time.sleep(2)
                
                # Clear field
                clear_phone_input()
                return True
        return False
    
    def _check_email_screen(self):
        """بررسی صفحه ایمیل"""
        return find_ui_element(text="Choose a login email") or \
               find_ui_element(resource_id="org.telegram.messenger:id/login_email_input")
    
    def _handle_email_verification(self):
        """مدیریت تأیید ایمیل"""
        self.add_log("📧 Email verification required", 'info')
        
        # Get email if not already
        if not self.email_address:
            self.get_temp_email()
            time.sleep(5)
        
        if self.email_address:
            # Enter email
            email_field = find_ui_element(resource_id="org.telegram.messenger:id/login_email_input")
            if email_field:
                tap(email_field[0], email_field[1])
                type_text(self.email_address)
                time.sleep(1)
                
                # Tap Next
                if wait_and_tap(text="Next", timeout=3) or wait_and_tap(desc="Next", timeout=3):
                    time.sleep(4)
                    
                    # Wait for email code
                    self.add_log("⏱️ Waiting for email code...", 'info')
                    email_code = self._get_email_code_from_api()
                    
                    if email_code:
                        self.add_log(f"✅ Email Code: {email_code}", 'success')
                        self._enter_verification_code(email_code)
                        return True
        
        return False
    
    def _get_sms_code_from_api(self):
        """دریافت کد SMS از API"""
        try:
            url = f"https://i.dropsms.cc/stubs/handler_api.php?action=getStatus&api_key={self.phone_api_key}&id={self.phone_request_id}"
            
            for i in range(20):
                response = requests.get(url, timeout=10)
                result = response.text.strip()
                
                if result.startswith("STATUS_OK"):
                    _, code_text = result.split(':')
                    code_match = re.search(r'\b(\d{5,6})\b', code_text)
                    if code_match:
                        return code_match.group(1)
                
                time.sleep(7)
            
            return None
        except:
            return None
    
    def _get_email_code_from_api(self):
        """دریافت کد ایمیل از API"""
        try:
            url = f"https://venusads.ir/api/V1/email/getCode/?key={self.email_api_key}&id={self.email_request_id}"
            
            for i in range(20):
                response = requests.get(url, timeout=10)
                data = response.json()
                
                if data.get('status') in ['success', 200]:
                    code_text = data.get('code', '')
                    code_match = re.search(r'\b(\d{5,6})\b', str(code_text))
                    if code_match:
                        return code_match.group(1)
                
                time.sleep(5)
            
            return None
        except:
            return None
    
    def _enter_verification_code(self, code):
        """وارد کردن کد تأیید"""
        # Find code field
        code_field = find_ui_element(resource_id="org.telegram.messenger:id/code_input_field")
        if code_field:
            tap(code_field[0], code_field[1])
        else:
            tap(540, 800)  # Middle of screen
        
        time.sleep(1)
        type_text(code)
        time.sleep(2)
        
        # Press Next/Done
        input_keyevent(66)  # ENTER
        time.sleep(2)
    
    def _enter_profile_info(self):
        """وارد کردن اطلاعات پروفایل"""
        # First name
        first_name_field = find_ui_element(resource_id="org.telegram.messenger:id/first_name_field")
        if first_name_field:
            tap(first_name_field[0], first_name_field[1])
            type_text("Ali")
        else:
            tap(300, 550)
            type_text("Ali")
        
        time.sleep(1)
        
        # Last name
        last_name_field = find_ui_element(resource_id="org.telegram.messenger:id/last_name_field")
        if last_name_field:
            tap(last_name_field[0], last_name_field[1])
            type_text("Karimi")
        else:
            tap(300, 650)
            type_text("Karimi")
        
        time.sleep(1)
        
        # Done/Next
        if wait_and_tap(text="Done", timeout=3) or wait_and_tap(desc="Done", timeout=3):
            pass
        else:
            input_keyevent(66)  # ENTER
        
        time.sleep(3)
    
    def _export_telegram_session(self):
        """اکسپورت session تلگرام"""
        if not TELETHON_AVAILABLE:
            self.add_log("⚠️ Telethon not installed", 'warning')
            return
        
        try:
            asyncio.run(self._async_export_session())
        except:
            # Create simple session file
            session_data = {
                'phone': self.phone_number,
                'api_id': self.api_id,
                'api_hash': self.api_hash,
                'created': datetime.now().isoformat()
            }
            
            if ON_ANDROID:
                storage_path = app_storage_path()
                filename = os.path.join(storage_path, f"telegram_session_{self.phone_number[1:]}.json")
            else:
                filename = f"telegram_session_{self.phone_number[1:]}.json"
            
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            self.add_log(f"✅ Session saved: {filename}", 'success')
    
    async def _async_export_session(self):
        """اکسپورت async session"""
        try:
            session_name = re.sub(r'[^a-zA-Z0-9]', '', self.phone_number.strip('+'))
            client = TelegramClient(session_name, self.api_id, self.api_hash)
            
            await client.connect()
            
            if not await client.is_user_authorized():
                await client.send_code_request(self.phone_number)
                
                # Wait for code
                code = None
                for i in range(10):
                    updates = await client.get_updates(limit=10)
                    for update in updates:
                        if isinstance(update, UpdateShortMessage):
                            if "code" in update.message.lower():
                                code_match = re.search(r'\b(\d{5})\b', update.message)
                                if code_match:
                                    code = code_match.group(1)
                                    break
                    if code:
                        break
                    await asyncio.sleep(3)
                
                if code:
                    await client.sign_in(self.phone_number, code)
            
            # Export session
            session_data = await client.export_session()
            
            if ON_ANDROID:
                storage_path = app_storage_path()
                filename = os.path.join(storage_path, f"telegram_session_{self.phone_number[1:]}.json")
            else:
                filename = f"telegram_session_{self.phone_number[1:]}.json"
            
            with open(filename, 'w') as f:
                json.dump(json.loads(session_data), f, indent=4)
            
            self.add_log(f"✅ Telethon session exported: {filename}", 'success')
            
            await client.disconnect()
            
        except Exception as e:
            self.add_log(f"❌ Telethon error: {str(e)}", 'error')
    
    def stop_automation(self):
        """توقف اتوماسیون"""
        self.is_running = False
        self.add_log("⏹️ Automation stopped", 'warning')
    
    def open_telegram_app(self):
        """باز کردن اپلیکیشن تلگرام"""
        self._launch_telegram()
        self.add_log("📱 Opening Telegram...", 'info')
    
    def clear_phone_input_field(self):
        """پاک کردن فیلد شماره"""
        clear_phone_input()
        self.add_log("🧹 Phone field cleared", 'info')
    
    def check_root_access(self):
        """بررسی دسترسی روت"""
        output, error, code = execute_command('su -c "echo Root Check"')
        
        if code == 0:
            self.add_log("✅ Root access confirmed", 'success')
            self.show_popup("Root Access", "Root access is available!")
        else:
            self.add_log("❌ No root access", 'error')
            self.show_popup("Root Access", "Root access is NOT available!")
    
    def get_device_information(self):
        """دریافت اطلاعات دستگاه"""
        try:
            # Get screen size
            output, error, code = execute_command('wm size')
            self.add_log(f"📱 Screen: {output}", 'info')
            
            # Get Android version
            output, error, code = execute_command('getprop ro.build.version.release')
            self.add_log(f"🤖 Android: {output}", 'info')
            
            # Get device model
            output, error, code = execute_command('getprop ro.product.model')
            self.add_log(f"📦 Model: {output}", 'info')
            
        except Exception as e:
            self.add_log(f"❌ Device info error: {str(e)}", 'error')
    
    def export_telegram_session(self):
        """اکسپورت session"""
        self._export_telegram_session()
    
    def clear_log_messages(self):
        """پاک کردن لاگ‌ها"""
        self.log_messages = []
        self.root.ids.log_text.text = "Logs cleared.\n"
        self.add_log("🗑️ Logs cleared", 'info')
    
    def show_popup(self, title, message):
        """نمایش پنجره پیام"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        
        btn = Button(text='OK', size_hint=(1, 0.3))
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        
        popup.open()

if __name__ == '__main__':
    TelegramBotApp().run()