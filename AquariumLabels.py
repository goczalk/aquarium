from pgu import gui
import pygame

BLACK = (0, 0, 0)

class AquariumLabels(gui.Table):
    def update_plancton_fish_labels(self, units_of_time, plancton, male, female, ill):
            self.time_label.set_text("Time: {0}".format(units_of_time))
            self.plancton_label.set_text("Plancton: {0}".format(plancton))
            self.male_fish_label.set_text("Male fish: {0}".format(male))
            self.female_fish_label.set_text("Female fish: {0}".format(female))
            self.ill_fish_label.set_text("Sick fish: {0}".format(ill))

    def __init__(self,**params):
        gui.Table.__init__(self,**params)
        self.time_label = gui.Label("Time: 0", color=BLACK)
        self.plancton_label = gui.Label("Plancton: 0", color=BLACK)
        self.male_fish_label = gui.Label("Male fish: 0", color=BLACK)
        self.female_fish_label = gui.Label("Female fish: 0", color=BLACK)
        self.ill_fish_label = gui.Label("Ill fish: 0", color=BLACK)

        def fullscreen_changed(btn):
            pygame.display.toggle_fullscreen()

        self.tr()
        self.td(gui.Label("Statistics", color=BLACK), colspan=2)

        self.tr()
        self.td(self.time_label, align=-1)

        self.tr()
        self.td(self.plancton_label, align=-1)
        #e = gui.HSlider(100,-500,500,size=20,width=100,height=16,name='speed')
        #self.td(e)
        
        self.tr()
        self.td(self.male_fish_label, align=-1)

        self.tr()
        self.td(self.female_fish_label, align=-1)


        self.tr()
        self.td(self.ill_fish_label, align=-1)
        #e = gui.HSlider(2,1,5,size=20,width=100,height=16,name='size')
        #self.td(e)
        
        #self.tr()
        #self.td(gui.Label("Quantity: ",color=BLACK),align=1)
        #e = gui.HSlider(100,1,1000,size=20,width=100,height=16,name='quantity')
        #e.connect(gui.CHANGE, stars_changed, e)
        #self.td(e)
        
        btn = gui.Switch(value=False, name='fullscreen')
        btn.connect(gui.CHANGE, fullscreen_changed, btn)

        self.tr()
        self.td(gui.Label("Full Screen: ", color=BLACK), align=-1)
        self.td(btn)
        
        #self.tr()
        #self.td(gui.Label("Warp Speed: ",color=BLACK),align=1)
        #self.td(gui.Switch(value=False,name='warp'))

