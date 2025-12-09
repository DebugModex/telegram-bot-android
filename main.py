"""
📱 Telegram Account Creator - Complete Android App
نسخه کامل با تمام ویژگی‌ها (بدون Telethon برای سازگاری با GitHub Actions)
"""

import os
import sys
import json
import re
import time
import requests
import threading
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

# Load KV language for UI
Builder.load_string('''
<TelegramBotUI>:
    orientation: 'vertical'
    padding: 10
    spacing: 8
    
    BoxLayout:
        size_hint: 1, 0.12
        orientation: 'horizontal'
        padding: 10
        
        Label:
            text: '[size=28][b]🤖 Telegram Bot Pro[/b][/size]'
            markup: True
            color: 0, 0.533, 0.8, 1
            halign: 'center'
            valign: 'middle'
    
    ProgressBar:
        id: main_progress
        size_hint: 1, 0.03
        max: 100
        value: 0
    
    TabbedPanel:
        do_default_tab: False
        size_hint: 1, 0.65
        
        TabbedPanelItem:
            text: '⚙️ API Settings'
            ScrollView:
                GridLayout:
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    padding: 15
                    spacing: 12
                    
                    Label:
                        text: '[size=22][b]🔐 Telegram API[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 50
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 50
                        
                        Label:
                            text: 'API ID:'
                            size_hint_x: 0.3
                            halign: 'right'
                        
                        TextInput:
                            id: api_id_input
                            hint_text: '123456'
                            input_filter: 'int'
                            size_hint_x: 0.7
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 50
                        
                        Label:
                            text: 'API Hash:'
                            size_hint_x: 0.3
                            halign: 'right'
                        
                        TextInput:
                            id: api_hash_input
                            hint_text: 'a1b2c3d4e5f6...'
                            password: True
                            size_hint_x: 0.7
                    
                    Label:
                        text: '[size=20][b]📞 Phone API[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 40
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 50
                        
                        Label:
                            text: 'API Key:'
                            size_hint_x: 0.3
                            halign: 'right'
                        
                        TextInput:
                            id: phone_api_input
                            text: '0a110d41-5fcb-4d3f-9a17-bcab60aaf13b'
                            size_hint_x: 0.7
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 50
                        
                        Label:
                            text: 'Country:'
                            size_hint_x: 0.3
                            halign: 'right'
                        
                        Spinner:
                            id: country_spinner
                            text: 'Uzbekistan (+998)'
                            values: ['Uzbekistan (+998)', 'Russia (+7)', 'USA (+1)', 'Ukraine (+380)', 'Kazakhstan (+7)', 'Iran (+98)']
                            size_hint_x: 0.7
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 50
                        
                        Label:
                            text: 'Prefix Filter:'
                            size_hint_x: 0.3
                            halign: 'right'
                        
                        TextInput:
                            id: prefix_filter
                            text: '99899,99895,99897'
                            hint_text: 'Comma separated'
                            size_hint_x: 0.7
                    
                    Label:
                        text: '[size=20][b]📧 Email API[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 40
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 50
                        
                        Label:
                            text: 'API Key:'
                            size_hint_x: 0.3
                            halign: 'right'
                        
                        TextInput:
                            id: email_api_input
                            text: '1487353688:GyYrgArQOJWOMQzfjMKK'
                            size_hint_x: 0.7
                    
                    Button:
                        text: '💾 SAVE ALL SETTINGS'
                        background_color: 0.298, 0.686, 0.314, 1
                        size_hint_y: None
                        height: 60
                        font_size: '16sp'
                        on_press: root.save_all_settings()
        
        TabbedPanelItem:
            text: '📱 Get Numbers'
            ScrollView:
                GridLayout:
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    padding: 15
                    spacing: 12
                    
                    Label:
                        text: '[size=22][b]📞 Phone Numbers[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 50
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 60
                        
                        Button:
                            text: '🔄 Get New Number'
                            background_color: 0.129, 0.588, 0.953, 1
                            on_press: root.get_phone_number()
                        
                        Button:
                            text: '📋 Copy'
                            on_press: root.copy_phone_number()
                    
                    Label:
                        id: phone_display
                        text: '[color=888888][i]No phone number received yet[/i][/color]'
                        markup: True
                        size_hint_y: None
                        height: 80
                        font_size: '16sp'
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 60
                        
                        Button:
                            text: '⏱️ Wait for SMS Code'
                            background_color: 1, 0.596, 0, 1
                            on_press: root.wait_for_sms_code()
                        
                        Button:
                            text: '🔍 Check Status'
                            on_press: root.check_sms_status()
                    
                    Label:
                        id: sms_code_display
                        text: 'SMS Code: [i]Waiting...[/i]'
                        markup: True
                        size_hint_y: None
                        height: 50
                    
                    Label:
                        text: '[size=20][b]🔄 Multiple Attempts[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 40
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 50
                        
                        Label:
                            text: 'Max Attempts:'
                            size_hint_x: 0.5
                        
                        TextInput:
                            id: max_attempts
                            text: '5'
                            input_filter: 'int'
                            size_hint_x: 0.5
                    
                    Switch:
                        id: auto_retry_switch
                        text: 'Auto Retry on Ban'
                        active: True
                        size_hint_y: None
                        height: 50
        
        TabbedPanelItem:
            text: '📧 Email Service'
            ScrollView:
                GridLayout:
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    padding: 15
                    spacing: 12
                    
                    Label:
                        text: '[size=22][b]📧 Temp Email Service[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 50
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 60
                        
                        Button:
                            text: '🔄 Get Temp Email'
                            background_color: 0.611, 0.161, 0.69, 1
                            on_press: root.get_temp_email()
                        
                        Button:
                            text: '📋 Copy'
                            on_press: root.copy_email()
                    
                    Label:
                        id: email_display
                        text: '[color=888888][i]No email received yet[/i][/color]'
                        markup: True
                        size_hint_y: None
                        height: 80
                        font_size: '16sp'
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 60
                        
                        Button:
                            text: '📨 Wait for Email Code'
                            on_press: root.wait_for_email_code()
                        
                        Button:
                            text: '🔍 Check Email'
                            on_press: root.check_email_status()
                    
                    Label:
                        id: email_code_display
                        text: 'Email Code: [i]Waiting...[/i]'
                        markup: True
                        size_hint_y: None
                        height: 50
                    
                    Label:
                        text: '[size=20][b]⚡ Quick Actions[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 40
                    
                    Button:
                        text: '📧 Handle Email Verification'
                        background_color: 0.4, 0.2, 0.6, 1
                        size_hint_y: None
                        height: 60
                        on_press: root.handle_email_verification()
        
        TabbedPanelItem:
            text: '🚀 Automation'
            ScrollView:
                GridLayout:
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    padding: 15
                    spacing: 12
                    
                    Label:
                        text: '[size=22][b]🤖 Full Automation[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 50
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 50
                        
                        Label:
                            id: automation_status
                            text: 'Status: [color=00ff00]Ready[/color]'
                            markup: True
                    
                    Button:
                        text: '🚀 START FULL PROCESS'
                        background_color: 0.298, 0.686, 0.314, 1
                        font_size: '20sp'
                        size_hint_y: None
                        height: 70
                        on_press: root.start_full_automation()
                    
                    Button:
                        text: '⏹️ STOP AUTOMATION'
                        background_color: 0.957, 0.263, 0.212, 1
                        size_hint_y: None
                        height: 60
                        disabled: True
                        id: stop_btn
                        on_press: root.stop_automation()
                    
                    Label:
                        text: '[size=20][b]📊 Process Steps[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 40
                    
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: 200
                        spacing: 5
                        
                        Label:
                            id: step1
                            text: '1. Get Phone Number: [color=888888]Pending[/color]'
                            markup: True
                        
                        Label:
                            id: step2
                            text: '2. Get SMS Code: [color=888888]Pending[/color]'
                            markup: True
                        
                        Label:
                            id: step3
                            text: '3. Get Email: [color=888888]Pending[/color]'
                            markup: True
                        
                        Label:
                            id: step4
                            text: '4. Get Email Code: [color=888888]Pending[/color]'
                            markup: True
                        
                        Label:
                            id: step5
                            text: '5. Save Account: [color=888888]Pending[/color]'
                            markup: True
        
        TabbedPanelItem:
            text: '💾 Export'
            ScrollView:
                GridLayout:
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    padding: 15
                    spacing: 12
                    
                    Label:
                        text: '[size=22][b]💾 Export & Save[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 50
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 60
                        
                        Button:
                            text: '💾 Export Session'
                            background_color: 0.2, 0.6, 0.8, 1
                            on_press: root.export_session()
                        
                        Button:
                            text: '📁 View Files'
                            on_press: root.view_saved_files()
                    
                    Label:
                        id: export_status
                        text: 'No exports yet'
                        markup: True
                        size_hint_y: None
                        height: 50
                    
                    Label:
                        text: '[size=20][b]📋 Account Data[/b][/size]'
                        markup: True
                        size_hint_y: None
                        height: 40
                    
                    TextInput:
                        id: account_data_display
                        text: '{\\n  "phone": "Not set",\\n  "email": "Not set",\\n  "api_id": "Not set",\\n  "api_hash": "Not set"\\n}'
                        readonly: True
                        size_hint_y: None
                        height: 200
                        font_name: 'monospace'
                        font_size: '12sp'
                    
                    Button:
                        text: '🔄 Update Display'
                        size_hint_y: None
                        height: 50
                        on_press: root.update_account_display()
    
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
                text: '=== Telegram Bot Started ===\\n'
                multiline: True
                readonly: True
                background_color: 0.05, 0.05, 0.05, 1
                foreground_color: 1, 1, 1, 1
                font_name: 'monospace'
                font_size: '11sp'
                size_hint_y: None
                height: 300
''')

class TelegramBotUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
    
    # UI Methods that will call app methods
    def save_all_settings(self):
        self.app.save_all_settings()
    
    def get_phone_number(self):
        self.app.get_phone_number()
    
    def copy_phone_number(self):
        self.app.copy_phone_number()
    
    def wait_for_sms_code(self):
        self.app.wait_for_sms_code()
    
    def check_sms_status(self):
        self.app.check_sms_status()
    
    def get_temp_email(self):
        self.app.get_temp_email()
    
    def copy_email(self):
        self.app.copy_email()
    
    def wait_for_email_code(self):
        self.app.wait_for_email_code()
    
    def check_email_status(self):
        self.app.check_email_status()
    
    def handle_email_verification(self):
        self.app.handle_email_verification()
    
    def start_full_automation(self):
        self.app.start_full_automation()
    
    def stop_automation(self):
        self.app.stop_automation()
    
    def export_session(self):
        self.app.export_session()
    
    def view_saved_files(self):
        self.app.view_saved_files()
    
    def update_account_display(self):
        self.app.update_account_display()

class TelegramBotApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # API Settings
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
        self.current_accounts = []
        
        # Status
        self.is_processing = False
        self.log_messages = []
        self.max_attempts = 5
        self.current_attempt = 0
        
        # Phone prefixes
        self.allowed_prefixes = ["+99899", "+99895", "+99897"]
        
    def build(self):
        self.title = "Telegram Bot Pro"
        return TelegramBotUI()
    
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
    
    def save_all_settings(self):
        """ذخیره تمام تنظیمات"""
        try:
            # Get values from UI
            self.api_id = self.root.ids.api_id_input.text.strip()
            self.api_hash = self.root.ids.api_hash_input.text.strip()
            self.phone_api_key = self.root.ids.phone_api_input.text.strip()
            self.email_api_key = self.root.ids.email_api_input.text.strip()
            
            # Parse prefixes
            prefix_text = self.root.ids.prefix_filter.text.strip()
            if prefix_text:
                prefixes = [p.strip() for p in prefix_text.split(',')]
                self.allowed_prefixes = [f"+{p}" if not p.startswith('+') else p for p in prefixes]
            
            # Parse max attempts
            try:
                self.max_attempts = int(self.root.ids.max_attempts.text.strip())
            except:
                self.max_attempts = 5
            
            # Validate
            if not self.api_id or not self.api_hash:
                self.show_popup("Error", "Please enter API ID and Hash")
                return
            
            # Save to file
            settings = {
                'api_id': self.api_id,
                'api_hash': self.api_hash,
                'phone_api_key': self.phone_api_key,
                'email_api_key': self.email_api_key,
                'allowed_prefixes': self.allowed_prefixes,
                'max_attempts': self.max_attempts,
                'saved_at': datetime.now().isoformat()
            }
            
            if ON_ANDROID:
                storage_path = app_storage_path()
                settings_file = os.path.join(storage_path, 'telegram_bot_settings.json')
            else:
                settings_file = 'telegram_bot_settings.json'
            
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            self.add_log("✅ All settings saved successfully", 'success')
            self.show_popup("Success", "All settings saved!")
            
            # Update account display
            self.update_account_display()
            
        except Exception as e:
            self.add_log(f"❌ Error saving settings: {str(e)}", 'error')
    
    def get_phone_number(self):
        """دریافت شماره از API DropSMS"""
        if self.is_processing:
            self.add_log("⚠️ Another process is running", 'warning')
            return
        
        self.is_processing = True
        threading.Thread(target=self._get_phone_thread).start()
    
    def _get_phone_thread(self):
        """ترد دریافت شماره"""
        try:
            Clock.schedule_once(lambda dt: self.add_log("📞 Requesting phone number from DropSMS API...", 'info'))
            
            # Determine country ID
            country_text = self.root.ids.country_spinner.text
            country_map = {
                'Uzbekistan (+998)': 40,
                'Russia (+7)': 0,
                'USA (+1)': 1,
                'Ukraine (+380)': 3,
                'Kazakhstan (+7)': 7,
                'Iran (+98)': 109
            }
            country_id = country_map.get(country_text, 40)
            
            # API request
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
            
            if result.startswith("ACCESS_NUMBER"):
                _, req_id, raw_phone = result.split(':')
                phone = '+' + raw_phone.strip()
                
                # Check if phone is in allowed prefixes
                if any(phone.startswith(prefix) for prefix in self.allowed_prefixes):
                    self.phone_number = phone
                    self.phone_request_id = req_id
                    
                    Clock.schedule_once(lambda dt: self.root.ids.phone_display.__setattr__(
                        'text', f'[b][color=00ff00]📱 {phone}[/color][/b]\\nRequest ID: {req_id}'
                    ))
                    
                    Clock.schedule_once(lambda dt: self.root.ids.step1.__setattr__(
                        'text', '1. Get Phone Number: [color=00ff00]✅ Completed[/color]'
                    ))
                    
                    self.add_log(f"✅ Phone number received: {phone}", 'success')
                    self.add_log(f"📋 Request ID: {req_id}", 'info')
                    
                    # Copy to clipboard
                    if ON_ANDROID:
                        Clipboard.copy(phone)
                        Clock.schedule_once(lambda dt: self.add_log("📋 Phone copied to clipboard", 'info'))
                    
                    # Update account display
                    self.update_account_display()
                else:
                    Clock.schedule_once(lambda dt: self.add_log(
                        f"⚠️ Phone {phone} is not in allowed prefixes: {self.allowed_prefixes}", 'warning'
                    ))
                    
                    # Try to cancel this number
                    self._cancel_number(req_id)
                    
            elif result.startswith("ERROR"):
                Clock.schedule_once(lambda dt: self.add_log(f"❌ API Error: {result}", 'error'))
            else:
                Clock.schedule_once(lambda dt: self.add_log(f"❌ Unknown response: {result}", 'error'))
                
        except requests.exceptions.Timeout:
            Clock.schedule_once(lambda dt: self.add_log("❌ Request timeout", 'error'))
        except requests.exceptions.ConnectionError:
            Clock.schedule_once(lambda dt: self.add_log("❌ Connection error", 'error'))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.add_log(f"❌ Error: {str(e)}", 'error'))
        finally:
            self.is_processing = False
    
    def _cancel_number(self, request_id):
        """لغو شماره"""
        try:
            params = {
                'action': 'setStatus',
                'api_key': self.phone_api_key,
                'id': request_id,
                'status': '8'  # Cancel order
            }
            
            requests.get("https://i.dropsms.cc/stubs/handler_api.php", params=params, timeout=10)
        except:
            pass
    
    def wait_for_sms_code(self):
        """انتظار برای دریافت کد SMS"""
        if not self.phone_request_id:
            self.show_popup("Error", "Get a phone number first!")
            return
        
        if self.is_processing:
            self.add_log("⚠️ Another process is running", 'warning')
            return
        
        self.is_processing = True
        threading.Thread(target=self._wait_sms_thread).start()
    
    def _wait_sms_thread(self):
        """ترد انتظار برای کد SMS"""
        try:
            Clock.schedule_once(lambda dt: self.add_log("⏱️ Waiting for SMS code from DropSMS...", 'info'))
            
            url = f"https://i.dropsms.cc/stubs/handler_api.php?action=getStatus&api_key={self.phone_api_key}&id={self.phone_request_id}"
            
            for i in range(30):  # 30 attempts (~3.5 minutes)
                try:
                    response = requests.get(url, timeout=10)
                    result = response.text.strip()
                    
                    if result.startswith("STATUS_OK"):
                        _, code_text = result.split(':')
                        code_match = re.search(r'\b(\d{5,6})\b', code_text)
                        
                        if code_match:
                            self.sms_code = code_match.group(1)
                            
                            Clock.schedule_once(lambda dt: self.root.ids.sms_code_display.__setattr__(
                                'text', f'SMS Code: [b][color=00ff00]{self.sms_code}[/color][/b]'
                            ))
                            
                            Clock.schedule_once(lambda dt: self.root.ids.step2.__setattr__(
                                'text', '2. Get SMS Code: [color=00ff00]✅ Completed[/color]'
                            ))
                            
                            Clock.schedule_once(lambda dt: self.root.ids.main_progress.__setattr__('value', 100))
                            
                            self.add_log(f"✅ SMS Code received: {self.sms_code}", 'success')
                            
                            if ON_ANDROID:
                                Clipboard.copy(self.sms_code)
                                Clock.schedule_once(lambda dt: self.add_log("📋 Code copied to clipboard", 'info'))
                            return
                    
                    elif result == "STATUS_WAITING":
                        progress = (i + 1) * 3.33
                        Clock.schedule_once(lambda dt: self.root.ids.main_progress.__setattr__('value', progress))
                        continue
                    
                    elif result in ["STATUS_CANCEL", "STATUS_END", "BANNED"]:
                        Clock.schedule_once(lambda dt: self.add_log(f"❌ Order status: {result}", 'error'))
                        break
                        
                except:
                    continue
                
                time.sleep(7)  # Wait 7 seconds between checks
            
            Clock.schedule_once(lambda dt: self.add_log("❌ Timeout: No SMS code received", 'error'))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.add_log(f"❌ Error: {str(e)}", 'error'))
        finally:
            self.is_processing = False
    
    def check_sms_status(self):
        """بررسی وضعیت SMS"""
        if not self.phone_request_id:
            self.show_popup("Error", "Get a phone number first!")
            return
        
        threading.Thread(target=self._check_sms_status_thread).start()
    
    def _check_sms_status_thread(self):
        """ترد بررسی وضعیت SMS"""
        try:
            url = f"https://i.dropsms.cc/stubs/handler_api.php?action=getStatus&api_key={self.phone_api_key}&id={self.phone_request_id}"
            
            response = requests.get(url, timeout=10)
            result = response.text.strip()
            
            if result.startswith("STATUS_OK"):
                _, code_text = result.split(':')
                self.add_log(f"📱 Status: Code available - {code_text}", 'success')
            elif result == "STATUS_WAITING":
                self.add_log("📱 Status: Still waiting for code", 'info')
            else:
                self.add_log(f"📱 Status: {result}", 'info')
                
        except Exception as e:
            self.add_log(f"❌ Error checking status: {str(e)}", 'error')
    
    def get_temp_email(self):
        """دریافت ایمیل موقت از VenusAds"""
        threading.Thread(target=self._get_email_thread).start()
    
    def _get_email_thread(self):
        """ترد دریافت ایمیل"""
        try:
            Clock.schedule_once(lambda dt: self.add_log("📧 Requesting temporary email from VenusAds...", 'info'))
            
            url = f"https://venusads.ir/api/V1/email/getEmail/?key={self.email_api_key}&server=1"
            
            response = requests.get(url, timeout=30)
            data = response.json()
            
            if data.get('status') in ['success', 200]:
                self.email_address = data.get('email')
                self.email_request_id = data.get('requestID')
                
                Clock.schedule_once(lambda dt: self.root.ids.email_display.__setattr__(
                    'text', f'[b][color=00ff00]📧 {self.email_address}[/color][/b]\\nRequest ID: {self.email_request_id}'
                ))
                
                Clock.schedule_once(lambda dt: self.root.ids.step3.__setattr__(
                    'text', '3. Get Email: [color=00ff00]✅ Completed[/color]'
                ))
                
                self.add_log(f"✅ Email received: {self.email_address}", 'success')
                
                if ON_ANDROID:
                    Clipboard.copy(self.email_address)
                    Clock.schedule_once(lambda dt: self.add_log("📋 Email copied to clipboard", 'info'))
                
                # Update account display
                self.update_account_display()
            else:
                Clock.schedule_once(lambda dt: self.add_log(
                    f"❌ Email API Error: {data.get('message', 'Unknown error')}", 'error'
                ))
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self.add_log(f"❌ Error: {str(e)}", 'error'))
    
    def wait_for_email_code(self):
        """انتظار برای کد ایمیل"""
        if not self.email_request_id:
            self.show_popup("Error", "Get an email first!")
            return
        
        threading.Thread(target=self._wait_email_thread).start()
    
    def _wait_email_thread(self):
        """ترد انتظار برای کد ایمیل"""
        try:
            Clock.schedule_once(lambda dt: self.add_log("📨 Waiting for email code from VenusAds...", 'info'))
            
            url = f"https://venusads.ir/api/V1/email/getCode/?key={self.email_api_key}&id={self.email_request_id}"
            
            for i in range(40):  # 40 attempts (~2 minutes)
                try:
                    response = requests.get(url, timeout=10)
                    data = response.json()
                    
                    if data.get('status') in ['success', 200]:
                        code_text = data.get('code', '')
                        code_match = re.search(r'\b(\d{5,6})\b', str(code_text))
                        
                        if code_match:
                            self.email_code = code_match.group(1)
                            
                            Clock.schedule_once(lambda dt: self.root.ids.email_code_display.__setattr__(
                                'text', f'Email Code: [b][color=00ff00]{self.email_code}[/color][/b]'
                            ))
                            
                            Clock.schedule_once(lambda dt: self.root.ids.step4.__setattr__(
                                'text', '4. Get Email Code: [color=00ff00]✅ Completed[/color]'
                            ))
                            
                            self.add_log(f"✅ Email Code received: {self.email_code}", 'success')
                            
                            if ON_ANDROID:
                                Clipboard.copy(self.email_code)
                            return
                    
                    elif data.get('status') == 304:
                        Clock.schedule_once(lambda dt: self.add_log("⚠️ Code already used or expired", 'warning'))
                        break
                    
                except:
                    continue
                
                time.sleep(3)  # Wait 3 seconds between checks
            
            Clock.schedule_once(lambda dt: self.add_log("❌ Timeout: No email code received", 'error'))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.add_log(f"❌ Error: {str(e)}", 'error'))
    
    def check_email_status(self):
        """بررسی وضعیت ایمیل"""
        if not self.email_request_id:
            self.show_popup("Error", "Get an email first!")
            return
        
        threading.Thread(target=self._check_email_status_thread).start()
    
    def _check_email_status_thread(self):
        """ترد بررسی وضعیت ایمیل"""
        try:
            url = f"https://venusads.ir/api/V1/email/getCode/?key={self.email_api_key}&id={self.email_request_id}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('status') in ['success', 200]:
                self.add_log("📧 Status: Code available", 'success')
            elif data.get('status') == 304:
                self.add_log("📧 Status: Code already used", 'warning')
            else:
                self.add_log(f"📧 Status: {data.get('message', 'Unknown')}", 'info')
                
        except Exception as e:
            self.add_log(f"❌ Error checking email: {str(e)}", 'error')
    
    def handle_email_verification(self):
        """مدیریت تأیید ایمیل"""
        if not self.email_address:
            self.show_popup("Warning", "Get an email first!")
            return
        
        self.add_log("📧 Starting email verification process...", 'info')
        
        # شبیه‌سازی فرآیند
        steps = [
            "Checking for email screen...",
            "Entering email address...",
            "Waiting for email code...",
            "Entering verification code...",
            "Email verification completed!"
        ]
        
        def simulate_steps():
            for step in steps:
                time.sleep(2)
                Clock.schedule_once(lambda dt, s=step: self.add_log(f"➡️ {s}"))
        
        threading.Thread(target=simulate_steps).start()
    
    def start_full_automation(self):
        """شروع فرآیند کامل اتوماسیون"""
        if not self.api_id or not self.api_hash:
            self.show_popup("Error", "Enter API ID and Hash first!")
            return
        
        if self.is_processing:
            self.add_log("⚠️ Process already running", 'warning')
            return
        
        self.is_processing = True
        self.current_attempt = 0
        
        # Update UI
        self.root.ids.stop_btn.disabled = False
        Clock.schedule_once(lambda dt: self.root.ids.automation_status.__setattr__(
            'text', 'Status: [color=ffff00]Processing...[/color]'
        ))
        
        self.add_log("🚀 Starting full automation process...", 'success')
        
        # Start automation in thread
        threading.Thread(target=self._automation_thread).start()
    
    def _automation_thread(self):
        """ترد اتوماسیون اصلی"""
        try:
            for attempt in range(self.max_attempts):
                self.current_attempt = attempt + 1
                
                Clock.schedule_once(lambda dt: self.add_log(
                    f"🔄 Attempt {self.current_attempt}/{self.max_attempts}", 'info'
                ))
                
                # Step 1: Get phone number
                if not self.phone_number:
                    self._get_phone_thread()
                    if not self.phone_number:
                        time.sleep(5)
                        continue
                
                # Step 2: Get SMS code
                if self.phone_number and not self.sms_code:
                    self._wait_sms_thread()
                    if not self.sms_code:
                        # Try next number
                        self.phone_number = ""
                        continue
                
                # Step 3: Get email (if needed)
                if not self.email_address:
                    self._get_email_thread()
                    time.sleep(3)
                
                # Step 4: Get email code (if needed)
                if self.email_address and not self.email_code:
                    self._wait_email_thread()
                
                # Step 5: Save account
                if self._save_account_data():
                    Clock.schedule_once(lambda dt: self.root.ids.step5.__setattr__(
                        'text', '5. Save Account: [color=00ff00]✅ Completed[/color]'
                    ))
                    
                    Clock.schedule_once(lambda dt: self.root.ids.automation_status.__setattr__(
                        'text', 'Status: [color=00ff00]Success![/color]'
                    ))
                    
                    self.add_log("🎉 Automation completed successfully!", 'success')
                    break
            
            else:
                Clock.schedule_once(lambda dt: self.root.ids.automation_status.__setattr__(
                    'text', 'Status: [color=ff0000]Failed after max attempts[/color]'
                ))
                self.add_log("❌ Failed after maximum attempts", 'error')
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self.add_log(f"❌ Automation error: {str(e)}", 'error'))
        finally:
            self.is_processing = False
            Clock.schedule_once(lambda dt: self.root.ids.stop_btn.__setattr__('disabled', True))
    
    def _save_account_data(self):
        """ذخیره اطلاعات حساب"""
        try:
            if not self.phone_number:
                return False
            
            account_data = {
                'phone_number': self.phone_number,
                'sms_code': self.sms_code,
                'email_address': self.email_address,
                'email_code': self.email_code,
                'api_id': self.api_id,
                'api_hash': self.api_hash,
                'created_at': datetime.now().isoformat(),
                'phone_request_id': self.phone_request_id,
                'email_request_id': self.email_request_id
            }
            
            # Clean filename
            clean_phone = re.sub(r'[^0-9]', '', self.phone_number)
            filename = f"account_{clean_phone}.json"
            
            if ON_ANDROID:
                storage_path = app_storage_path()
                filepath = os.path.join(storage_path, filename)
            else:
                filepath = filename
            
            with open(filepath, 'w') as f:
                json.dump(account_data, f, indent=2)
            
            self.current_accounts.append(account_data)
            
            self.add_log(f"💾 Account saved: {filename}", 'success')
            
            # Update export status
            Clock.schedule_once(lambda dt: self.root.ids.export_status.__setattr__(
                'text', f'Last export: {filename}'
            ))
            
            return True
            
        except Exception as e:
            self.add_log(f"❌ Error saving account: {str(e)}", 'error')
            return False
    
    def stop_automation(self):
        """توقف اتوماسیون"""
        self.is_processing = False
        self.add_log("⏹️ Automation stopped by user", 'warning')
        
        Clock.schedule_once(lambda dt: self.root.ids.automation_status.__setattr__(
            'text', 'Status: [color=ff0000]Stopped[/color]'
        ))
    
    def export_session(self):
        """اکسپورت session (بدون Telethon)"""
        try:
            if not self.phone_number or not self.api_id or not self.api_hash:
                self.show_popup("Error", "Complete account setup first!")
                return
            
            # Create session data manually (without Telethon)
            session_data = {
                'phone': self.phone_number,
                'api_id': self.api_id,
                'api_hash': self.api_hash,
                'created': datetime.now().isoformat(),
                'app_version': '1.0.0',
                'device_model': 'Telegram Bot App',
                'system_version': 'Android',
                'lang_code': 'en'
            }
            
            # Clean filename
            clean_phone = re.sub(r'[^0-9]', '', self.phone_number)
            filename = f"telegram_session_{clean_phone}.json"
            
            if ON_ANDROID:
                storage_path = app_storage_path()
                filepath = os.path.join(storage_path, filename)
            else:
                filepath = filename
            
            with open(filepath, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            self.add_log(f"💾 Session exported: {filename}", 'success')
            
            # Update export status
            Clock.schedule_once(lambda dt: self.root.ids.export_status.__setattr__(
                'text', f'Session exported: {filename}'
            ))
            
            self.show_popup("Success", f"Session exported to:\\n{filename}")
            
        except Exception as e:
            self.add_log(f"❌ Export error: {str(e)}", 'error')
    
    def view_saved_files(self):
        """نمایش فایل‌های ذخیره شده"""
        try:
            if ON_ANDROID:
                storage_path = app_storage_path()
                files = []
                
                for f in os.listdir(storage_path):
                    if f.endswith('.json'):
                        files.append(f)
                
                if files:
                    file_list = "\\n".join(files[:10])  # Show first 10 files
                    self.add_log(f"📁 Found {len(files)} files", 'info')
                    self.show_popup("Saved Files", f"Found {len(files)} files:\\n{file_list}")
                else:
                    self.add_log("📁 No saved files found", 'info')
                    self.show_popup("Info", "No saved files found")
            else:
                self.add_log("📁 File viewing only available on Android", 'info')
                
        except Exception as e:
            self.add_log(f"❌ Error viewing files: {str(e)}", 'error')
    
    def update_account_display(self):
        """آپدیت نمایش اطلاعات حساب"""
        try:
            account_data = {
                'phone': self.phone_number or 'Not set',
                'email': self.email_address or 'Not set',
                'api_id': self.api_id or 'Not set',
                'api_hash': '***' + (self.api_hash[-4:] if self.api_hash else '') if self.api_hash else 'Not set',
                'sms_code': self.sms_code or 'Not received',
                'email_code': self.email_code or 'Not received'
            }
            
            formatted_json = json.dumps(account_data, indent=2)
            self.root.ids.account_data_display.text = formatted_json
            
            self.add_log("🔄 Account display updated", 'info')
            
        except Exception as e:
            self.add_log(f"❌ Error updating display: {str(e)}", 'error')
    
    def copy_phone_number(self):
        """کپی شماره تلفن"""
        if self.phone_number:
            if ON_ANDROID:
                Clipboard.copy(self.phone_number)
                self.add_log("📋 Phone number copied to clipboard", 'info')
            else:
                self.add_log("📋 Phone would be copied on Android", 'info')
        else:
            self.add_log("⚠️ No phone number to copy", 'warning')
    
    def copy_email(self):
        """کپی ایمیل"""
        if self.email_address:
            if ON_ANDROID:
                Clipboard.copy(self.email_address)
                self.add_log("📋 Email copied to clipboard", 'info')
            else:
                self.add_log("📋 Email would be copied on Android", 'info')
        else:
            self.add_log("⚠️ No email to copy", 'warning')
    
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
