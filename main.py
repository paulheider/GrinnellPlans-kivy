from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf8')

## Allow labels to have background colors
#import LabelB

import inspect

import time
import datetime
import requests
#import urllib
#import base64
#import urllib2

import re

##from html2rest import html2rest
##import StringIO
from HTMLParser import HTMLParser
#from bs4 import BeautifulSoup

import webbrowser

import kivy

kivy.require('1.9.0')

## TODO:  integrate a config file
##from kivy.config import Config
from kivy.logger import Logger

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.factory import Factory

from kivy.properties import ObjectProperty

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from kivy.utils import escape_markup

from kivy.storage.jsonstore import JsonStore
from kivy.storage.dictstore import DictStore

def this_line():
    callerframerecord = inspect.stack()[1]
    ## 0 represents this line
    ## 1 represents line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    return info.lineno

## We use a very strict regex pattern because of how we treat
## planlove as a special form of URL to be parsed
## read.php?searchname=gspelvin
planlove_re = re.compile( "^read\.php\?searchname=([a-zA-Z0-9]+)$" )
autofinger_level_re = re.compile( "^level_[0-9]$" )

plan_name_parser = HTMLParser()

class PlansHTMLParser(HTMLParser):
    plan_buffer = ''
    
    def handle_starttag(self, tag, attrs):
        ## TODO:  add support for <hr>, <pre>
        ## https://www.grinnellplans.com/documents/faq.html#htmltags
        ## https://github.com/kivy/kivy/tree/master/kivy/data/fonts
        if( tag == 'a' ):
            href_content = None
            class_type = None
            for attr in attrs:
                if( attr[ 0 ] == 'href' ):
                    href_content = attr[ 1 ]
                elif( attr[ 0 ] == 'class' ):
                    class_type = attr[ 1 ]
            self.plan_buffer = ''.join( ( self.plan_buffer ,
                                          '[ref=' ,
                                          href_content ,
                                          ']' ) )
            if( class_type == 'planlove' ):
                ##print( '{} -> {}'.format( href_content ,
                ##                          planlove_re.findall(href_content)))
                ##planlove_target = planlove_re.findall( href_content )[ 0 ]
                self.plan_buffer = ''.join( ( self.plan_buffer ,
                                              '[color=0000ff]' ) )
            elif( class_type == 'onplan' ):
                self.plan_buffer = ''.join( ( self.plan_buffer ,
                                              '[color=00ff00]' ) )
        elif( tag == 'pre' ):
            ## TODO:  Make mono font configurable
            mono_font = 'RobotoMono-Regular'
            self.plan_buffer = ''.join( ( self.plan_buffer ,
                                          '[font=' ,
                                          mono_font ,
                                          ']' ) )
        elif( tag == 'b' ):
            self.plan_buffer = ''.join( ( self.plan_buffer , '[b]' ) )
        elif( tag == 'i' ):
            self.plan_buffer = ''.join( ( self.plan_buffer , '[i]' ) )
        elif( tag == 'u' ):
            self.plan_buffer = ''.join( ( self.plan_buffer , '[u]' ) )
        elif( tag == 'strike' ):
            self.plan_buffer = ''.join( ( self.plan_buffer , '[s]' ) )

        
    def handle_endtag(self, tag):
        if( tag == 'a' ):
            ## TODO: deal with nested tags
            self.plan_buffer = ''.join( ( self.plan_buffer ,
                                          '[/color][/ref]' ) )
        elif( tag == 'pre' ):
            self.plan_buffer = ''.join( ( self.plan_buffer , '[/font]' ) )
        elif( tag == 'b' ):
            self.plan_buffer = ''.join( ( self.plan_buffer , '[/b]' ) )
        elif( tag == 'i' ):
            self.plan_buffer = ''.join( ( self.plan_buffer , '[/i]' ) )
        elif( tag == 'u' ):
            self.plan_buffer = ''.join( ( self.plan_buffer , '[/u]' ) )
        elif( tag == 'strike' ):
            self.plan_buffer = ''.join( ( self.plan_buffer , '[/s]' ) )
        
    def handle_data(self, data):
        self.plan_buffer = ''.join( ( self.plan_buffer ,
                                      escape_markup( data ) ) )

