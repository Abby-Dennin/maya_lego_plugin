from maya import cmds

class LegoBrick(object):
    def __init__(self):
        self.brick = None
    
    def create_brick(self, length, width, color, plate=False):
        size_x = 0.8
        size_y = 0.96
        size_z = 0.8

        brick = cmds.polyCube(h=size_y, w=size_x, d=size_z, sx=5, sy=6, sz=5)
        stud_faces = ['{}.f[36:38]'.format(brick),
                      '{}.f[41:43]'.format(brick),
                      '{}.f[46:48]'.format(brick)]

        cmds.select(stud_faces)
        cmds.polyCircularizeFace()
        cmds.scale(0.8, 1, 0.8)
        