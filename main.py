import sys
# Fix path on iOS, otherwise can't find relative imports
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))

import os
import re
import time
import datetime

import kivy
kivy.require( '2.0.0' )

from kivy.app import App
from kivy.logger import Logger

from kivymd.app import MDApp

from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import OneLineIconListItem

from kivymd.uix.button import MDFlatButton
from kivy.uix.popup import Popup
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.utils import platform
if( platform == 'linux' ):
    ##Window.size = ( 600 , 350 )
    Window.size = ( 350 , 600 )

from kivy.properties import StringProperty, ObjectProperty, NumericProperty

from kivy.network.urlrequest import UrlRequest
import urllib
import simplejson as json
import webbrowser

## TODO:  integrate a config file
##from kivy.config import Config

from kivy.clock import Clock

# from kivy.graphics import Color

# from kivy.storage.dictstore import DictStore

## We use a very strict regex pattern because of how we treat
## planlove as a special form of URL to be parsed
## read.php?searchname=gspelvin
planlove_re = re.compile( "^read\.php\?searchname=([a-zA-Z0-9]+)$" )
autofinger_level_re = re.compile( "^level_[0-9]$" )

now_time = datetime.datetime.now()
now_stamp = now_time.strftime( "%Y-%m-%d %H:%M:%S" )
now_filesafe = now_time.strftime( "%Y-%m-%d_%H%M%S" )
log_file = 'grinnell_plans_{}.txt'.format( now_filesafe )

########################################################################
##
########################################################################

# class Content(BoxLayout):
#     def __init__(self, **kwargs):
#         super( BoxLayout , self).__init__(**kwargs)

about_string = """A Kivy app for interfacing with GrinnellPlans

[b]Contributions or Bugs?[/b]\n[i][ref=https://github.com/paulheider/GrinnellPlans-kivy/issues]https://github.com/paulheider/GrinnellPlans-kivy/issues[/ref][/i]

[b]Lead Dev:[/b]  Paul M. Heider

[b]Version:[/b]  {}

Copyright © 2017-2021 Paul M. Heider
"""

class FingerDialog( BoxLayout ):
    pass


