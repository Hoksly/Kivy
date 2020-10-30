from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
# from kivy.uix.floatlayout import FloatLayout

# from kivy.lang import Builder

from kivy.uix.label import Label
from kivy.uix.widget import Widget
# from kivy.uix.image import Image
# from kivy.uix.button import Button

# from kivy.config import Config
# from kivy.properties import ObjectProperty
from kivy.core.window import Window

import os

# Config.set('graphics', 'resizable', True)

# Globals:
W_HEIGHT = 100  # height of folder and file widgets
P_W_DISTANCE = 0  # distance between PageWidget and Folder/File Widget


def if_dir(path):
    try:
        os.listdir(path)
        return True
    except:
        return False


def show_dirs_and_files(directory, show_secrets=False):
    files = []
    dirs = []

    if show_secrets:
        for el in os.listdir(directory):
            if if_dir(directory + '/' + el):
                dirs.append(el)
            else:
                files.append(el)

    else:
        for el in os.listdir(directory):
            if el[0] != '.':
                if if_dir(directory + '/' + el):
                    dirs.append(el)
                else:
                    files.append(el)

    return files, dirs


# In future it will be main application
'''
class TestApp(App):
    def build(self):
        bl = BoxLayout(orientation='vertical')

        files, dirs = show_dirs_and_files('./')

        for el in dirs:
            bl.add_widget(Label(text=el))

        for el in files:
            label = (Label(text=el, size_hint=(1.0, 1.0), halign='left', valign='middle'))
            label.bind(size=label.setter('text_size'))
            bl.add_widget(label)

        l = len(dirs) + len(files)
        while l < 12:
            bl.add_widget(Widget())
            l += 1

        return bl

'''


def build_page(dirs):
    root = PageWidget()
    root.size = Window.size
    top = root.height
    for el in dirs:
        i = dirs.index(el) + 1
        root.add_widget(FolderWidget(pos=(P_W_DISTANCE, top - i * W_HEIGHT), height=W_HEIGHT, width=root.width))

    # d = FolderWidget(pos = (0, 0), height = 100, width = root.width)
    # d.txt  = "Hello World"
    # root.add_widget(d)

    return root


# just for testing PageWidget class
class PageApp(App):
    def build(self):
        # Here is a bug: after 6th it doesn't add anything, so max size for dirs/files in 1 die now is 6
        c = build_page([1, 2, 3, 4, 5, 6, 7, 8])
        return c


class FolderWidget(Widget):
    # If text not changed for directory name it will cause an error:
    txt = "<Name_Error>"


class PageWidget(Widget):
    pass


# Another class-tester
'''
class Test2App(App):

    def build(self):
        return Label()
'''

if __name__ == '__main__':
    PageApp().run()
