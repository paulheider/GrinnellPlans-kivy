from kivy.app import App
from kivy.logger import Logger

from kivy.clock import Clock

from kivy.uix.screenmanager import Screen

from kivy.graphics import Color

from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import OneLineListItem

from kivy.network.urlrequest import UrlRequest

class PlanItem( OneLineListItem ):
    username = ""

    def on_release( self ):
        Logger.info( 'Autofinger: reading {}'.format( self.username ) )
        app = App.get_running_app()
        app.root.ids.screen_manager.current = "read_plan_screen"
        app.root.ids.read_plan_screen.readTask( self.username )
        app.flagged_plans.remove( self.username )

class FlaggedPlanScreen( Screen ):

    def on_enter( self ):
        app = App.get_running_app()
        ## TODO - add loading animation
        app.root.ids.toolbar.title = 'Flagged Plans'
        app.root.ids.toolbar.right_action_items = [ [ "view-column" , lambda x: app.showAutofingerList() ] ,
                                                    [ "account-search" , lambda x: app.showSearch() ] ]
        app.root.ids.toolbar.md_bg_color = [ 1 , .3 , .8 , .5 ]
        ##
        self.ids.plan_list.clear_widgets()
        for username in app.flagged_plans:
            plan_item = PlanItem( text = '{}'.format( username ) )
            plan_item.username = username
            self.ids.plan_list.add_widget( plan_item )

