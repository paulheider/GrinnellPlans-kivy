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

# from kivy.storage.dictstore import DictStore

########################################################################
##
########################################################################

## TODO:  add remember username/password button

# def get_json_list( session , username = None , testing = False ):
#     if( username == None ):
#         app = App.get_running_app()
#         try:
#             username = app.cookie_jar.get( 'user_name' )[ 'username' ]
#         except Exception as e:
#             st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
#             Logger.info( 'Error:  Unable to extract username from cookie jar - {1}\n'.format( st , e ) )
#             return None
#     ##
#     try:
#         url = api_urls[ 'autofinger' ]
#         response = session.post( url ,
#                                  data = { 'username' : username } )
#         if( testing ):
#             Logger.info( 'Staging: Status Code = {}'.format( response.status_code ) )
#         if( response.status_code == 200 ):
#             json_response = response.json()
#             response.close()
#             json_message = json_response[ 'message' ]
#             json_success = json_response[ 'success' ]
#             if( testing ):
#                 Logger.info( 'Staging: JSON Response = {}'.format( json_response ) )
#                 Logger.info( 'Staging: JSON Success = {}'.format( json_success ) )
#                 Logger.info( 'Staging: JSON Message = {}'.format( json_message ) )
#             if( json_success ):
#                 json_list = json_response[ 'autofingerList' ]
#                 return json_list
#             else:
#                 return None
#         else:
#             ## Don't forget to close the response for good housekeeping
#             response.close()
#             return None
#     except Exception as e:
#         st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
#         Logger.info( 'Error: {1}'.format( st , e ) )
#     return None