from kivy.utils import platform

## Hack until this bug is fixed to launch native Android browser
## https://github.com/kivy/python-for-android/issues/846
## http://python-for-android.readthedocs.io/en/latest/apis/#using-android
## TODO:  reorganize to preload to that the first URL isn't so slow
def launch_webbrowser(url):
    if platform == 'android':
        from jnius import autoclass, cast
        def open_url(url):
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            browserIntent = Intent()
            browserIntent.setAction(Intent.ACTION_VIEW)
            browserIntent.setData(Uri.parse(url))
            currentActivity = cast('android.app.Activity', activity)
            currentActivity.startActivity(browserIntent)
            
        # Web browser support.
        class AndroidBrowser(object):
            def open(self, url, new=0, autoraise=True):
                open_url(url)
            def open_new(self, url):
                open_url(url)
            def open_new_tab(self, url):
                open_url(url)
                
        webbrowser.register('android', AndroidBrowser, None, -1)
        
    webbrowser.open(url)
## END hack
        
cookie_jar = DictStore( 'cookies.dat' )
session = None

autofinger_list = {}

## TODO:  add remember username/password button
def LLOOGG( message ):
    ##plans_app.screens[ 1 ].ids[ 'loading_page_logs' ].text = message
    Logger.info( message )


class PopupBox(Popup):
    pop_up_text = ObjectProperty()
    
    def update_pop_up_text(self, p_message):
        self.pop_up_text.text = p_message


class LoginScreen( Screen ):

    def show_popup( self , message ):
        LLOOGG( "{} - {}".format( this_line() ,
                                  message ) )
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text( message )
        self.pop_up.open()

    def update_autofinger( self , json_list = None ):
        ## Updating the autofinger list happens automatically by a new
        ## api call unless you provide a json_list of the autofinger
        ## level entries when calling this function.
        if( json_list == None ):
            try:
                username = cookie_jar.get( 'user_name' )[ 'username' ]
            except Exception as e:
                st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
                LLOOGG( 'Error:  Unable to extract username from cookie jar - {1}\n'.format( st , e ) )
            try:
                url = 'https://www.grinnellplans.com/api/1/index.php?task=autofingerlist'
                response = session.post( url ,
                                         data = { 'username': username } )
                json_response = None
                if( response.status_code == 200 ):
                    json_response = response.json()
                    response.close()
                    json_list = json_response[ 'autofingerList' ]
            except Exception as e:
                st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
                LLOOGG( 'Error:  {1}\n'.format( st , e ) )
        ## Clear out the old global variable for update
        global autofinger_list
        autofinger_list = {}
        ## Loop through the autofinger levels to update each level in turn
        for level in json_list:
            level_number = level[ u'level' ]
            ##print( 'Level {}'.format( level_number ) )
            autofinger_list[ 'level_{}'.format( level_number ) ] = []
            ##autofinger_list[ 'level_{}'.format( level_number ) ] = ''
            level_string = 'level_{}'.format( level_number )
            for username in level[ u'usernames' ]:
                autofinger_list[ level_string ].append( username )
                ##print( "\t{}".format( username ) )

    
    def guestAuth( self , username , password ):
        pass##print( '{} -> {}'.format( username , password ) )

    
    def logInTask( self , username , password ):
        global session
        self.show_popup( 'Logging in...' )
        plans_app.current = 'landing_page'
        LLOOGG( "{} - {}h {}w".format( this_line() ,
                                       plans_app.height ,
                                       plans_app.width ) )
        try:
            if( username == '' ):
                LLOOGG( 'Username must not be empty.' )
            elif( password == '' ):
                LLOOGG( 'Password must not be empty.' )
            else:
                ##LLOOGG( "{} - {} {}".format( this_line() ,
                ##                             username ,
                ##                             password ) )
                login_url = 'https://www.grinnellplans.com/api/1/index.php?task=login'
                LLOOGG( "{} - {}".format( this_line() , login_url ) )
                session = requests.Session()
                LLOOGG( "{} - {}".format( this_line() , 'session created' ) )
                response = session.post( login_url ,
                                         data = { 'username': username ,
                                                  'password': password } )
                LLOOGG( "{} - {}".format( this_line() , 'response generated' ) )
                jar = response.cookies
                if( response.status_code == 200 ):
                    cookie_jar.put( 'user_name' ,
                                    username = username )
                    ##cookie_jar.put( 'user_pass' ,
                    ##                passwd = password )
                    json_response = response.json()
                    print( '{} - {}'.format( this_line() , json_response ) )
                    self.update_autofinger( json_response[ 'autofingerList' ] )
                    response.close()
                    LLOOGG( 'Logged in.  Checking plan...' )
                    ##plans_app.current = 'landing_page'
                    self.pop_up.dismiss()
                    LLOOGG( "{} - popup dismissed".format( this_line() ) )
                else:
                    LLOOGG( 'Failed to log in:  {}'.format( response.status_code ) )
        except Exception as e:
            st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
            LLOOGG( 'Error:  {1}\n'.format( st , e ) )
    
    
    def __init__(self , **kwargs ):
        super(LoginScreen, self).__init__(**kwargs)


