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
import urllib
import simplejson as json

########################################################################
##
########################################################################
# plan_name_parser = None ##HTMLParser()

# class PlansHTMLParser():##HTMLParser):
#     plan_buffer = ''
    
#     def handle_starttag(self, tag, attrs):
#         ## TODO:  add support for <hr>, <pre>
#         ## https://www.grinnellplans.com/documents/faq.html#htmltags
#         ## https://github.com/kivy/kivy/tree/master/kivy/data/fonts
#         if( tag == 'a' ):
#             href_content = None
#             class_type = None
#             for attr in attrs:
#                 if( attr[ 0 ] == 'href' ):
#                     href_content = attr[ 1 ]
#                 elif( attr[ 0 ] == 'class' ):
#                     class_type = attr[ 1 ]
#             self.plan_buffer = ''.join( ( self.plan_buffer ,
#                                           '[ref=' ,
#                                           href_content ,
#                                           ']' ) )
#             if( class_type == 'planlove' ):
#                 ##print( '{} -> {}'.format( href_content ,
#                 ##                          planlove_re.findall(href_content)))
#                 ##planlove_target = planlove_re.findall( href_content )[ 0 ]
#                 self.plan_buffer = ''.join( ( self.plan_buffer ,
#                                               '[color=' ,
#                                               cookie_jar.get( 'default_color_scheme' )[ 'planlove_fg' ] ,
#                                               ']' ) )
#             elif( class_type == 'onplan' ):
#                 self.plan_buffer = ''.join( ( self.plan_buffer ,
#                                               '[color=' ,
#                                               cookie_jar.get( 'default_color_scheme' )[ 'link_fg' ] ,
#                                               ']' ) )
#         elif( tag == 'pre' ):
#             ## TODO:  Make mono font configurable
#             mono_font = 'RobotoMono-Regular'
#             self.plan_buffer = ''.join( ( self.plan_buffer ,
#                                           '[font=' ,
#                                           mono_font ,
#                                           ']' ) )
#         elif( tag == 'b' ):
#             self.plan_buffer = ''.join( ( self.plan_buffer , '[b]' ) )
#         elif( tag == 'i' ):
#             self.plan_buffer = ''.join( ( self.plan_buffer , '[i]' ) )
#         elif( tag == 'u' ):
#             self.plan_buffer = ''.join( ( self.plan_buffer , '[u]' ) )
#         elif( tag == 'strike' ):
#             self.plan_buffer = ''.join( ( self.plan_buffer , '[s]' ) )

        
#     def handle_endtag(self, tag):
#         if( tag == 'a' ):
#             ## TODO: deal with nested tags
#             self.plan_buffer = ''.join( ( self.plan_buffer ,
#                                           '[/color][/ref]' ) )
#         elif( tag == 'pre' ):
#             self.plan_buffer = ''.join( ( self.plan_buffer , '[/font]' ) )
#         elif( tag == 'b' ):
#             self.plan_buffer = ''.join( ( self.plan_buffer , '[/b]' ) )
#         elif( tag == 'i' ):
#             self.plan_buffer = ''.join( ( self.plan_buffer , '[/i]' ) )
#         elif( tag == 'u' ):
#             self.plan_buffer = ''.join( ( self.plan_buffer , '[/u]' ) )
#         elif( tag == 'strike' ):
#             self.plan_buffer = ''.join( ( self.plan_buffer , '[/s]' ) )
        
#     def handle_data(self, data):
#         self.plan_buffer = ''.join( ( self.plan_buffer ,
#                                       escape_markup( data ) ) )

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

