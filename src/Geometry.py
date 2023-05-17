import numpy as np
from OpenGL.GL import *


class Geometry:
    def __init__(self, filename):
        # Vertices stores all of the model data per face in the following format:
        # vertex_x, vertex_y, vertex_z, texture_s, texture_t, normal_x, normal_y, normal_z
        # Each value is a 32bit float
        # This means that if you wanted to get all of the vertex data:
        # Your start index would be 0, size would be 3 (x, y , x) and your stride would be 32

        self.vertices = self.LoadFile(filename)
        self.vertexCount = len(self.vertices) // 8
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.lowerBound, self.upperBound = self.calcBoundBox()

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Create Vertex Attributes Pointers Here
        # Note that you will need to use ctypes.c_void_p(i) to specify the starting index
        # when using glVertexAttribPointer

        # position data
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        # texture data
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        # Normal's data
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))

    def calcBoundBox(self):
        
        # Select the x, y, z coordinates of the vertices
        xCoords = self.vertices[0::8]
        yCoords = self.vertices[1::8]
        zCoords = self.vertices[2::8]
        
        # Calculates the min and max x, y and z 
        lowerBound = [min(xCoords), min(yCoords), min(zCoords)]
        upperBound = [max(xCoords), max(yCoords), max(zCoords)]

        return lowerBound, upperBound
    
    def LoadFile(self, filename):

        # raw, unassembled data
        v = []
        vt = []
        vn = []

        # final, assembled and packed result
        vertices = []

        # open the obj file and read the data
        with open(filename, 'r') as f:
            line = f.readline()
            while line:
                firstSpace = line.find(" ")
                flag = line[0:firstSpace]
                if flag == "v":
                    # vertex
                    line = line.replace("v ", "")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    v.append(l)
                elif flag == "vt":
                    # texture coordinate
                    line = line.replace("vt ", "")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vt.append(l)
                elif flag == "vn":
                    # normal
                    line = line.replace("vn ", "")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vn.append(l)
                elif flag == "f":
                    # face, three or more vertices in v/vt/vn form
                    line = line.replace("f ", "")
                    line = line.replace("\n", "")
                    # get the individual vertices for each line
                    line = line.split(" ")
                    faceVertices = []
                    faceTextures = []
                    faceNormals = []
                    for vertex in line:
                        # break out into [v,vt,vn],
                        # correct for 0 based indexing.
                        l = vertex.split("/")
                        position = int(l[0]) - 1
                        faceVertices.append(v[position])
                        texture = int(l[1]) - 1
                        faceTextures.append(vt[texture])
                        normal = int(l[2]) - 1
                        faceNormals.append(vn[normal])
                    # obj file uses triangle fan format for each face individually.
                    # unpack each face
                    triangles_in_face = len(line) - 2

                    vertex_order = []
                    """
                        eg. 0,1,2,3 unpacks to vertices: [0,1,2,0,2,3]
                    """
                    for i in range(triangles_in_face):
                        vertex_order.append(0)
                        vertex_order.append(i + 1)
                        vertex_order.append(i + 2)
                    for i in vertex_order:
                        for x in faceVertices[i]:
                            vertices.append(x)
                        for x in faceTextures[i]:
                            vertices.append(x)
                        for x in faceNormals[i]:
                            vertices.append(x)
                line = f.readline()
        return vertices

    def cleanup(self):
        glDeleteBuffers(1, (self.vbo,))