from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
# from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

# from kivy.lang import Builder

from kivy.uix.label import Label
from kivy.uix.widget import Widget
# from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager

# from kivy.config import Config
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle

from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

import os

# Globals:
FILE_IMAGES = {'.txt': 'txt.png', '.mp3': 'mp3.png', '.log': 'txt.png'}
W_HEIGHT = Window.height // 10  # height of folder and file widgets
P_W_DISTANCE = 0  # distance between PageWidget and Folder/File Widget
TOP_BAR_HEIGHT = W_HEIGHT/ 2
PATH_LABEL_HEIGHT = W_HEIGHT / 2
Manager = ScreenManager()


def if_dir(path):
    try:
        os.listdir(path)
        return True
    except:
        return False


def give_previous_dir(name):
    if name == '/':
        return '/'
    else:
        return name[:name.rindex('/')]


def show_dirs_and_files(directory, show_secrets=False):
    files = []
    dirs = []
    try:

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
    except:
        return [], []

    return sorted(files), sorted(dirs)


def build_page(files, dirs, dir_name=''):
    # Idk how, but it works
    root = GridLayout(cols=1, size_hint_y=None)
    root.bind(minimum_height=root.setter('height'))

    if root.height < W_HEIGHT * (len(dirs) + len(files)):
        root.size = (Window.width, W_HEIGHT * (len(dirs) + len(files)))

    top = root.height

    f = GoBackFolderWidget(pos=(P_W_DISTANCE, top - W_HEIGHT), height=W_HEIGHT, width=root.width)
    root.add_widget(f)
    top -= W_HEIGHT
    f.full_name = give_previous_dir(dir_name)
    f.main_dir = dir_name
    f.ids.folder_label.text = '...'

    for el in dirs:
        i = dirs.index(el) + 1

        f = FolderWidget(pos=(P_W_DISTANCE, top - i * W_HEIGHT), height=W_HEIGHT, width=root.width)
        f.ids.folder_label.text = el
        f.full_name = dir_name + '/' + el

        root.add_widget(f)

        del f

    top -= len(dirs) * W_HEIGHT

    for el in files:
        i = files.index(el) + 1
        f = FileWidget(pos=(P_W_DISTANCE, top - i * W_HEIGHT), height=W_HEIGHT, width=root.width)

        try:
            f.ids.file_label.text = el
        except ValueError:
            f.ids.file_label = 'Name_error'

        try:
            c_name = el[el.index('.'):]
        except ValueError:
            c_name = 'Unknown'

        if c_name in FILE_IMAGES.items():
            img_source = FILE_IMAGES.get(c_name)
        else:
            img_source = 'unknown.png'

        f.ids.file_image.source = 'sources/images/' + img_source

        root.add_widget(f)
        del f, c_name, img_source

    s = ScrollView(height=Window.height - PATH_LABEL_HEIGHT - TOP_BAR_HEIGHT, width=Window.width)
    s.add_widget(root)

    n, q = Widget(size_hint=(None, None), size=s.size), Widget(size_hint=(None, None), size=Window.size)
    n.add_widget(s)
    q.add_widget(n)

    p_l = BigClass(pos=(P_W_DISTANCE, q.height - TOP_BAR_HEIGHT - PATH_LABEL_HEIGHT), height=PATH_LABEL_HEIGHT,
                   width=q.width)
    p_l.ids.l1.text = dir_name

    with p_l.canvas:
        Color(0.86, 0.86, 0.86, 0.25)
        Rectangle(pos=p_l.pos, size=p_l.size)

    q.add_widget(p_l)

    bar = TopBar(pos= (P_W_DISTANCE, q.height -TOP_BAR_HEIGHT), height= TOP_BAR_HEIGHT, width= q.width)
    with bar.canvas:
        Color(0.86, 0.86, 0.86, 0.25)
        Rectangle(pos=bar.pos, size=bar.size)

    q.add_widget(bar)

    screen = Screen()
    screen.name = dir_name
    screen.add_widget(q)

    return screen


# just for testing PageWidget class
class PageApp(App):
    folder = '/'

    def build(self):
        f, d = show_dirs_and_files(self.folder)
        page = build_page(f, d, dir_name=self.folder)
        Manager.add_widget(page)
        del f, d, page
        return Manager


class FolderWidget(Widget):
    # If text not changed for directory name it will cause an error:
    text = "<Name_error>"
    full_name = '/'

    def switch_to(self):
        f, d = show_dirs_and_files(self.full_name)
        page = build_page(f, d, self.full_name)
        Manager.add_widget(page)
        Manager.remove_widget(Manager.get_screen(self.full_name[:self.full_name.rindex('/')]))
        Manager.transition.direction = 'left'
        Manager.current = self.full_name
        del f, d, page


class FileWidget(Widget):
    # If text not changed for file name it will cause an error:
    file_name = "<Name_error>"


class GoBackFolderWidget(FolderWidget):
    full_name = '/'
    main_dir = '/'

    def switch_to(self):
        global Manager
        try:
            f, d = show_dirs_and_files(self.full_name)
            page = build_page(f, d, self.full_name)
            Manager.add_widget(page)
            Manager.transition.direction = 'right'
            Manager.current = self.full_name
            Manager.remove_widget(Manager.get_screen(self.main_dir))
            del f, d, page
        except:
            pass


class BigClass(Widget):
    pass


class TopBar(Widget):
    w_distance = NumericProperty()
    h_d = NumericProperty()
    w_d = NumericProperty()


if __name__ == '__main__':
    main = PageApp()
    main.folder = '/home/hoksly/Github'
    main.run()