class ReadPlanScreen( Screen ):
    # ## TODO:  add a button to flag plan for comment/later and see all flagged

    # plan_body = ''
    # plan_chunks = []
    # chunk_labels = []
    # tag_start_stack = []
    # tag_end_stack = []
    
    # def on_pre_enter( self ):
    #     LLOOGG( 'pre-enter' )
        
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
                        

    # def finish_labels( self , chunk_start , safe_chunk_ends , *args ):
    #     ##
    #     for chunk_end in safe_chunk_ends:
    #         chunk = '\n'.join( self.plan_chunks[ chunk_start : chunk_end ] )
    #         if( chunk == "" ):
    #             chunk = " "
    #         chunk_prefix = ''
    #         for tag in reversed( self.tag_start_stack ):
    #             chunk_prefix  = '{}{}'.format( tag ,
    #                                            chunk_prefix )
    #         self.extract_open_tags( chunk )
    #         chunk_suffix = ''
    #         for tag in reversed( self.tag_end_stack ):
    #             chunk_suffix = '{}{}'.format( chunk_suffix ,
    #                                           tag )
    #         chunk = '{}{}{}'.format( chunk_prefix ,
    #                                  chunk ,
    #                                  chunk_suffix )
    #         chunk_label = self.plan_content_template( chunk )
    #         self.ids.plan_grid.add_widget( chunk_label )
    #         self.chunk_labels.append( chunk_label )
            
    
    # def guestAuth( self , username ):
    #     ##print( '{} -|'.format( username ) )
    #     pass
    
    
    # def cleanPlanBody( self , plan_body , this_encoding = None ):
    #     ##print( '{} - Cleaning plan body'.format( this_line() ) )
    #     plans_parser = PlansHTMLParser()
    #     if( this_encoding == None ):
    #         plans_parser.feed( plan_body )
    #     else:
    #         plans_parser.feed( plan_body.encode( this_encoding ) )
    #     return plans_parser.plan_buffer
    #     ## TODO: maybe replace beatufil soup with HTMLParser
    #     ## https://docs.python.org/2/library/htmlparser.html
    #     #if( this_encoding == None ):
    #     #    soup = BeautifulSoup( plan_body ,
    #     #                          'html.parser' )
    #     #else:
    #     #    soup = BeautifulSoup( plan_body.decode( this_encoding ) ,
    #     #                          'html.parser' )
    #     #return soup.get_text()
    #     if( this_encoding == None ):
    #         return plan_body
    #     ## Default
    #     return plan_body.encode( this_encoding )

    # def readFromHomeButton( self ):
    #     username = plans_app.screens[ 0 ].ids.username.text
    #     if( username != '' ):
    #         self.readTask( username )
    
            
    # def readFromFingerButton( self ):
    #     username = plans_app.screens[ 3 ].ids.finger.text
    #     if( username != '' ):
    #         self.readTask( username )

    
    # def readFromLevels( self , button_instance ):
    #     username = button_instance.text
    #     if( username != '' ):
    #         self.readTask( username )

    
    # def readFromRef( self , instance , ref_string ):
    #     planlove_matches = planlove_re.findall( ref_string )
    #     if( len( planlove_matches ) == 0 ):
    #         LLOOGG( 'readFromRef:  {} - generic url = {}'.format( this_line() , ref_string ) )
    #         launch_webbrowser( ref_string )
    #     else:
    #         username = planlove_matches[ 0 ]
    #         LLOOGG( 'readFromRef:  {} - {} from {}'.format( this_line() , username , ref_string ) )
    #         self.readTask( username )

    # def extract_open_tags( self , text ):
    #     s = re.split( '(\[.*?\])' , text )
    #     s = [ x for x in s if x != '' ]
    #     for chunk in s:
    #         if( chunk.startswith( '[/' ) and
    #             chunk.endswith( ']' ) ):
    #             self.tag_start_stack.pop()
    #             self.tag_end_stack.pop()
    #         elif( chunk.startswith( '[' ) and
    #             chunk.endswith( ']' ) ):
    #             self.tag_start_stack.append( chunk )
    #             if( chunk.startswith( '[anchor' ) ):
    #                 ## TODO - treat closing anchors as special
    #                 self.tag_end_stack.append( '[/anchor]' )
    #             elif( chunk.startswith( '[color' ) ):
    #                 self.tag_end_stack.append( '[/color]' )
    #             elif( chunk.startswith( '[font' ) ):
    #                 self.tag_end_stack.append( '[/font]' )
    #             elif( chunk.startswith( '[ref' ) ):
    #                 ## TODO - treat closing ref as special
    #                 self.tag_end_stack.append( '[/ref]' )
    #             elif( chunk.startswith( '[size' ) ):
    #                 self.tag_end_stack.append( '[/size]' )
    #             else:
    #                 self.tag_end_stack.append( '{}/{}'.format( chunk[ 0 ] ,
    #                                                            chunk[ 1: ] ) )

    # def redraw_label( self , instance , value ):
    #     instance.text_size = ( instance.width, None )
    #     instance.height = instance.texture_size[1]

    
    # def plan_content_template( self , content = 'Hello World&br;' ):
    #     ## TODO - use a separate color pair for the plan content labels
    #     tmp_label = LabelB( color = cookie_jar.get( 'color_scheme' )[ 'content_fg' ] ,
    #                         bcolor = cookie_jar.get( 'color_scheme' )[ 'background' ] ,
    #                         halign = 'left' ,
    #                         valign = 'top' ,
    #                         markup = True ,
    #                         text = content )
    #     tmp_label.size_hint_y = None
    #     tmp_label.text_size = ( tmp_label.width , None )
    #     tmp_label.height = tmp_label.texture_size[ 1 ]
    #     tmp_label.bind( size = self.redraw_label ,
    #                     texture_size = self.redraw_label )
    #     ## TODO:  add on_long_press send to clipboard
    #     tmp_label.bind( on_ref_press = self.readFromRef )
    #     tmp_label.texture_update()
    #     return( tmp_label )

    # def find_safe_ends( self , chunks , start , end ):
    #     if( end - start == 0 ):
    #         return None
    #     chunk = '\n'.join( chunks[ start : end ] )
    #     chunk_label = self.plan_content_template( chunk )
    #     ##TODO -
    #     ##from kivy.core.window import Window
    #     ##print( 'Window.size = {}\ntexture_size[1] = {}'.format( Window.height ,
    #     ##                                                        chunk_label.texture_size[ 1 ] ) )
    #     if( chunk_label.texture_size[ 1 ] < 30000 ):
    #         return( [ end ] )
    #     else:
    #         gap = int( ( end - start ) / 2 )
    #         return( self.find_safe_ends( chunks , start , start + gap ) + self.find_safe_ends( chunks , start + gap , end ) )
        
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
            self.ids.toolbar.title = resp_dict[ 'plandata' ][ 'username' ]
            self.ids.plan.text = resp_dict[ 'plandata' ][ 'plan' ]
        #     if( response.status_code == requests.codes.ok ):
        #         json_response = response.json()
        #         ##print( 'Encoding = {}'.format( response.encoding ) )
        #         ##plan_body = response.text.encode( response.encoding )
        #         #### We don't actually need the grab the username because
        #         #### it was passed to the original function
        #         ##username = json_response[ 'plandata' ][ 'username' ]
        #         self.plan_body = self.cleanPlanBody( json_response[ 'plandata' ][ 'plan' ] ,
        #                                              response.encoding )
        #         plan_name = self.cleanPlanName( json_response[ 'plandata' ][ 'pseudo' ] ,
        #                                         response.encoding )
        #         last_login = self.adjustClock( json_response[ 'plandata' ][ 'last_login' ] )
        #         last_updated = self.adjustClock( json_response[ 'plandata' ][ 'last_updated' ] )
        #         response.close()
        #         plans_app.screens[ 3 ].ids.username.text = username
        #         plans_app.screens[ 3 ].ids.psuedo.text = plan_name
        #         plans_app.screens[ 3 ].ids.last_login.text = last_login
        #         plans_app.screens[ 3 ].ids.last_updated.text = last_updated
        #         ## If we got here from clicking the read button, then empty out the data
        #         #plans_app.screens[ 3 ].ids.finger.text = ''
        #         ## and move the scrollview back to the top of the page
        #         #plans_app.screens[ 3 ].ids.content_scroller.scroll_to( plans_app.screens[ 3 ].ids.username )
        # except Exception as e:
        #     st = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
        #     LLOOGG( 'Error:  {1}\n'.format( st , e ) )
