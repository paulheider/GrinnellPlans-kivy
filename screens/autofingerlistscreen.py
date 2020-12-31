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
        app.pop()
        app.root.ids.screen_manager.current = "read_plan_screen"
        app.root.ids.read_plan_screen.readTask( self.username )


class AutofingerListScreen( Screen ):

    def on_enter( self ):
        app = App.get_running_app()
        ## TODO - add loading animation
        app.root.ids.toolbar.title = 'Autofinger Lists'
        app.root.ids.toolbar.right_action_items = [[ "account-search" , lambda x: app.showSearch() ]]
        app.root.ids.toolbar.md_bg_color = [ 1 , .3 , .8 , .5 ]
        ##
        self.ids.level1_list.clear_widgets()
        self.ids.level2_list.clear_widgets()
        self.ids.level3_list.clear_widgets()
        for af_level in app.autofinger_list:
            if( af_level[ 'level' ] == '1' ):
                for username in af_level[ 'usernames' ]:
                    plan_item = PlanItem( text = '{}'.format( username ) )
                    plan_item.username = username
                    self.ids.level1_list.add_widget( plan_item )
            elif( af_level[ 'level' ] == '2' ):
                for username in af_level[ 'usernames' ]:
                    plan_item = PlanItem( text = '{}'.format( username ) )
                    plan_item.username = username
                    self.ids.level2_list.add_widget( plan_item )
            elif( af_level[ 'level' ] == '3' ):
                for username in af_level[ 'usernames' ]:
                    plan_item = PlanItem( text = '{}'.format( username ) )
                    plan_item.username = username
                    self.ids.level3_list.add_widget( plan_item )
        ##
        app.done_loading()
                

