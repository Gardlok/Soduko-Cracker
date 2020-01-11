from kivy.app import App
from kivy.uix.button import Button

class Butt(App):
    def build(self):
        button = Button(text="Press Me", font_size="30sp",
                        background_color=(1,1,1,1),
                        color = (50,50,50,50),
                        size = (15,15),
                        )
        button.bind(on_press = self.clickit)
        return button
    
    def clickit(self, event):
        print("oh shiiiit!")
        
Butt().run()
        
