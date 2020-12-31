import os

from kivy.app import App
from kivy.logger import Logger

from kivy.clock import Clock

from kivy.uix.screenmanager import Screen

from kivy.graphics import Color

from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.icon_definitions import md_icons

from kivy.network.urlrequest import UrlRequest
import urllib
import simplejson as json

########################################################################
##
########################################################################

class SearchScreen( Screen ):


    def login_failure( self , req , resp ):
        Logger.info( 'Login: failed login' )
        Logger.info( 'Login: req = {}'.format( req ) )
        Logger.info( 'Login: resp = {}'.format( resp ) )

    def login_error( self , req , resp ):
        Logger.info( 'Login: error login' )
        Logger.info( 'Login: req = {}'.format( req ) )
        Logger.info( 'Login: resp = {}'.format( resp ) )

    def login_success( self , req , resp ):
        Logger.info( 'Login: successful login' )
        ## Valid responses:
        ## - { "message" : "Invalid username or password." ,
        ##     "success" : false }
        ## - { "message" : "" ,
        ##     "success" : true ,
        ##     "autofingerList" : [
        ##        { "level" : "1" ,
        ##          "usernames" : [ ... ] } ,
        ##        { "level" : "2" ,
        ##          "usernames" : [ ... ] } ,
        ##        { "level" : "3" ,
        ##          "usernames" : [ ... ] } ] }
        resp_dict = json.loads( resp )
        if( resp_dict[ 'success' ] ):
            app = App.get_running_app()
            cookie_str = req.resp_headers[ 'Set-Cookie' ]
            cookies = cookie_str.split( ';' )
            for cookie in cookies:
                cookie = cookie.strip()
                try:
                    key , val = cookie.split( '=' )
                except ValueError:
                    key = cookie
                if( key == 'PHPSESSID' ):
                    app.session_id = val
                    with open( app.session_file , 'w' ) as fp:
                        fp.write( '{}\n{}'.format( app.username ,
                                                   app.session_id ) )
                    break
            app.autofinger_list = resp_dict[ 'autofingerList' ]
            app.root.ids.screen_manager.current = "autofinger_list_screen"
        else:
            Logger.error( 'Login: {}'.format( resp_dict[ 'message' ] ) )
            return

    def searchUsername( self ):
        Logger.info( 'Search: fingering user' )
        app = App.get_running_app()
        app.pop()
        username = app.root.ids.search_screen.ids.username.text
        app.root.ids.read_plan_screen.readTask( username )
        app.root.ids.screen_manager.current = "read_plan_screen"
        

    def on_enter( self ):
        app = App.get_running_app()
        ##
        app.root.ids.toolbar.title = 'Search'
        ## right_action_items: [ [ "view-column" , lambda x: app.showAutofingerList() ] ]
        app.root.ids.toolbar.md_bg_color = [ 1 , 0.8 , .3 , .5 ]
        ##
        app.root.ids.search_screen.ids.username.text = ""
        

    def __init__(self , **kwargs ):
        super(SearchScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color( 1 , 1 , 1 , 1 )