class LoadingPage( Screen ):

    def on_enter( self ):
        pass

    
    def __init__(self , **kwargs ):
        super(LoadingPage, self).__init__(**kwargs)


class LandingPage( Screen ):
    ## TODO:  random buttons for each person on your autoread list
    ## https://kivy.org/docs/api-kivy.uix.floatlayout.html#module-kivy.uix.floatlayout
    ## TODO:  add refresh button or pull at top to refresh

    def show_popup( self , message ):
        if( message == None ):
            message = 'Waiting for PlanGodot'
        LLOOGG( "{} - {}".format( this_line() ,
                                  message ) )
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text( message )
        self.pop_up.open()
    

    def load_autofinger_levels( self ):
        global autofinger_list
        button_width = 0.9 * plans_app.width / 3
        button_height = plans_app.height * 0.5
        self.show_popup( 'Loading autofinger levels...' )
        ##
        for level_name in plans_app.screens[ 2 ].ids:
            level_matches = autofinger_level_re.findall( level_name )
            if( len( level_matches ) == 0 ):
                ## Ignore widgets that aren't named "level_[0-9]"
                continue
            ##print( "\t{}".format( level_name ) )
            plans_app.screens[ 2 ].ids[ level_name ].clear_widgets()
            ## TODO:  reformat
            pretty_level_name = level_name[:1].upper() + \
                                level_name[1:].replace( '_' , ' ' )
            level_lbl = Label( id = '{}_lbl'.format( level_name ) ,
                               size_y = button_height ,
                               text = pretty_level_name )
            plans_app.screens[ 2 ].ids[ level_name ].add_widget( level_lbl )
            ## TODO:  is this line really necessary?
            plans_app.screens[ 2 ].ids[ level_name ].bind( minimum_height = plans_app.screens[ 2 ].ids[ level_name ].setter( 'height' ) )
            if( autofinger_list.has_key( level_name ) ):
                for username in autofinger_list[ level_name ] :
                    ##print( "\t\t{}".format( username ) )
                    finger_btn = Button( text = username ,
                                         size_x = button_width ,
                                         size_y = button_height ,
                                         size_hint_y = None )
                    ##TODO:  bind readTask to this button
                    finger_btn.bind( on_press = plans_app.screens[ 3 ].readFromLevels )
                    plans_app.screens[ 2 ].ids[ level_name ].add_widget( finger_btn )
        self.pop_up.dismiss()
        
        
    def on_enter( self ):
        plans_app.screens[ 0 ].update_autofinger()
        self.load_autofinger_levels()
        

    def __init__(self , **kwargs ):
        super(LandingPage, self).__init__(**kwargs)


