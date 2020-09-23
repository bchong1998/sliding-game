from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
import image_slicer
from random import shuffle
from PIL import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
import copy
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os

class LoadPicture(Screen):
    def selected(self, filename):
        try:
            self.ids.img.source = filename[0]
            global selectedimage
            selectedimage = filename[0]
            secondwindow.update()           
        except:
            pass

class DisplayPicture(Screen):
    def __init__(self, **kwargs):
        super(DisplayPicture,self).__init__(**kwargs)
        global secondwindow 
        secondwindow = self
    
    def update(self, *args):
        global selectedimage 
        self.ids.img2.source = selectedimage
        
    def make_square(self, im, min_size=256, fill_color=(0,0,0,0)):
        im = Image.open(im)
        if im.size[0] > 256 or im.size[1] > 256:
            im = im.resize((256,256))
        self.x, self.y = im.size
        size = max(min_size, self.x, self.y)
        global new_im
        new_im = Image.new('RGBA', (size, size), fill_color)
        new_im.paste(im, (int((size - self.x) / 2), int((size - self.y) / 2)))
        new_im.save('squareimage.png')
        
    #divide image into 4*4 tiles
    def crop_image(self):
        image_slicer.slice('squareimage.png', 16)

class ScrambledPicture(Screen):
    def __init__(self, **kwargs):
        super(ScrambledPicture, self).__init__(**kwargs)
        self.tile_list = []
        self.grid_pos = []
        self.image_list = []
        self.tile_list_array = [[164.0,436.0],[228.0,436.0],[292.0,436.0],[356.0,436.0],
                                [164.0,372.0],[228.0,372.0],[292.0,372.0],[356.0,372.0],
                                [164.0,308.0],[228.0,308.0],[292.0,308.0],[356.0,308.0],
                                [164.0,244.0],[228.0,244.0],[292.0,244.0],[356.0,244.0]]

        self.correct_grid_pos = [[164.0,436.0],[228.0,436.0],[292.0,436.0],[356.0,436.0],
                                [164.0,372.0],[228.0,372.0],[292.0,372.0],[356.0,372.0],
                                [164.0,308.0],[228.0,308.0],[292.0,308.0],[356.0,308.0],
                                [164.0,244.0],[228.0,244.0],[292.0,244.0]]
        #shuffle the tile positions
        shuffle(self.tile_list_array)
        f = FloatLayout(size_hint = (0.1,0.1))
        f.add_widget(Label(text='hi'))
        for i in range(1, 5):
            for j in range(1, 5):
                btn = Button(name = str('btn' + str(i*4+j-4)),
                            id = str('btn'+ str(i*4+j-4)),
                            size = (64,64),
                            pos = (self.tile_list_array[i*4+j-5][0], self.tile_list_array[i*4+j-5][1]),
                            on_release = self.move_tile
                            )
                self.image_list.append(str('squareimage_0' + str(i) + '_0' + str(j) + '.png'))
                self.tile_list.append(btn)
                self.grid_pos.append(btn.pos)
                f.add_widget(btn)
        self.add_widget(f)
        f.add_widget(Button(text = 'Solve',
                            pos = (292.5,0),
                            on_release = self.do_you_win
                            ))
        f.remove_widget(self.tile_list[15]) #the same picture will always be popped
        self.tile_list.pop(15)
        self.grid_pos.pop(15)
        self.image_list.pop(15)
        
        self.score = 0
        
    def closeAndDeleteFiles(self,*args):
        for i in range(0,15):
            os.remove(str(self.image_list[i]))
        os.remove('squareimage_04_04.png')
        os.remove('squareimage.png')


    def change_tile_image(self):
        for i in range(0,15):
            self.tile_list[i].background_normal = str(self.image_list[i])

    def move_tile(self, instance, *args):
        moveRight = Animation(x = instance.pos[0] + 64, y = instance.pos[1],duration = 0.1)
        moveLeft = Animation(x = instance.pos[0] - 64, y = instance.pos[1],duration = 0.1)
        moveUp = Animation(x = instance.pos[0], y = instance.pos[1] + 64,duration = 0.1)
        moveDown = Animation(x = instance.pos[0], y = instance.pos[1] - 64,duration = 0.1)
        #check if tile is blank
        lstWithoutInstance = copy.copy(self.tile_list)
        lstWithoutInstance.remove(instance)
        trueFalseDown = []
        trueFalseUp = []
        trueFalseLeft = []
        trueFalseRight = []

        if instance.pos[1] == 244:
            trueFalseDown.append(True)
        if instance.pos[1] == 436:
            trueFalseUp.append(True)
        if instance.pos[0] == 356:
            trueFalseRight.append(True)
        if instance.pos[0] == 164:
            trueFalseLeft.append(True)
        for tile in lstWithoutInstance:
            trueFalseDown.append(tile.collide_point(x = instance.pos[0]+32, y= instance.pos[1]-32))
            trueFalseUp.append(tile.collide_point(x=instance.pos[0]+32, y = instance.pos[1]+96))
            trueFalseRight.append(tile.collide_point(x=instance.pos[0]+ 96, y = instance.pos[1]+32))
            trueFalseLeft.append(tile.collide_point(x=instance.pos[0]-32, y = instance.pos[1]+32))
        
        if any(trueFalseDown) == False:
            moveDown.start(instance)
        if any(trueFalseUp) == False:
            moveUp.start(instance)
        if any(trueFalseRight) == False:
            moveRight.start(instance)
        if any(trueFalseLeft) == False:
            moveLeft.start(instance)
        #revert back to original with full tile list    
        lstWithoutInstance = self.tile_list
        self.score += 1
        

    def do_you_win(self,*args):
        current_pos = []
        #check current position of all the tiles
        for tile in self.tile_list:
            current_pos.append(tile.pos)
        popupwin = Popup(title = 'you win!',
                         content = Label(text = 'good job! your score is:' + str(self.score)),
                         size_hint = (0.5,0.5))
        popupnotyet = Popup(title = 'not yet!',
                         content = Label(text = 'continue solving!'),
                         size_hint = (0.5,0.5))
        if current_pos == self.correct_grid_pos:
            popupwin.open()

        else:
            popupnotyet.open()

class Screenmanager(ScreenManager):
    pass

kv = Builder.load_file("main.kv")


class MyMainApp(App):
    def build(self):
        Window.size = (640,640)
        return kv


if __name__ == "__main__":
    MyMainApp().run()