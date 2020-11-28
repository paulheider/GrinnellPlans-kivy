import time
import re

from kivy.app import App
from kivy.logger import Logger

from kivy.clock import Clock

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView

from kivy.graphics import Color

from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import OneLineListItem

from kivy.network.urlrequest import UrlRequest
import urllib
import simplejson as json

from html.parser import HTMLParser
from kivy.utils import escape_markup

########################################################################
##
########################################################################

planlove_fg = '0000ff'
link_fg = '0000ff'


class PlansHTMLParser( HTMLParser ):
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
                                              '[color=' ,
                                              planlove_fg ,
                                              ##cookie_jar.get( 'default_color_scheme' )[ 'planlove_fg' ] ,
                                              ']' ) )
            elif( class_type == 'onplan' ):
                self.plan_buffer = ''.join( ( self.plan_buffer ,
                                              '[color=' ,
                                              link_fg ,
                                              ##cookie_jar.get( 'default_color_scheme' )[ 'link_fg' ] ,
                                              ']' ) )
        elif( tag == 'pre' ):
            ## TODO:  Make mono font configurable
            mono_font = 'RobotoMono-Regular'
            self.plan_buffer = ''.join( ( self.plan_buffer ,
                                          '[font=' ,
                                          mono_font ,
                                          ']' ) )
        elif( tag == 'b' ):
            self.plan_buffer = ''.join( ( self.plan_buffer , '[b]' ) )
        elif( tag == 'hr' ):
            self.plan_buffer = ''.join( ( self.plan_buffer , '------------' ) )
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

# ## Hack until this bug is fixed to launch native Android browser
# ## https://github.com/kivy/python-for-android/issues/846
# ## http://python-for-android.readthedocs.io/en/latest/apis/#using-android
# ## TODO:  reorganize to preload to that the first URL isn't so slow
# def launch_webbrowser(url):
#     if platform == 'android':
#         from jnius import autoclass, cast
#         def open_url(url):
#             PythonActivity = autoclass('org.kivy.android.PythonActivity')
#             activity = PythonActivity.mActivity
#             Intent = autoclass('android.content.Intent')
#             Uri = autoclass('android.net.Uri')
#             browserIntent = Intent()
#             browserIntent.setAction(Intent.ACTION_VIEW)
#             browserIntent.setData(Uri.parse(url))
#             currentActivity = cast('android.app.Activity', activity)
#             currentActivity.startActivity(browserIntent)
            
#         # Web browser support.
#         class AndroidBrowser(object):
#             def open(self, url, new=0, autoraise=True):
#                 open_url(url)
#             def open_new(self, url):
#                 open_url(url)
#             def open_new_tab(self, url):
#                 open_url(url)
                
#         webbrowser.register('android', AndroidBrowser, None, -1)
        
#     webbrowser.open(url)
# ## END hack

        
class ScrollableLabel( ScrollView ):
    text = StringProperty( '' )


