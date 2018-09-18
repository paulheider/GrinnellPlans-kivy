## http://robertour.com/2015/07/15/kivy-label-or-widget-with-background-color-property/

from kivy.uix.label import Label
from kivy.properties import ListProperty

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<LabelB>:
  bcolor: 1, 1, 1, 1
  canvas.before:
    Color:
      rgba: self.bcolor
    Rectangle:
      pos: self.pos
      size: self.size
""")

class LabelB(Label):#class MyLabel(Label):
    bcolor = ListProperty([1,1,1,1])
    
    #def on_size(self, *args):
    #    self.canvas.before.clear()
    #    with self.canvas.before:
    #        Color( bcolor )#0, 1, 0, 0.25)
    #        Rectangle(pos=self.pos, size=self.size)
            
#Factory.register( 'KivyB' , module = 'LabelB' )
