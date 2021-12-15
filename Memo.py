from logging import error, raiseExceptions, root
from os import W_OK
import pathlib
#from typing_extensions import Concatenate
import PIL
import os
import threading
from kivy.clock import Clock, mainthread
from kivy.core import window
from kivy.core.window import Window
from typing import Text, List
from kivy.app import App
from kivy.lang import builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.app import Builder
from kivy.metrics import dp
from kivy.config import Config
from kivy.app import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty, ObjectProperty
from functools import partial
from plyer import filechooser
import time

#Window.maximize()
foto_list = []
image_list =[]


newpath = r'MemoFoto'
if not os.path.exists(newpath):
    os.makedirs(newpath)



class LandingPage(Screen):
    hint_text = StringProperty('Vul je naam hier in')


    def __init__(self, **kwargs):
        super(LandingPage, self).__init__(**kwargs)

        self.gamer_name = ''
        self.sec = 0
        self.on = 0

    def screen_transition(self, *args):
        self.manager.current = 'ImageChooser'
        if len(foto_list) == 25:
            self.popup_foto_selection()
        else:
            self.popup_foto_new_selection()
        
    def popup_foto_selection(self,*args):
        content = PopupFotoSelect()
        popupSelection = Popup(content=content,title='', separator_height=dp(0), auto_dismiss=False, size_hint=(.6, .5))
        content.ids.start_selection_bt.bind(on_release=popupSelection.dismiss,on_press=ImageChooserPage().file_chooser)
        popupSelection.open()
        
    def popup_foto_new_selection(self,*args):
        content = PopupFotoSelectionEmpltyList()
        popup_new = Popup(content=content,title='', separator_height=dp(0), auto_dismiss=True, size_hint=(.6, .5)) 
        content.ids.new_selection_bt.bind(on_release=popup_new.dismiss)
        popup_new.open()

    def startPlay(self):
        return self.ids.start_bt.bind(on_release=self.screen_transition)

    def start_bt(self):
        Octaaf = 'Octaaf De Bolle'
        Kwebbel = 'Kweeeeeebbel'
        self.gamer_name = self.ids.name_input.text
        gamer = self.gamer_name.upper()
  
        if len(gamer) <= 0:
            self.ids.name_input.hint_text = 'alstublieft uw naam in'
        elif gamer == 'DOURAYD':
            self.ids.up_button.text = f"Hallo {Octaaf}"
            self.manager.get_screen('ImageChooser').gamer_label = 'De Bolle: Ik Will pIpI DoeN'
            self.startPlay()
            self.ids.dridi.text = 'druk op de startknop'
            
        elif gamer == 'SHAHINEZE':
            self.ids.up_button.text = f'Hallo {Kwebbel}'
            self.manager.get_screen('ImageChooser').gamer_label = 'Kwebbel: jij pRaaT te Veeeel'
            self.startPlay()
            self.ids.dridi.text = 'druk op de startknop'
           
        else:
            self.ids.up_button.text = f'Hallo {gamer.title()}'
            PopupFotoSelect.hallo_gamer= f'Hallo {gamer.title()}'
            PopupFotoSelectionEmpltyList.gamer= f'Hallo {gamer.title()}'
            self.startPlay()
            self.ids.dridi.text = 'druk op de startknop'
            


####################################  Fotos selection      ############################

class PopupFotoSelectionEmpltyList(FloatLayout):
    gamer = StringProperty('')
    def __init__(self,**kwargs):
        super(PopupFotoSelectionEmpltyList,self).__init__(**kwargs)


class PopupFotoSelect(FloatLayout):
    hallo_gamer = StringProperty('')
    def __init__(self,**kwargs):
        super(PopupFotoSelect,self).__init__(**kwargs)      

class PopupFotoError(FloatLayout):
    pass
class PopupFotoInList(FloatLayout):
    pass
class PopupFullList(FloatLayout):
    pass
class PopupExitApp(FloatLayout):
    pass
class PopupInfoFotoInList(FloatLayout):
    pass


