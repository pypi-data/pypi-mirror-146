from kivy import Config
import os, darkdetect

Config.set('graphics', 'resizable', 1)
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', 0)
Config.write()

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.settings import ContentPanel
from kivymd.app import MDApp
from screeninfo import get_monitors
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty


def Help():
    print('''builder_string: str = '', app_name: str = '', list_of_files: list = None,
                 screen_size=None, min_x: int = 0.1, min_y: int = 0.1, center: bool = True,
                 run_at_build: bool = False, sun_icon: str = 'white-balance-sunny',
                 moon_icon: str = 'weather-night', main_color: str = 'Blue''')

def Spec(name: str, filename: str, icon: str, path: str = os.getcwd()):

    path = path.replace("\\", r"\\")

    print(fr"""
from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(['{filename}'],
             pathex=[{path}],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={{}},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='{name}',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None, icon='{icon}')

coll = COLLECT(exe, Tree('{path}'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='{name}')""")

class Kivy4(MDApp):

    def __init__(self, builder_string: str = '', app_name: str = '', list_of_files: list = None,
                 screen_size=None, min_x: int = 0.1, min_y: int = 0.1, center: bool = True,
                 run_at_build: bool = False, sun_icon: str = 'white-balance-sunny',
                 moon_icon: str = 'weather-night', main_color: str = 'Blue', **kwargs):

        super().__init__(**kwargs)

        self.builder_string = builder_string
        self.app_name = app_name

        app_data_path = os.getenv('APPDATA') + '/' + app_name
        self.appdata_path = app_data_path
        # self.appdata_path = app_name
        self.create_files(list_of_files)

        self.moon_icon = moon_icon
        self.sun_icon = sun_icon
        self.dark_mode_icon = StringProperty(sun_icon)
        self.isDarkMode()
        self.theme_cls.primary_palette = main_color

        screen = get_monitors()[0]
        self.width = screen.width
        self.height = screen.height

        self.screen_positions(screen_size, min_x, min_y, center)

        self.run_at_build = run_at_build

        self.run()

    def build(self):
        self.use_kivy_settings = False
        self.settings_cls = ContentPanel
        self.title = self.app_name
        Window.bind(on_request_close=lambda x: self.on_request_close())

        if self.run_at_build:
            self.Build()

        return Builder.load_string(self.custom_classes() + self.builder_string)

    def screen_positions(self, screen_size, min_x, min_y, center):

        if screen_size is None:
            x, y = 0.6, 0.6

        else:
            x, y = screen_size[0], screen_size[1]

        Window.size = (self.width * x, self.height * y)
        Window.minimum_height = self.height * min_y
        Window.minimum_width = self.width * min_x

        if center:
            Window.left = (self.width - (self.width * x)) / 2
            Window.top = (self.height - (self.height * y)) / 2

    def create_files(self, list_of_files):

        try:
            if not os.path.isdir(self.appdata_path):
                os.mkdir(self.appdata_path)

            if list_of_files:
                for file, value in list_of_files:
                    self.setFile(file + '.txt', value, check_if_file_exist=True)

        except Exception as e:
            return e

    def setFile(self, file, value, check_if_file_exist=False):

        path_to_create = f'{self.appdata_path}/{file}'

        try:
            if not check_if_file_exist or not os.path.isfile(path_to_create):
                with open(path_to_create, 'w') as f:
                    f.write(value)

        except Exception as e:
            print(e)
            return e

    def getFile(self, file, default=None, create_file_if_not_exist=False):

        path_of_file = f'{self.appdata_path}/{file}'

        try:
            with open(path_of_file, 'r') as f:
                return f.read()

        except FileNotFoundError:
            if create_file_if_not_exist:
                with open(path_of_file, 'w') as f:
                    f.write(default)
                    return default

        except Exception as e:
            print(e)
            return default

    def isDarkMode(self, filename='dark mode.txt'):
        try:
            with open(self.appdata_path + '/' + filename, 'r') as f:

                current_mode = f.read()
                self.theme_cls.theme_style = current_mode

                if f.read() == 'Dark':
                    self.dark_mode_icon = self.moon_icon

                else:
                    self.dark_mode_icon = self.sun_icon

                return current_mode == 'Dark'

        except FileNotFoundError:
            with open(self.appdata_path + '/' + filename, 'w') as f:
                default = darkdetect.theme()
                f.write(default)

                self.theme_cls.theme_style = default

                if default == 'Dark':
                    self.dark_mode_icon = self.moon_icon

                else:
                    self.dark_mode_icon = self.sun_icon

                return default == 'Dark'

    def setDarkMode(self, value=None, filename='dark mode.txt'):
        if value is None:
            value = darkdetect.theme()

        self.setFile(filename, value)

        if value == 'Dark':
            self.dark_mode_icon = self.moon_icon

        else:
            self.dark_mode_icon = self.sun_icon

        self.theme_cls.theme_style = value

    def reverseDarkMode(self, filename: str = 'dark mode.txt'):
        try:
            with open(self.appdata_path + '/' + filename, 'r') as f:

                current_mode = f.read()

                if current_mode == 'Dark':
                    self.setDarkMode('Light')
                    return 'Light'

                self.setDarkMode('Dark')
                return 'Dark'


        except FileNotFoundError:
            with open(self.appdata_path + '/' + filename, 'w') as f:
                default = darkdetect.theme()
                f.write(default)

                self.theme_cls.theme_style = default

                if default == 'Dark':
                    self.dark_mode_icon = self.moon_icon

                else:
                    self.dark_mode_icon = self.sun_icon

                return default

    @staticmethod
    def on_request_close(ignore_user_request: bool = False):
        return ignore_user_request

    @staticmethod
    def getToolbar(properties: list):
        Id, title, right_icons, left_icons = properties

        return f'''
    MDToolbar:
        id: {Id}
        pos_hint: {{"top": 1}}
        elevation: 10
        title: {title}
        right_action_items: {right_icons}
        left_action_items: {left_icons}'''

    @staticmethod
    def custom_classes():
        return '''
<Text@MDLabel>:
    halign: 'center'

<Input@MDTextField>:
    mode: "rectangle"
    text: ""
    size_hint_x: 0.5

<Check@MDCheckbox>:
    group: 'group'
    size_hint: None, None
    size: dp(48), dp(48)

<Btn@MDFillRoundFlatIconButton>:
    text: ""
'''