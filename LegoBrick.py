from maya import cmds

class LegoBrick(object):
    def __init__(self):
        self.brick = None
    
    def create_brick(self, length, width, color, plate=False):
        size_x = 0.8
        size_y = 0.96
        size_z = 0.8

        brick = cmds.polyCube(h=size_y, w=size_x, d=size_z, sx=5, sy=6, sz=5)
        edge_faces = self.select_edges()
        stud_faces = []

        # finds the start and end index for each row of faces
        for x in range(width * 5 + 1):
            if x > 0:
                start = length * 5 * x
                end = start + ((length * 5) - 1)

        # cmds.select(stud_faces)
        # cmds.polyCircularizeFace()
        # cmds.scale(0.8, 1, 0.8)
    
    # currently selects edges of the top face, needs to select edges of the bottom face
    def select_edges(self, width, length):
        edge_faces = []

        # finds the start and end index for each row of faces
        for x in range(width * 5 + 1):
            if x > 0:
                start = length * 5 * x
                end = start + ((length * 5) - 1)

                if x == 1 or x == width * 5:
                    edge_faces.append('{0}.f[{1}:{2}]'.format(self.brick[0], start, end))
                else:
                    edge_faces.append('{0}.f[{1}]'.format(self.brick[0], start))
                    edge_faces.append('{0}.f[{1}]'.format(self.brick[0], end))

    def select_studs(self):
        pass