class ImageChooserPage(Screen):

    def __init__(self,**kwargs):
        super(ImageChooserPage, self).__init__(**kwargs)
        self.window_size()
        self.foto = ''
        self.still_to_select=25

    def window_size(self,dt=0,*args):
        if Window.width <270:
            for x in range (1,26):
                foto_id = f'foto_{x}'
                image_list.append(foto_id)
                self.ids[foto_id].size_hint= (.20,.15)



    def file_chooser(self,*args):
        filechooser.open_file(on_selection= self.selected_foto)
    def selected_foto(self, foto_path):
        content_instance = PopupFotoError()
        content = content_instance
        popup = Popup(content=content, title='', separator_height=dp(0), auto_dismiss=True, size_hint=(.6, .3))
        content.ids.dismiss_bt.bind(on_press=popup.dismiss)
        extention_list = ['.JPG', '.PNG', '.GIF', '.TIFF', '.WEBP', '.INDD', '.erer','.JPEG']
        try:
            extention_control = pathlib.Path(foto_path[0]).suffix
            if extention_control.upper() in extention_list:
                self.foto = foto_path[0]

            else:
                popup.open()       
        except (RuntimeError, TypeError, NameError, IndexError, PIL.UnidentifiedImageError):
            pass


    def update(self, *args):
        background_normal_list =[]
        print(len(foto_list))
        for x in range(1,25):
            x = self.ids[f'foto_{x}'].background_normal
            background_normal_list.append(x)
        if len(foto_list) == 4:
            self.full_list()
        elif len(foto_list) < 25 and self.foto not in foto_list and self.foto not in background_normal_list:
            foto_list.append(self.foto)
            self.ids[args[0]].background_normal = self.foto
        elif len(foto_list) < 25 and self.foto in foto_list and self.foto not in background_normal_list:
            self.ids[args[0]].background_normal = self.foto
        elif len(foto_list) < 25 and self.foto in foto_list and self.foto in background_normal_list:
            self.foto_in_list()



    def foto_in_list(self, *args):
        foto_in_list_instance = PopupFotoInList()
        popup_inlist = Popup(content=foto_in_list_instance, title='', separator_height=dp(0),
                             auto_dismiss=True, size_hint=(.6, .3))
        foto_in_list_instance.ids.foto_in_list.bind(on_press=popup_inlist.dismiss)
        popup_inlist.open()

    def full_list(self,*args):
        print('yes full')
        full_list_instance = PopupFullList()
        popup_full_list = Popup(content=full_list_instance, title='', separator_height=dp(0),
                                auto_dismiss=True, size_hint=(.8, .4))
        full_list_instance.ids.start_game_bt.bind(on_press=popup_full_list.dismiss,
                                                  on_release=self.screen_transition)
        popup_full_list.open()

    def foto_pass(self,*args):
        pass









    def screen_transition(self, *args):
        self.manager.current = 'game'



    '''def exit_app(self):
        exit_app = PopupExitApp()
        exit_app_content = exit_app
        popup_exit_app = Popup(content=exit_app_content, title='', separator_height=dp(0),
                               auto_dismiss=True, size_hint=(.6, .4))
        exit_app_content.ids.no_exit_bt.bind(on_press=popup_exit_app.dismiss)
        popup_exit_app.open()'''


##################################################################################################

################################### GAME PAGE ###################################################

class GamePage(StackLayout):

    def __init__(self, **kwargs):
        super(GamePage, self).__init__(**kwargs)
        self.counter = 0
        self.on = 0
        for i in range(50):
            self.btn = Button(text=str(i), size_hint=(.1, .2))
            buttoncallback = partial(self.pressed, self.btn.text)
            self.btn.bind(on_press=buttoncallback)

            self.add_widget(self.btn)

    def pressed(self, *args):
        self.parent.parent.parent.on_start_timer()

        '''print(args[0])
        if self.on == 0:
            scroll.on_start_timer()
            self.on += 1
        else:
            scroll.on_pause_timer()
            self.on -= 1'''


class Scroll(Screen):
    if_timer = False

    def __init__(self, **kwargs):
        super(Scroll, self).__init__(**kwargs)
        self.pattern = '{0:02d}:{1:02d}:{2:02d}'
        self.timer = [0, 0, 0]
        self.timerString = ''
        self.Clock_run = ''

    def Label_updater(self, time_string):
        self.ids.time_.text = time_string
        print(self.ids.time_.text)

    def timer_func(self, *args):
        self.timer[2] += 1
        if self.timer[2] >= 60:
            self.timer[2] = 0
            self.timer[1] += 1
        if self.timer[1] >= 60:
            self.timer[0] += 1
            self.timer[1] = 0
        self.timeString = self.pattern.format(self.timer[0], self.timer[1], self.timer[2])
        self.Label_updater(self.timeString)

    def screen_transition(self, *args):
        self.manager.current = 'landing'

    def on_start_timer(self):

        if self.if_timer is False:
            Clock.schedule_interval(self.timer_func, 1)
            self.if_timer = True

    def on_pause_timer(self):
        Clock.unschedule(self.timer_func)
        self.if_timer = False

    def stop_play(self):

        self.on_pause_timer()
        self.timeString = self.pattern.format(0, 0, 0)
        self.Label_updater(self.timeString)
        self.pattern = '{0:02d}:{1:02d}:{2:02d}'
        self.timer = [0, 0, 0]
        # self.manager.get_screen('landing').ids.dridi.text='Daaaaag'# or root.manager.get_screen....
        self.manager.get_screen('landing').reset_landing()
        return self.ids.stop_game.bind(on_release=self.screen_transition)


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)


class MemoApp(App):
    def build(self):
        sm = WindowManager(transition=FadeTransition())
        sm.add_widget(LandingPage(name='landing'))
        sm.add_widget(Scroll(name='game'))
        sm.add_widget(ImageChooserPage(name='ImageChooser'))
        return sm




if __name__ == '__main__':

    MemoApp().run()
