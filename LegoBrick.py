from maya import cmds

class LegoBrick(object):
    def __init__(self, length, width):
        self.brick = None
        self.length = length
        self.width = width
    
    def create_brick(self, color, plate=False):
        size_x = 0.8 * self.length
        size_y = 0.96
        size_z = 0.8 * self.width

        self.brick = cmds.polyCube(h=size_y, w=size_x, d=size_z, sx=5 * self.length, sy=6, sz=5 * self.width)
        self.create_studs()
    
    def select_inner_brick(self):
        inner_faces = []

        # finds the faces for the bottom inner brick
        for x in range(self.width * 5 + 1):
            if x > 0:
                start = (self.length * 5 * x) + (25 * self.length * self.width) + (55 * self.length)
                end = start + ((self.length * 5) - 1)

                if x != 1 and x != self.width * 5:
                    inner_faces.append('{0}.f[{1}:{2}]'.format(self.brick[0], start + 1, end - 1))
        
        cmds.select(inner_faces)
        return inner_faces
    
    def select_edges(self):
        edge_faces = []
       
        # finds the outer edge of the bottom of the brick
        for x in range(self.width * 5 + 1):
            if x > 0:
                start = (self.length * 5 * x) + (25 * self.length * self.width) + (55 * self.length)
                end = start + ((self.length * 5) - 1)

                if x == 1 or x == self.width * 5:
                    edge_faces.append('{0}.f[{1}:{2}]'.format(self.brick[0], start, end))
                else:
                    edge_faces.append('{0}.f[{1}]'.format(self.brick[0], start))
                    edge_faces.append('{0}.f[{1}]'.format(self.brick[0], end))
        
        cmds.select(edge_faces)
        return edge_faces

    def select_studs(self):
        stud_faces = []
        
        # finds the studs
        for x in range(self.width * 5 + 1):
            for y in range(self.length * 5 + 1):

                start = (self.length * 5 * x) + (25 * self.length)
                end = start + ((self.length * 5) - 1)
                
    
                if x % 5 != 1 and x % 5 != 0 and y % 5 != 1 and y % 5 != 0:
                    stud_faces.append('{0}.f[{1}]'.format(self.brick[0], start + (y - 1)))
        
        
        cmds.select(stud_faces)
        return stud_faces
    
    def create_inner_brick(self):
        inner_faces = self.select_inner_brick()

    def create_studs(self):
        stud_faces = self.select_studs()

        cmds.polyCircularizeFace()
        cmds.scale(0.8, 1, 0.8)