# def session_login( session , username , password , testing = False ):
#     app = App.get_running_app()
#     try:
#         if( username == '' ):
#             Logger.info( 'Error: Username must not be empty.' )
#             return( False , session )
#         elif( password == '' ):
#             Logger.info( 'Error: Password must not be empty.' )
#             return( False , session )
#         Logger.info( "Staging: {} - {}".format( this_line() , api_urls[ 'login' ] ) )
#         session = requests.Session()
#         Logger.info( "Staging: {} - {}".format( this_line() , 'session created' ) )
#         response = session.post( api_urls[ 'login' ] ,
#                                  data = { 'username' : username ,
#                                           'password' : password } )
#         Logger.info( "Staging: {} - {}".format( this_line() , 'response generated' ) )
#         if( testing ):
#             Logger.info( '{}'.format( response ) )
#             Logger.info( 'Staging: Status Code = {}'.format( response.status_code ) )
#             Logger.info( 'Headers = {}'.format( response.headers ) )
#             Logger.info( 'Text = {}'.format( response.text ) )
#         if( response.status_code == requests.codes.ok ):
#             ##
#             json_response = response.json()
#             response.close()
#             json_success = json_response[ 'success' ]
#             json_message = json_response[ 'message' ]
#             if( testing ):
#                 Logger.info( 'Staging: JSON Success = {}'.format( json_success ) )
#                 Logger.info( 'Staging: JSON Message = {}'.format( json_message ) )
#             if( json_success ):
#                 if( testing ):
#                     print( '{} - {}'.format( this_line() , json_response ) )
#                 ## TODO - remember the SessionID cookie?
#                 #jar = response.cookies
#                 ##Logger.info( '{}'.format( jar[ 'Cookie PHPSESSID' ] ) )
#                 if( testing ):
#                     Logger.info( '{}'.format( jar ) )
#                 ## TODO - if remember username is checked, then...
#                 app.cookie_jar.put( 'user_name' ,
#                                 username = username )
#                 ## TODO - if remember password is checked, then...
#                 ##cookie_jar.put( 'user_pass' ,
#                 ##                passwd = password )
#                 Logger.info( 'Staging: {} - Logged in.  Checking plan...'.format( this_line() ) )
#                 with open('session.dat', 'w') as fp:
#                     ## TK
#                     1##pickle.dump( requests.utils.dict_from_cookiejar( session.cookies ) ,
#                     ##             fp )
#                 return( True , session )
#             else:
#                 Logger.info( 'Warning: ' +
#                         'Unsuccessful login. Returning to login page:  {}'.format( json_message ) )
#                 return( False , session )
#         else:
#             Logger.info( 'Error: Failed to log in (Status Code = {})'.format( response.status_code ) )
#             return( False , session )
#     except Exception as e:
#         st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
#         Logger.info( 'Error:  {1}\n'.format( st , e ) )
#     return( False , session )


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
        # app = App.get_running_app()
        # ## TODO - add a button to the home screen to that you can do very early
        # ##        in case the saved data is corrupted somehow? same for cookie_jar, defaults?
        # global session
        # session = None
        # if( os.path.exists( 'session.dat' ) ):
        #     os.remove( 'session.dat' )
        # if( applcookie_jar.exists( 'user_name' ) ):
        #     ## TODO:  make this a robust look-up rather than hard-coded index
        #     plans_app.screens[ 0 ].ids.username.text = app.cookie_jar.get( 'user_name' )[ 'username' ]
        # plans_app.current = 'login'
        pass
    
    def logInTask( self , username , password ):
        Logger.info( 'Login: verifying username and password' )
        app = App.get_running_app()
        if( username == '' ):
            Logger.error( 'Login: username must not be empty.' )
            return
        elif( password == '' ):
            Logger.error( 'Login: password must not be empty.' )
            return
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
                if( key == 'PHPSESSIONID' ):
                    app.session_id = val
                    break
            app.autofinger_list = resp_dict[ 'autofingerList' ]
            ##app.root.ids.screen_manager.current = "lobby_screen"
        else:
            Logger.error( 'Login: {}'.format( resp[ 'message' ] ) )
            return
        #         Logger.info( "Staging: {} - {}".format( this_line() , 'response generated' ) )
        #         if( testing ):
        #             Logger.info( '{}'.format( response ) )
        #             Logger.info( 'Staging: Status Code = {}'.format( response.status_code ) )
        #             Logger.info( 'Headers = {}'.format( response.headers ) )
        #             Logger.info( 'Text = {}'.format( response.text ) )
        #         if( response.status_code == requests.codes.ok ):
        #             ##
        #             json_response = response.json()
        #             response.close()
        #             json_success = json_response[ 'success' ]
        #             json_message = json_response[ 'message' ]
        #             if( testing ):
        #                 Logger.info( 'Staging: JSON Success = {}'.format( json_success ) )
        #                 Logger.info( 'Staging: JSON Message = {}'.format( json_message ) )
        #             if( json_success ):
        #                 if( testing ):
        #                     print( '{} - {}'.format( this_line() , json_response ) )
        #                 ## TODO - remember the SessionID cookie?
        #                 #jar = response.cookies
        #                 ##Logger.info( '{}'.format( jar[ 'Cookie PHPSESSID' ] ) )
        #                 if( testing ):
        #                     Logger.info( '{}'.format( jar ) )
        #                 ## TODO - if remember username is checked, then...
        #                 app.cookie_jar.put( 'user_name' ,
        #                                 username = username )
        #                 ## TODO - if remember password is checked, then...
        #                 ##cookie_jar.put( 'user_pass' ,
        #                 ##                passwd = password )
        #                 Logger.info( 'Staging: {} - Logged in.  Checking plan...'.format( this_line() ) )
        #                 with open('session.dat', 'w') as fp:
        #                     ## TK
        #                     1##pickle.dump( requests.utils.dict_from_cookiejar( session.cookies ) ,
        #                     ##             fp )
        #                 return( True , session )
        #             else:
        #                 Logger.info( 'Warning: ' +
        #                         'Unsuccessful login. Returning to login page:  {}'.format( json_message ) )
        #                 return( False , session )
        #         else:
        #             Logger.info( 'Error: Failed to log in (Status Code = {})'.format( response.status_code ) )
        #             return( False , session )
        #     except Exception as e:
        #         st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
        #         Logger.info( 'Error:  {1}\n'.format( st , e ) )
        # try:
        #     ( successful_login , session ) = \
        #       session_login( session , username , password )
        #     ##
        #     if( successful_login ):
        #         ## TODO - move this extra call to get_json_list back inside
        #         ##        the call to session_login
        #         json_list = get_json_list( session = session ,
        #                                    username = username )
        #         if( json_list == None ):
        #             Logger.info( 'Warning: I had trouble loading the autofinger list' )
        #             plans_app.current = 'login_page'
        #             self.endSession()
        #             return()
        #         else:
        #             self.update_autofinger( json_list )
        #     else:
        #         self.endSession()
        #         return()
        # except Exception as e:
        #     st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
        #     Logger.info( 'Error:  {1}\n'.format( st , e ) )


    def __init__(self , **kwargs ):
        super(LoginScreen, self).__init__(**kwargs)
        ## Setting color scheme
        #bg = cookie_jar.get( 'color_scheme' )[ 'background' ]
        with self.canvas.before:
            ## TODO - pull color from cookie_jar
            Color( 1 , 1 , 1 , 1 )
        Clock.schedule_once(self.init_ui, 0)
    
    def init_ui( self , dt = 0 ):
        # app = App.get_running_app()
        # ## Setting color scheme
        # for this_child in self.children:
        #     for widget in this_child.walk( restrict = False ):
        #         if( type( widget ) == type( Button() ) ):
        #             widget.background_color = app.cookie_jar.get( 'color_scheme' )[ 'button_bg' ]
        #             widget.color = app.cookie_jar.get( 'color_scheme' )[ 'button_fg' ]
        #         elif( type( widget ) == type( Label() ) ):
        #             widget.background_color = app.cookie_jar.get( 'color_scheme' )[ 'label_bg' ]
        #             widget.color = app.cookie_jar.get( 'color_scheme' )[ 'label_fg' ]
        pass
