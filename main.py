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

from kivy.core.window import Window
from kivy.utils import platform
if( platform == 'linux' ):
    Window.size = ( 600 , 350 )

## TODO:  integrate a config file
##from kivy.config import Config

# from kivy.clock import Clock

# from kivy.graphics import Color

# from kivy.storage.dictstore import DictStore

## We use a very strict regex pattern because of how we treat
## planlove as a special form of URL to be parsed
## read.php?searchname=gspelvin
planlove_re = re.compile( "^read\.php\?searchname=([a-zA-Z0-9]+)$" )
autofinger_level_re = re.compile( "^level_[0-9]$" )

## TODO - add a if( debug mode flag ): here?
##        or maybe make this a toggle on the home screen
##        to use an alternate backend
base_url = 'https://www.grinnellplans.com'

api_urls = { 'autofinger' : '{}/api/1/index.php?task={}'.format( base_url , 'autofingerlist' ) ,
             'read'       : '{}/api/1/index.php?task={}'.format( base_url , 'read' ) ,
             'login'      : '{}/api/1/index.php?task={}'.format( base_url , 'login' ) }


autofinger_list = {}

now_time = datetime.datetime.now()
now_stamp = now_time.strftime( "%Y-%m-%d %H:%M:%S" )
now_filesafe = now_time.strftime( "%Y-%m-%d_%H%M%S" )
log_file = 'grinnell_plans_{}.txt'.format( now_filesafe )

########################################################################
##
########################################################################

class GrinnellPlansApp(App):
    __version__ = '20.48.1'
    
    cookie_jar = None
    session = None

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
    
    def on_start( self ):
        ##self.cookie_jar = DictStore( 'cookies.dat' )
        self.initilize_global_dirs()
        self.loadColorScheme()
        
    def build(self):
        ## The kv file handles layout
        pass


if __name__ == '__main__':
    GrinnellPlansApp().run()
    