class ReadPlanScreen( Screen ):
    ## TODO:  add a button to flag plan for comment/later and see all flagged
    plans_parser = None
    
    # def on_enter( self ):
    #     LLOOGG( 'enter' )
    #     ## TODO - if the len( plan_chunks ) < 100 # double screen size
    #     ##          then just display a single chunk
    #     LLOOGG( 'Plan is {} chars long'.format( len( self.plan_body ) ) )
    #     if( len( self.plan_body ) < 1024 ):
    #         chunk_label = self.plan_content_template( self.plan_body )
    #         self.ids.plan_grid.add_widget( chunk_label )
    #         self.chunk_labels.append( chunk_label )
    #         return
    #     self.plan_chunks = self.plan_body.splitlines()
    #     LLOOGG( 'Plan is {} chunks long'.format( len( self.plan_chunks ) ) )
    #     ##        else
    #     ##          display the first 100 lines and then process the rest
    #     ##          of the chunks
    #     ## TODO - make bottom widget a loading gif
    #     ## TODO - don't freeze the screen while this is happening
    #     just_now = datetime.datetime.now()
    #     #safe_chunk_ends = [ 5 , len( self.plan_chunks ) ] ## TKZ self.find_safe_ends( plan_chunks , 0 , len( plan_chunks ) )
    #     safe_chunk_ends = self.find_safe_ends( self.plan_chunks , 0 , len( self.plan_chunks ) )
    #     chunk_end = safe_chunk_ends.pop( 0 )
    #     ## Add the first label
    #     self.finish_labels( 0 , [ chunk_end ] )
    #     Clock.schedule_once( partial( self.finish_labels ,
    #                                   chunk_end ,
    #                                   safe_chunk_ends ) , 0 )
    #     LLOOGG( 'Done with enter ReadPlan' )


    def chunkPlanBody( self , dt ):
        ## bails  at 6144
        new_chunk_size = len( self.ids.plan_body.text ) + 1024
        if( new_chunk_size < len( self.plans_parser.plan_buffer ) ):
            Logger.info( 'Read: {}'.format( new_chunk_size ) )
            self.ids.plan_body.text = self.plans_parser.plan_buffer[ 0:new_chunk_size ]
            Clock.schedule_once( self.chunkPlanBody , 2 )
        else:
            self.ids.plan_body.text = self.plans_parser.plan_buffer
            
    
    def cleanPlanBody( self , plan_body , this_encoding = None ):
        Logger.info( 'Read: cleaning plan' )
        self.plans_parser = PlansHTMLParser()
        if( this_encoding == None ):
            self.plans_parser.feed( plan_body )
        else:
            self.plans_parser.feed( plan_body.encode( this_encoding ) )
        if( len( self.plans_parser.plan_buffer ) < 5120 ):
            self.ids.plan_body.text = self.plans_parser.plan_buffer
        else:
            ## https://github.com/kivy/kivy/issues/2119
            Logger.info( 'Read: plan size is {} ({}). Chunking plan'.format( len( plan_body ) ,
                                                                             len( self.plans_parser.plan_buffer ) ) )
            self.ids.plan_body.text = self.plans_parser.plan_buffer[ 0:5120 ]
            ##Clock.schedule_once( self.chunkPlanBody )
            
                
        
    def readTask( self , username ):
        Logger.info( 'Read: opening plan for {}'.format( username ) )
        app = App.get_running_app()
        params = urllib.parse.urlencode( { 'username' : username } )
        headers = { 'Content-type' : 'application/x-www-form-urlencoded',
                    'Accept' : 'text/plain' ,
                    'Cookie' : 'PHPSESSID={}'.format( app.session_id ) }
        req = UrlRequest( app.api_urls[ 'read' ] ,
                          on_success = self.read_success ,
                          on_failure = self.read_failure ,
                          on_error = self.read_error ,
                          req_body  = params ,
                          req_headers = headers )

    def read_failure( self , req , resp ):
        Logger.info( 'Read: failed read' )
        Logger.info( 'Read: req = {}'.format( req ) )
        Logger.info( 'Read: resp = {}'.format( resp ) )

    def read_error( self , req , resp ):
        Logger.info( 'Read: error read' )
        Logger.info( 'Read: req = {}'.format( req ) )
        Logger.info( 'Read: resp = {}'.format( resp ) )

    def read_success( self , req , resp ):
        Logger.info( 'Read: successful read' )
        ## Responses
        ## - { "message" : "" ,
        ##     "success" : true ,
        ##     "plandata" : {
        ##       "username" : "bown" ,
        ##       "last_login" : "11\/24\/20, 2:01 AM",
        ##       "last_updated":"11\/26\/20, 8:10 PM",
        ##       "pseudo":"poet~lover~rebel~spy",
        ##       "partial":false,
        ##       "plan" : "..." } }
        resp_dict = json.loads( resp )
        if( resp_dict[ 'success' ] ):
            ##app = App.get_running_app()
            ##plan_name = self.cleanPlanName( json_response[ 'plandata' ][ 'pseudo' ] ,
            ##                                response.encoding )
            self.ids.toolbar.title = resp_dict[ 'plandata' ][ 'username' ]
            ##last_login = self.adjustClock( json_response[ 'plandata' ][ 'last_login' ] )
            ##last_updated = self.adjustClock( json_response[ 'plandata' ][ 'last_updated' ] )
            ## NEXT - TK - clean up plan to display
            ##self.cleanPlanBody( resp_dict[ 'plandata' ][ 'plan' ] ,
            ##                    None )
            ##self.ids.plan_body.text = resp_dict[ 'plandata' ][ 'plan' ]
            ##self.ids.plan_body.text = self.cleanPlanBody( resp_dict[ 'plandata' ][ 'plan' ] ,
            ##                                              None )
            self.cleanPlanBody( resp_dict[ 'plandata' ][ 'plan' ] ,
                                ## TODO - find encoding in response
                                None )
            ##plans_app.screens[ 3 ].ids.psuedo.text = plan_name
            ## and move the scrollview back to the top of the page
        else:
            Logger.error( 'Read: {}'.format( resp_dict[ 'message' ] ) )
            return
            
