from kivy.app import App
from kivy.logger import Logger

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer

from kivymd.uix.list import OneLineIconListItem

from kivy.properties import StringProperty, ObjectProperty, NumericProperty


class ItemDrawer( OneLineIconListItem ):
    icon = StringProperty()


class ContentNavigationDrawer( BoxLayout ):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class HamburgerMenu( MDNavigationDrawer ):
    pass