class ReadPlan( Screen ):
    ## TODO:  add a button to flag plan for comment/later and see all flagged
    def show_popup( self , message ):
        if( message == None ):
            message = 'Waiting for PlanGodot'
        LLOOGG( "{} - {}".format( this_line() ,
                                  message ) )
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text( message )
        self.pop_up.open()
    
    
    def on_enter( self ):
        #with open( '/tmp/plan_body.html' , 'r' ) as f:
        #    plan_body = self.cleanPlanBody( f.read() )
        #f.closed
        ##print( "{} - {}".format( this_line() , plan_body[ 0:250 ] ) )
        LLOOGG( "{} - Original length = {}".format( this_line() ,
        #                                               plans_app.screens[ 3 ].ids.plan.bcolor ,
                                                    plans_app.screens[ 3 ].ids.plan.texture_size ) )
        ## TODO:  Readjusting label size to match text size
        ##   - https://blog.kivy.org/2014/07/wrapping-text-in-kivys-label/
        #plans_app.screens[ 3 ].ids.plan.text = plan_body
        ##plans_app.screens[ 3 ].ids.plan.text_size = ( 780 , 800 )
        ##plans_app.screens[ 3 ].ids.plan.texture_size[ 1 ] )
        ##plans_app.screens[ 3 ].ids.plan.texture_update()
        ##plans_app.screens[ 3 ].ids.plan.height = plans_app.screens[ 3 ].ids.plan.texture_size[ 1 ]
        ##plans_app.screens[ 3 ].ids.plan.size = plans_app.screens[ 3 ].ids.plan.texture_size
        ##plans_app.screens[ 3 ].ids.plan.size = plans_app.screens[ 3 ].ids.plan.texture_size
        ##text_size: self.width, None
        ##height: self.texture_size[1]
        #LLOOGG( "{} - Plan length = {} vs. {}".format( this_line() ,
        #                                               len( plan_body ) ,
        #                                               plans_app.screens[ 3 ].ids.plan.texture_size ) )
        #

    def guestAuth( self , username ):
        print( '{} -|'.format( username ) )
    
    
    def cleanPlanBody( self , plan_body , this_encoding = None ):
        print( '{} - Cleaning plan body'.format( this_line() ) )
        plans_parser = PlansHTMLParser()
        if( this_encoding == None ):
            plans_parser.feed( plan_body )
        else:
            plans_parser.feed( plan_body.encode( this_encoding ) )
        return plans_parser.plan_buffer
        ## TODO: maybe replace beatufil soup with HTMLParser
        ## https://docs.python.org/2/library/htmlparser.html
        #if( this_encoding == None ):
        #    soup = BeautifulSoup( plan_body ,
        #                          'html.parser' )
        #else:
        #    soup = BeautifulSoup( plan_body.decode( this_encoding ) ,
        #                          'html.parser' )
        #return soup.get_text()
        if( this_encoding == None ):
            return plan_body
        ## Default
        return plan_body.encode( this_encoding )
    
    
    def cleanPlanName( self , plan_name , this_encoding ):
        ##return html_parser.unescape( plan_name.encode( this_encoding ) )
        return plan_name_parser.unescape( plan_name )

    
    ## TODO:  convert times to local timezone
    ## TODO:  add local vs. UTC vs. other timezone display options
    def adjustClock( self , timestamp ):
        return timestamp
    

    def readFromHomeButton( self ):
        username = plans_app.screens[ 0 ].ids.username.text
        if( username != '' ):
            self.show_popup( 'Loading plan...' )
            self.readTask( username )
            self.pop_up.dismiss()
    
            
    def readFromFingerButton( self ):
        username = plans_app.screens[ 3 ].ids.finger.text
        if( username != '' ):
            self.show_popup( 'Loading plan...' )
            self.readTask( username )
            self.pop_up.dismiss()

    
    def readFromLevels( self , button_instance ):
        username = button_instance.text
        if( username != '' ):
            self.show_popup( 'Loading plan...' )
            self.readTask( username )
            self.pop_up.dismiss()

    
    def readFromRef( self , ref_string ):
        planlove_matches = planlove_re.findall( ref_string )
        if( len( planlove_matches ) == 0 ):
            LLOOGG( 'readFromRef:  {} - generic url = {}'.format( this_line() , ref_string ) )
            launch_webbrowser( ref_string )
        else:
            username = planlove_matches[ 0 ]
            LLOOGG( 'readFromRef:  {} - {} from {}'.format( this_line() , username , ref_string ) )
            self.show_popup( 'Loading plan...' )
            self.readTask( username )
            self.pop_up.dismiss()
    
    
    def readTask( self , username ):
        global session
        ## TODO:  scroll back to top of page for new plan
        plans_app.current = 'read_plan'
        try:
            url = 'https://www.grinnellplans.com/api/1/index.php?task=read'
            response = session.post( url ,
                                     data = { 'username': username } )
            json_response = None
            if( response.status_code == 200 ):
                json_response = response.json()
                ##print( 'Encoding = {}'.format( response.encoding ) )
                ##plan_body = response.text.encode( response.encoding )
                #### We don't actually need the grab the username because
                #### it was passed to the original function
                ##username = json_response[ 'plandata' ][ 'username' ]
                plan_body = self.cleanPlanBody( json_response[ 'plandata' ][ 'plan' ] ,
                                                response.encoding )
                plan_name = self.cleanPlanName( json_response[ 'plandata' ][ 'pseudo' ] ,
                                                response.encoding )
                last_login = self.adjustClock( json_response[ 'plandata' ][ 'last_login' ] )
                last_updated = self.adjustClock( json_response[ 'plandata' ][ 'last_updated' ] )
                ##LLOOGG( '{}'.format( this_line() ) )
                ##with open( '/tmp/plan_body.html' , 'w' ) as f:
                ##    f.write( plan_body )
                ##f.closed
                response.close()
                plans_app.screens[ 3 ].ids.username.text = username
                plans_app.screens[ 3 ].ids.psuedo.text = plan_name
                plans_app.screens[ 3 ].ids.last_login.text = last_login
                plans_app.screens[ 3 ].ids.last_updated.text = last_updated
                ##plans_app.screens[ 3 ].ids.plan.text = plan_body[ 0:250 ]##'asdf'
                plans_app.screens[ 3 ].ids.plan.text = plan_body
                ## If we got here from clicking the read button, then empty out the data
                plans_app.screens[ 3 ].ids.finger.text = ''
        except Exception as e:
            st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
            LLOOGG( 'Error:  {1}\n'.format( st , e ) )

    def __init__(self , **kwargs ):
        super(ReadPlan, self).__init__(**kwargs)


class EditPlan( Screen ):
    pass

class ScreenManagement( ScreenManager ):
    pass
            

plans_app = Builder.load_file( "main.kv" )

class GrinnellPlansApp(App):
    
    def build(self):
        ## plans_app.screen_names[ 0 ]
        ##print( '{}'.format( plans_app.screens[ 0 ].ids.password.text ) )
        print( 'Screens:  {}'.format( plans_app.screens ) )
        if( cookie_jar.exists( 'user_name' ) ):
            ##cookie_jar.exists( 'user_pass' ) ):
            ## TODO:  make this a robust look-up rather than hard-coded index
            plans_app.screens[ 0 ].ids.username.text = cookie_jar.get( 'user_name' )[ 'username' ]
            ##plans_app.screens[ 0 ].ids.password.text = cookie_jar.get( 'user_pass' )[ 'passwd' ]
        plans_app.current = 'login'
        ##plans_app.current = 'landing_page'
        ##plans_app.current = 'loading_page'
        ##plans_app.current = 'read_plan'
        return plans_app
    
if __name__ == '__main__':
    GrinnellPlansApp().run()
    
