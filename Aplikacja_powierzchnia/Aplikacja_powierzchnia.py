from pickle import TRUE
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from bs4 import BeautifulSoup
import re
import requests
import sys

class PowierzchniaKraju(App):
    def build(self):
        #returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # image 
        #self.window.add_widget(Image(source="Favicon_2021_big.png"))

        # label 
        self.country_name = Label(
                        text= "Podaj nazwe kraju",
                        font_size= 25,
                        color= '#957DAD',
                        bold=TRUE
                        
                        )
        self.window.add_widget(self.country_name)

        # text input 
        self.user = TextInput(
                    multiline= False,
                    padding_y= (20,20),
                    size_hint= (1, 0.5),
                    font_size=30
                    )

        self.window.add_widget(self.user)

        # button
        self.button = Button(
                      text= "kliknij",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#957DAD',
                      color="#FFDFD3",
                      font_size = 40,

                      
                      )
        
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        return self.window

    def callback(self, introduce):
        # change label text to "Hello + user name!"
        
        country = self.user.text
        country_replace = country.replace(' ', '_')
        country_minimalize = country_replace.lower()
        country_upper = re.sub("(^|[_])\s*([a-zA-Z])", lambda p: p.group(0).upper(),country_minimalize)

        if country == "":
            self.country_name.text = 'Niepoprawne panstwo'
        else:       
            url = "https://pl.wikipedia.org/wiki/" + country_upper
            result = requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")
            powierzchnia = doc.find_all(text='Powierzchnia ')
            try:
                parent_powierzchnia = powierzchnia[0].parent

                grandparent = parent_powierzchnia.parent
                a = grandparent.find_all('p')
                b = a[0].text
                c = str(b)
                split_string = c.split('[') 
                d = split_string[0]
                substring = d.split('k')
                substring_2 = substring[0]
                self.country_name.text = "Powierzchnia " + str(country_upper.replace('_', ' ')) + " to: " + str(substring_2) + " km2"
                self.user.text=""
            except IndexError:
                self.country_name.text = 'Niepoprawne panstwo'
                self.user.text=""

if __name__ == "__main__":
    PowierzchniaKraju().run()