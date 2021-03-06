import os

from kivy.app import App
from kivy.logger import Logger

from kivy.clock import Clock

from kivy.uix.screenmanager import Screen

from kivy.graphics import Color

from kivymd.uix.label import MDLabel
from kivymd.icon_definitions import md_icons

from kivy.network.urlrequest import UrlRequest
import urllib
import simplejson as json

########################################################################
##
########################################################################

## TODO:  add remember username/password button

class LoginScreen( Screen ):

    def version( self , *args ):
        app = App.get_running_app()
        return app.__version__

    def update_autofinger( self , json_list = None ):
        # global session
        # ## Updating the autofinger list happens automatically by a new
        # ## api call unless you provide a json_list of the autofinger
        # ## level entries when calling this function.
        # if( json_list == None ):
        #     json_list = get_json_list( session = session )
        #     if( json_list == None ):
        #         Logger.info( 'Error: autofinger list still empty after trying to load it.' )
        #         return()
        # ## Clear out the old global variable for update
        # global autofinger_list
        # autofinger_list = {}
        # ## Loop through the autofinger levels to update each level in turn
        # for level in json_list:
        #     level_number = level[ u'level' ]
        #     ##print( 'Level {}'.format( level_number ) )
        #     autofinger_list[ 'level_{}'.format( level_number ) ] = []
        #     ##autofinger_list[ 'level_{}'.format( level_number ) ] = ''
        #     level_string = 'level_{}'.format( level_number )
        #     for username in level[ u'usernames' ]:
        #         autofinger_list[ level_string ].append( username )
        #         ##print( "\t{}".format( username ) )
        pass

    def guestAuth( self , username , password ):
        pass


    def loadSavedSession( self ):
        # app = App.get_running_app()
        # if( os.path.exists( 'session.dat' ) ):
        #     with open('session.dat') as fp:
        #         tmp_cookies = 1##TK requests.utils.cookiejar_from_dict( pickle.load( fp ) )
        #         session = requests.Session()
        #         session.cookies.update( tmp_cookies )
        #         plans_app.screens[ 0 ].ids.username.text = app.cookie_jar.get( 'user_name' )[ 'username' ]
        #     return True
        return False

    
    def endSession( self ):
        ## TODO - add a button to the home screen to that you can do very early
        ##        in case the saved data is corrupted somehow? same for cookie_jar, defaults?
        app = App.get_running_app()
        if( os.path.exists( app.session_file ) ):
            os.remove( app.session_file )


    def logInTask( self , username , password ):
        Logger.info( 'Login: verifying username and password' )
        app = App.get_running_app()
        if( username == '' ):
            Logger.error( 'Login: username must not be empty.' )
            return
        elif( password == '' ):
            Logger.error( 'Login: password must not be empty.' )
            return
        app.username = username
        if( username == 'demo' ):
            #demo_password_file = os.path.join( 'demo' ,
            #                                   'password.txt' )
            #with open( demo_password_file , 'r' ) as fp:
            #    demo_password = fp.readline().strip()
            demo_password = 'helloworld'
            if( self.ids.password.text == demo_password ):
                Logger.info( 'Login: successfully restored demo session' )
                app.demo_session_flag = True
            else:
                Logger.info( 'Login: incorrect demo password' )
        params = urllib.parse.urlencode( { 'username' : username ,
                                           'password' : password } )
        headers = { 'Content-type' : 'application/x-www-form-urlencoded',
                    'Accept' : 'text/plain' }
        req = UrlRequest( app.api_urls[ 'login' ] ,
                          on_success = self.login_success ,
                          on_failure = self.login_failure ,
                          on_error = self.login_error ,
                          req_body  = params ,
                          req_headers = headers )
        ## TODO - start login animation

    def login_failure( self , req , resp ):
        Logger.info( 'Login: failed login' )
        Logger.info( 'Login: req = {}'.format( req ) )
        Logger.info( 'Login: resp = {}'.format( resp ) )

    def login_error( self , req , resp ):
        Logger.info( 'Login: error login' )
        Logger.info( 'Login: req = {}'.format( req ) )
        Logger.info( 'Login: resp = {}'.format( resp ) )

    def login_success( self , req , resp ):
        Logger.info( 'Login: valid return for login' )
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
        app = App.get_running_app()
        if( resp_dict[ 'success' ] ):
            Logger.info( 'Login: successful login' )
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
        elif( app.demo_session_flag ):
            Logger.info( 'Login: successful demo session' )
            app.autofinger_list = [ { "level" : "1" ,
                                      "usernames" : [ 'plans' , 'gspelvin' ] } ,
                                    { "level" : "2" ,
                                      "usernames" : [ 'newbie' ] } ,
                                    { "level" : "3" ,
                                      "usernames" : [ 'nemo' , 'kaplan' , 'harvey' ] } ]
            app.root.ids.screen_manager.current = "autofinger_list_screen"
        else:
            Logger.error( 'Login: {}'.format( resp_dict[ 'message' ] ) )
            return


    def restoreSessionTask( self , dt = None ):
        Logger.info( 'Login: restoring previous session' )
        app = App.get_running_app()
        app.pop()
        with open( app.session_file , 'r' ) as fp:
            app.username = fp.readline().strip()
            app.session_id = fp.readline().strip()
        params = urllib.parse.urlencode( { 'username' : app.username } )
        headers = { 'Content-type' : 'application/x-www-form-urlencoded',
                    'Accept' : 'text/plain' ,
                    'Cookie' : 'PHPSESSID={}'.format( app.session_id ) }
        req = UrlRequest( app.api_urls[ 'autofinger' ] ,
                          on_success = self.restore_session_success ,
                          on_failure = self.restore_session_failure ,
                          on_error = self.restore_session_error ,
                          req_body  = params ,
                          req_headers = headers )
        ## TODO - start login animation

    def restore_session_failure( self , req , resp ):
        Logger.info( 'Login: failed restore session' )
        Logger.info( 'Login: req = {}'.format( req ) )
        Logger.info( 'Login: resp = {}'.format( resp ) )

    def restore_session_error( self , req , resp ):
        Logger.info( 'Login: error restore session' )
        Logger.info( 'Login: req = {}'.format( req ) )
        Logger.info( 'Login: resp = {}'.format( resp ) )

    def restore_session_success( self , req , resp ):
        Logger.info( 'Login: successful restore session query' )
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
        app = App.get_running_app()
        if( resp_dict[ 'success' ] ):
            Logger.info( 'Login: successfully restored session' )
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
        elif( app.demo_session_flag ):
            app.root.ids.screen_manager.current = "autofinger_list_screen"
        else:
            Logger.error( 'Login: {}'.format( resp_dict[ 'message' ] ) )
            return


    def __init__(self , **kwargs ):
        super(LoginScreen, self).__init__(**kwargs)
        ## Setting color scheme
        #bg = cookie_jar.get( 'color_scheme' )[ 'background' ]
        with self.canvas.before:
            ## TODO - pull color from cookie_jar
            Color( 1 , 1 , 1 , 1 )
        Clock.schedule_once(self.init_ui, 0)
    
    def init_ui( self , dt = 0 ):
        app = App.get_running_app()
        app.session_file = os.path.join( app.user_data_dir ,
                                         'php_sess_id.txt' )
        if( os.path.exists( app.session_file ) ):
            Clock.schedule_once( self.restoreSessionTask , 0 )
