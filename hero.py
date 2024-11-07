class Hero():
    def __init__(self,pos,land):
        self.mode = True
        self.land = land
        self.hero = loader.loadModel("Car.egg")
        self.hero.setTexture(loader.loadTexture("TextureMap.tif"))
       
        #self.hero.setColor(1,0.5,0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_hero()


    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0,0,1.5)
        self.cameraOn = True
        
    def cameraUp(self):
        pos = self.hero.getPos()
        
        base.mouseInterfaceNode.setPos( -pos[0], -pos[1], -pos[2] -3 )
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False
    def accept_hero(self):
        base.accept( 'c' , self.changeView)
        base.accept("n", self.turn_left)
        base.accept('n'+'-repeat', self.turn_left)
        base.accept("m", self.turn_right)
        base.accept('m'+'-repeat', self.turn_right)


        base.accept('w' , self.forward)
        base.accept('w'+'-repeat', self.forward)

        base.accept('s' , self.back)
        base.accept('s'+'-repeat', self.back)

        base.accept('a' , self.left)
        base.accept('a'+'-repeat', self.left)

        base.accept('d' , self.right)
        base.accept('d'+'-repeat', self.right)

        base.accept('z', self.changeMode)
        base.accept('z'+'-repeat', self.changeMode)

        base.accept('b', self.build)
        base.accept('v', self.destroy)


        base.accept('k', self.land.saveMap)
        base.accept('r', self.land.loadMap)



        


        



    def changeView(self):
        if  self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def turn_left(self):
        self.hero.setH((self.hero.getH()+ 5) % 360)
    def turn_right(self):
        self.hero.setH((self.hero.getH()+ 5) % 360)

    def check_dir(self,angle):
        if angle >= 0 and angle <=20:
            return (0, -1)
        elif angle <= 65:
            return(1, -1)
        elif angle <= 110:
            return(1, 0)
        elif angle <= 155:
            return(1, 1)
        elif angle <= 200:
            return(0, 1)
        elif angle <= 245:
            return(-1, 1)
        elif angle <= 290:
            return(-1, 0)
        elif angle <= 335:
            return(-1, -1)
        else:
            return(0, -1)
    
    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = x_from + dy
        return x_to, y_to, z_from
    

        
    def just_move(self,angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)



    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)


    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH()+180) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)


    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
                pos = self.land.findHighestEmpty(pos)
                self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] +1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ()+1)


    def down(self):
        if self.mode and self.hero.getZ()>1:
            self.hero.getZ(self.hero.getZ()-1)

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)