class GrinnellPlansApp( MDApp ):
    __version__ = '20.53.6'

    notch_height = NumericProperty( 0 ) # dp(25) if on new iphones
    navdrawer_height = NumericProperty( 0 )
    
    ## TODO - add a if( debug mode flag ): here?
    ##        or maybe make this a toggle on the home screen
    ##        to use an alternate backend
    base_url = 'https://www.grinnellplans.com'
    api_urls = { 'autofinger' : '{}/api/1/index.php?task={}'.format( base_url , 'autofingerlist' ) ,
                 'read'       : '{}/api/1/index.php?task={}'.format( base_url , 'read' ) ,
                 'login'      : '{}/api/1/index.php?task={}'.format( base_url , 'login' ) }
    
    cookie_jar = None
    session_id = None
    session_file = None

    username = ""
    demo_session_flag = False
    autofinger_list = {}
    flagged_plans = set()

    progress_bar = ObjectProperty()
    loading_popup = ObjectProperty()
    loading_flag = False

    about_popup = ObjectProperty()
    about_content = ObjectProperty()
    
    def mainMenu( self ):
        Logger.info( 'Toolbar: main menu' )
        self.root.ids.screen_manager.current = "flagged_plan_screen"
        
    
    def rememberPlan( self ):
        Logger.info( 'Read: toggling read-later flag on plan' )
        open_plan = self.root.ids.toolbar.title
        flagged_plan_file = os.path.join( App.get_running_app().user_data_dir ,
                                          'flagged_plans_{}.txt'.format( self.username ) )
        if( open_plan in self.flagged_plans ):
            self.root.ids.toolbar.right_action_items = [ [ "flag" , lambda x: app.rememberPlan() ] ,
                                                         [ "view-column" , lambda x: app.showAutofingerList() ] ,
                                                         [ "account-search" , lambda x: app.showSearch() ] ]
            self.flagged_plans.remove( open_plan )
            with open( flagged_plan_file , 'w' ) as fp:
                for plan_name in self.flagged_plans:
                    fp.write( '{}\n'.format( plan_name ) )
        else:
            self.root.ids.toolbar.right_action_items = [ [ "flag-outline" , lambda x: app.rememberPlan() ] ,
                                                         [ "view-column" , lambda x: app.showAutofingerList() ] ,
                                                         [ "account-search" , lambda x: app.showSearch() ] ]
            self.flagged_plans.add( open_plan )
            with open( flagged_plan_file , 'w' ) as fp:
                for plan_name in self.flagged_plans:
                    fp.write( '{}\n'.format( plan_name ) )


    def showAutofingerList( self ):
        if( self.root.ids.screen_manager.current == "autofinger_list_screen" ):
            1 ## NOOP - TODO - maybe change this to fully refresh the list?
        else:
            self.pop()
            self.root.ids.screen_manager.current = "autofinger_list_screen"
            params = urllib.parse.urlencode( { 'username' : self.username } )
            headers = { 'Content-type' : 'application/x-www-form-urlencoded',
                        'Accept' : 'text/plain' ,
                        'Cookie' : 'PHPSESSID={}'.format( self.session_id ) }
            req = UrlRequest( self.api_urls[ 'autofinger' ] ,
                              on_success = self.root.ids.login_screen.restore_session_success ,
                              on_failure = self.root.ids.login_screen.restore_session_failure ,
                              on_error = self.root.ids.login_screen.restore_session_error ,
                              req_body  = params ,
                              req_headers = headers )

        
    def showSearch( self ):
        Logger.info( 'Toolbar: search for plan' )
        self.root.ids.screen_manager.current = "search_screen"

        
    def readFingerDialog( self , *kwargs ):
        Logger.info( 'Dialog: reading plan' )
        with open( os.path.join( App.get_running_app().user_data_dir ,
                                 'log.txt' ) , 'w' ) as fp:
            ##    fp.write( '{}\n'.format( dialog_ref ) )
            fp.write( '{}\n'.format( App.get_running_app().dialog.ids.finger_username ) )
            fp.write( 'fin\n' )
        ##print( '{}\n'.format( self.dialog.ids ) )
        
            
    def closeFingerDialog( self , dialog_ref ):
        Logger.info( 'Dialog: closing' )
        print( '{}'.format( dialog_ref ) )
        print( '{}'.format( dialog_ref.ids ) )
        if( self.dialog is not None ):
            self.dialog.dismiss()


    def log_out( self ):
        self.root.ids.login_screen.endSession()
        self.root.ids.screen_manager.current = "login_screen"

            
    def initilize_global_dirs(self):
        log_dir = os.path.join( App.get_running_app().user_data_dir , 'log' )
        if( not os.path.exists( log_dir ) ):
            os.makedirs( log_dir )

    def loadDefaultColorScheme( self ):
        ##if( not cookie_jar.exists( 'default_color_scheme' ) ):
        # self.cookie_jar.put( 'default_color_scheme' ,
        #                 background = [ 1 , 1 , 1 , 1 ] ,
        #                 ## rgb(149,165,166)
        #                 button_bg = [ .58431372549019607843 , .64705882352941176470 , .65098039215686274509 , 1 ] ,
        #                 button_fg = [ 1 , 1 , 1 , 1 ] ,
        #                 label_bg = [ 0.5 , 0.5 , 0.5 , 1 ] ,
        #                 label_fg = [ 0 , 0 , 0 , 1 ] ,
        #                 content_fg = [ 0 , 0 , 0 , 1 ] ,
        #                 planlove_fg = '0000ff' ,
        #                 link_fg = '0000ff' )
        pass
    
    
    def loadColorScheme( self ):
        self.loadDefaultColorScheme()
        # self.cookie_jar.put( 'color_scheme' ,
        #                 background = self.cookie_jar.get( 'default_color_scheme' )[ 'background' ] ,
        #                 button_bg = self.cookie_jar.get( 'default_color_scheme' )[ 'button_bg' ] ,
        #                 button_fg = self.cookie_jar.get( 'default_color_scheme' )[ 'button_fg' ] ,
        #                 label_bg = self.cookie_jar.get( 'default_color_scheme' )[ 'label_bg' ] ,
        #                 label_fg = self.cookie_jar.get( 'default_color_scheme' )[ 'label_fg' ] ,
        #                 content_fg = self.cookie_jar.get( 'default_color_scheme' )[ 'content_fg' ] ,
        #                 planlove_fg = self.cookie_jar.get( 'default_color_scheme' )[ 'planlove_fg' ] ,
        #                 link_fg = self.cookie_jar.get( 'default_color_scheme' )[ 'link_fg' ] )
    
    def pop( self ):
        self.loading_flag = True
        self.progress_bar.value = 1
        self.loading_popup.open()

    def done_loading( self ):
        self.loading_flag = False
        self.loading_popup.dismiss()

    def next(self, dt):
        if( self.progress_bar.value >= 100 ):
            self.progress_bar.value = 1
        else:
            self.progress_bar.value += 5
        return self.loading_flag

    def puopen(self, instance):
        Clock.schedule_interval( self.next , 1/25 )

        
    def refLink( self , src , link , *kwargs ):
        Logger.info( 'About: ref clicked' )
        webbrowser.open( link )


    def on_start( self ):
        ##self.cookie_jar = DictStore( 'cookies.dat' )
        self.initilize_global_dirs()
        self.loadColorScheme()
        ## Setting up the loading progress bar
        ## TODO - set to indeterminate
        self.progress_bar = MDProgressBar()
        # TODO - change pop colors to match underlying screen theme
        self.loading_popup = Popup(
            title = 'Loading',
            title_align = 'center' ,
            content = self.progress_bar,
            auto_dismiss = False,
            size_hint = ( 0.5 , None )
        )
        self.loading_popup.bind( on_open = self.puopen )
        ##
        self.about_content = MDLabel( text = about_string.format( self.__version__ ) ,
                                      markup = True ,
                                      padding = [ 10 , 10 ] ,
                                      theme_text_color = "Custom" ,
                                      text_color = [ 1 , 1 , 1 , 1 ] ,
                                      on_ref_press = self.refLink )
        self.about_popup = Popup(
            title = 'Grinnell Plans',
            title_align = 'center' ,
            content = self.about_content ,
            size_hint = ( 0.8 , 0.8 )
        )
        self.about_popup.bind( on_press = self.about_popup.dismiss )
        ##
        if( platform == 'android' ):
            Logger.info( 'Verifying run-time permissions' )
            try:
                from android.permissions import request_permissions, check_permission, Permission
            except ImportError:
                Logger.exception( 'Error importing android.permissions' )
            Logger.info( 'Imported permission modules' )
            request_response = request_permissions( [ Permission.INTERNET ] )
            if( check_permission( Permission.INTERNET ) ):
                Logger.info( 'Verified permissions:  {}'.format( Permission.INTERNET ) )
            else:
                Logger.info( 'Rejected permissions:  {}'.format( Permission.INTERNET ) )
        else:
            Logger.info( 'No additional permissions needed' )
        flagged_plan_file = os.path.join( App.get_running_app().user_data_dir ,
                                          'flagged_plans_{}.txt'.format( self.username ) )
        if( os.path.exists( flagged_plan_file ) ):
            with open( flagged_plan_file , 'r' ) as fp:
                self.flagged_plans.add( fp.readline().strip() )
        self.navdrawer_height = self.root.ids.toolbar.height

        
    def build(self):
        ## The kv file handles layout
        pass


if __name__ == '__main__':
    GrinnellPlansApp().run()
    
