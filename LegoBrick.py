from maya import cmds 
import sys
import importlib

sys.path.append("C:\\Users\\abiga\\OneDrive\\Documents\\maya\\2024\\plug-ins")

from maya_lego_plugin import LegoColors

importlib.reload(LegoColors)

class LegoBrick(object):
    def __init__(self, length, width, brick=None):
        self.brick = brick
        self.length = length
        self.width = width
        self.color = None
    
    def create_brick(self, name):
        size_x = 0.8 * self.length
        size_y = 0.96
        size_z = 0.8 * self.width

        self.brick = cmds.polyCube(h=size_y, w=size_x, d=size_z, sx=5 * self.length, sy=6, sz=5 * self.width)
        self.brick = cmds.rename(name)
        self.create_studs()
        self.create_inner_brick()
        self.set_random_color()
    
    def move_brick(self, x, y, z): 
        cmds.select(self.brick)
        cmds.move(x, y, z)

    def get_brick(self):
        return self.brick
    
    def select_inner_brick(self):
        inner_faces = []

        # finds the faces for the bottom inner brick
        for x in range(self.width * 5 + 1):
            if x > 0:
                start = (self.length * 5 * x) + (25 * self.length * self.width) + (55 * self.length)
                end = start + ((self.length * 5) - 1)

                if x != 1 and x != self.width * 5:
                    inner_faces.append('{0}.f[{1}:{2}]'.format(self.brick, start + 1, end - 1))
        
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
                    edge_faces.append('{0}.f[{1}:{2}]'.format(self.brick, start, end))
                else:
                    edge_faces.append('{0}.f[{1}]'.format(self.brick, start))
                    edge_faces.append('{0}.f[{1}]'.format(self.brick, end))
        
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
                    stud_faces.append('{0}.f[{1}]'.format(self.brick, start + (y - 1)))
        
        
        cmds.select(stud_faces)
        return stud_faces
    
    def create_inner_brick(self):
        inner_faces = self.select_inner_brick()
        cmds.polyExtrudeFacet(ltz=-.8)

    def create_studs(self):
        stud_faces = self.select_studs()

        cmds.polyCircularizeFace()
        #cmds.scale(0.8, 1, 0.8)
        cmds.polyExtrudeFacet(ltz=.16)
    
    def set_random_color(self):
        lego_colors = LegoColors.LegoColors()
        self.color = lego_colors.get_random_color()

        materials = cmds.ls(mat=True)
        sg = "{0}{1}".format(self.color['name'].replace(" ", "").replace("-", ""), "SG")
        
        if self.color['name'].replace(" ", "").replace("-", "") in materials:
               cmds.sets(self.brick, forceElement=sg)
        else:
            self.create_material()
    
    def create_material(self):
        material_name = self.color['name'].replace(" ", "").replace("-", "")
        base_color_hex = self.color['hex']
        base_color_rgb = tuple(int(base_color_hex[i:i+2], 16) for i in (0, 2, 4))

        material, sg = self.create_shader(material_name, base_color_rgb)

        cmds.sets(self.brick, forceElement=sg)
    
    def create_shader(self, name, base_color):
        material = cmds.shadingNode("lambert", name=name, asShader=True)
        sg = cmds.sets(name="%sSG" % name, empty=True, renderable=True, noSurfaceShader=True)
        cmds.setAttr("{0}.color".format(name), float(base_color[0] / 255), float(base_color[1] / 255), float(base_color[2] / 255), type='double3')

        cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
        return material, sg
