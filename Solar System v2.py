import os
import sys
#C:\Users\Vadim\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\panda3d\models
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from direct.showbase.ShowBase import *
from direct.task import Task
from panda3d.core import *

base = ShowBase()

dir = os.path.abspath(__file__).strip('Solar System v2.py')

def lightIntensive():
    return 100, 100, 100, 0.00001

class World(DirectObject.DirectObject):

    def __init__(self):
        self.title = OnscreenText(  
            text=u"Simple model of the Solar System\nDeveloped by students from 465 group:\n Tatarincev V.P.\n Vinokurov N.A.",
            parent=base.a2dBottomRight, align=TextNode.A_right,
            style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.25), scale=.07)

        self.title2 = OnscreenText(  
            text=u"Instructions:\n[P] - pause\n[mouse] - move",
            parent=base.a2dBottomLeft, align=TextNode.A_left,
            style=1, fg=(1, 1, 1, 1), pos=(0.0, 0.25), scale=.09)

        
        base.setBackgroundColor(0, 0, 0)

        
        def loadLight(x = 33):
            #удалённость источника света от солнца (2 - отключить солнце, норма = 4-5, больше 15 - всё светло)

            plight = PointLight('plight')
            plight.setColor(VBase4(lightIntensive()))
            plnp = render.attachNewNode(plight)
            plnp.setPos(1*x, 0, 0)
            render.setLight(plnp)

            plight = PointLight('plight')
            plight.setColor(VBase4(lightIntensive()))
            plnp = render.attachNewNode(plight)
            plnp.setPos(-1*x, 0, 0)
            render.setLight(plnp)

            plight = PointLight('plight')
            plight.setColor(VBase4(lightIntensive()))
            plnp = render.attachNewNode(plight)
            plnp.setPos(0, 1*x, 0)
            render.setLight(plnp)

            plight = PointLight('plight')
            plight.setColor(VBase4(lightIntensive()))
            plnp = render.attachNewNode(plight)
            plnp.setPos(0, -1*x, 0)
            render.setLight(plnp)

            plight = PointLight('plight')
            plight.setColor(VBase4(lightIntensive()))
            plnp = render.attachNewNode(plight)
            plnp.setPos(0, 0, 1*x)
            render.setLight(plnp)

            plight = PointLight('plight')
            plight.setColor(VBase4(lightIntensive()))
            plnp = render.attachNewNode(plight)
            plnp.setPos(0, 0, -1*x)
            render.setLight(plnp)

            #включаем свет от дальних звезд
            alight = AmbientLight('alight')
            alight.setColor(VBase4(0.1, 0.1, 0.1, 1))
            alnp = render.attachNewNode(alight)
            render.setLight(alnp)
        
        loadLight()
 
        self.yearscale = 60
        # Скорость вращения Земли
        self.dayscale = self.yearscale / 360.0 * 5
        self.orbitscale = 50  #  10
        self.sizescale = 0.6  #  0.6
        self.loadPlanets()  
        self.rotatePlanets()

        self.accept("p", self.handleEarth)

    def togglePlanet(self, planet, day, orbit=None, text=None):
        if day.isPlaying():
            print("Pausing " + planet)
            state = " [PAUSED]"
        else:
            print("Resuming " + planet)
            state = " [RUNNING]"

        if text:
            old = text.getText()
            text.setText(old[0:old.rfind(' ')] + state)

        self.toggleInterval(day)
        if orbit:
            self.toggleInterval(orbit)

    def toggleInterval(self, interval):
        if interval.isPlaying():
            interval.pause()
        else:
            interval.resume()

    def handleEarth(self):
        self.togglePlanet("Earth", self.day_period_earth,
                          self.orbit_period_earth)
        self.togglePlanet("Moon", self.day_period_moon,
                          self.orbit_period_moon)

    def loadPlanets(self):

        self.orbit_root_earth = render.attachNewNode('orbit_root_earth')

        self.orbit_root_moon = (
            self.orbit_root_earth.attachNewNode('orbit_root_moon'))
        # Небо
        self.sky = loader.loadModel("models/solar_sky_sphere")
        self.sky_tex = loader.loadTexture("2k_stars.jpg")
        self.sky.setTexture(self.sky_tex, 1)
        self.sky.reparentTo(render)
        self.sky.setScale(400) #40
        # Солнце
        self.sun = loader.loadModel("models/planet_sphere")
        self.sun_tex = loader.loadTexture("models/sun_8k.jpg")     
        #self.sun_tex = loader.loadTexture("models/123456.jpg")  
        self.sun.setTexture(self.sun_tex, 1)       
        self.sun.reparentTo(render)
        self.sun.setScale(30 * self.sizescale) #2       
        # Земля
        self.earth = loader.loadModel("models/planet_sphere")
        self.earth_tex = loader.loadTexture("models/2k_earth.jpg")
        self.earth.setTexture(self.earth_tex, 1)
        self.earth.reparentTo(self.orbit_root_earth)
        self.earth.setScale(self.sizescale) #none
        self.earth.setPos(self.orbitscale, 0, 0)
        #Луна
        self.orbit_root_moon.setPos(self.orbitscale, 0, 0)
        self.moon = loader.loadModel("models/planet_sphere")
        self.moon_tex = loader.loadTexture("models/2k_moon.jpg")
        #self.moon_tex = loader.loadTexture("models/123456.jpg")
        self.moon.setTexture(self.moon_tex, 1)
        self.moon.reparentTo(self.orbit_root_moon)
        self.moon.setScale(0.365 * self.sizescale) #0.3
        self.moon.setPos(0.1 * self.orbitscale, 0, 0) #Коэффицент показывает на отдалённость луны

    def rotatePlanets(self):

        self.day_period_sun = self.sun.hprInterval(20, (360, 0, 0))

        self.orbit_period_earth = self.orbit_root_earth.hprInterval(
            self.yearscale, (360, 0, 0))
        self.day_period_earth = self.earth.hprInterval(
            self.dayscale, (360, 0, 0))

        self.orbit_period_moon = self.orbit_root_moon.hprInterval(
            (.0749 * self.yearscale), (360, 0, 0))
        self.day_period_moon = self.moon.hprInterval(
            (.0749 * self.yearscale), (360, 0, 0))

        self.day_period_sun.loop()   
        self.orbit_period_earth.loop()
        self.day_period_earth.loop()
        self.orbit_period_moon.loop()
        self.day_period_moon.loop()

w = World()
base.run()
