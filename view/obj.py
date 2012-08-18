import os
import warnings

from pyglet.gl import *
from pyglet import image

class Material(object):
    diffuse   = [.8, .8, .8]
    ambient   = [.2, .2, .2]
    specular  = [0., 0., 0.]
    emission  = [0., 0., 0.]
    shininess = 0.

    #specular  = [0.5, 0.5, 0.5]
    #emission  = [0.5, 0.5, 0.5]
    #shininess = 0.5

    opacity   = 1.
    texture   = None

    def __init__(self, name):
        self.name = name

    def apply(self, face=GL_FRONT_AND_BACK):
        #print "Applying material: %s" % self
        #import pdb; pdb.set_trace()
        if self.texture:
            glEnable(self.texture.target)
            glBindTexture(self.texture.target, self.texture.id)
        else:
            glDisable(GL_TEXTURE_2D)

        glMaterialfv(face, GL_DIFFUSE,
            (GLfloat * 4)(*(self.diffuse + [self.opacity])))
        glMaterialfv(face, GL_AMBIENT,
            (GLfloat * 4)(*(self.ambient + [self.opacity])))
        glMaterialfv(face, GL_SPECULAR,
            (GLfloat * 4)(*(self.specular + [self.opacity])))
        glMaterialfv(face, GL_EMISSION,
            (GLfloat * 4)(*(self.emission + [self.opacity])))
        glMaterialf(face, GL_SHININESS, self.shininess)

    def __str__(self):
      return """diffuse: %s, 
      ambient: %s, 
      specular: %s,
      emission: %s,
      shininess: %s""" % (self.diffuse,
                         self.ambient,
                         self.specular,
                         self.emission,
                         self.shininess)

class MaterialGroup(object):
    def __init__(self, material):
        self.material = material

        # Interleaved array of floats in GL_T2F_N3F_V3F format
        self.vertices = []
        self.array = None

class Mesh(object):
    def __init__(self, name):
        self.name = name
        self.groups = []

        # Display list, created only if compile() is called, but used
        # automatically by draw()
        self.list = None

    def draw(self):
        if self.list:
            glCallList(self.list)
            return

        glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
        glPushAttrib(GL_CURRENT_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT)
        #glPushAttrib(GL_CURRENT_BIT | GL_ENABLE_BIT)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        for group in self.groups:
            group.material.apply()
            #DUMMY_MATERIAL.apply()
            if group.array is None:
                group.array = (GLfloat * len(group.vertices))(*group.vertices)
                group.triangles = len(group.vertices) / 8
            glInterleavedArrays(GL_T2F_N3F_V3F, 0, group.array)
            glDrawArrays(GL_TRIANGLES, 0, group.triangles)
        glPopAttrib()
        glPopClientAttrib()

    def compile(self):
        if not self.list:
            list = glGenLists(1)
            glNewList(list, GL_COMPILE)
            self.draw()
            glEndList()
            self.list = list

class OBJ:
    def __init__(self, filename, file=None, path=None):
        self.materials = {}
        self.meshes = {}        # Name mapping
        self.mesh_list = []     # Also includes anonymous meshes

        if file is None:
            file = open(filename, 'r')

        if path is None:
            path = os.path.dirname(filename)
        self.path = path

        mesh = None
        group = None
        material = None

        vertices = [[0., 0., 0.]]
        normals = [[0., 0., 0.]]
        tex_coords = [[0., 0.]]

        for line in open(filename, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue

            if values[0] == 'v':
                vertices.append(map(float, values[1:4]))
            elif values[0] == 'vn':
                normals.append(map(float, values[1:4]))
            elif values[0] == 'vt':
                tex_coords.append(map(float, values[1:3]))
            elif values[0] == 'mtllib':
                #pass
                self.load_material_library(values[1])
            elif values[0] in ('usemtl', 'usemat'):
                material = self.materials.get(values[1], None)
                if material is None:
                    warnings.warn('Unknown material: %s' % values[1])
                if mesh is not None:
                    group = MaterialGroup(material)
                    mesh.groups.append(group)
            elif values[0] == 'o':
                mesh = Mesh(values[1])
                self.meshes[mesh.name] = mesh
                self.mesh_list.append(mesh)
                group = None
            elif values[0] == 'f':
                if mesh is None:
                    mesh = Mesh('')
                    self.mesh_list.append(mesh)
                if material is None:
                    material = Material()
                if group is None:
                    group = MaterialGroup(material)
                    mesh.groups.append(group)

                # For fan triangulation, remember first and latest vertices
                v1 = None
                vlast = None
                points = []
                for i, v in enumerate(values[1:]):
                    v_index, t_index, n_index = \
                        (map(int, [j or 0 for j in v.split('/')]) + [0, 0])[:3]
                    if v_index < 0:
                        v_index += len(vertices) - 1
                    if t_index < 0:
                        t_index += len(tex_coords) - 1
                    if n_index < 0:
                        n_index += len(normals) - 1
                    vertex = tex_coords[t_index] + \
                             normals[n_index] + \
                             vertices[v_index]

                    if i >= 3:
                        # Triangulate
                        group.vertices += v1 + vlast
                    group.vertices += vertex

                    if i == 0:
                        v1 = vertex
                    vlast = vertex
                   
    def open_material_file(self, filename):
        '''Override for loading from archive/network etc.'''
        return open(os.path.join(self.path, filename), 'r')

    def load_material_library(self, filename):
        material = None
        file = self.open_material_file(filename)

        for line in file:
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue

            #import pdb; pdb.set_trace()
            if values[0] == 'newmtl':
                material = Material(values[1])
                self.materials[material.name] = material
            elif material is None:
                warnings.warn('Expected "newmtl" in %s' % filename)
                continue

            try:
                if values[0] == 'Kd':
                    material.diffuse = map(float, values[1:])
                elif values[0] == 'Ka':
                    material.ambient = map(float, values[1:])
                elif values[0] == 'Ks':
                    material.specular = map(float, values[1:])
                elif values[0] == 'Ke':
                    material.emissive = map(float, values[1:])
                elif values[0] == 'Ns':
                    material.shininess = float(values[1])
                elif values[0] == 'd':
                    material.opacity = float(values[1])
                elif values[0] == 'map_Kd':
                    try:
                        material.texture = image.load(values[1]).texture
                    except image.ImageDecodeException:
                        warnings.warn('Could not load texture %s' % values[1])
            except:
                warnings.warn('Parse error in %s.' % filename)

    def draw(self):
        for mesh in self.mesh_list:
            mesh.draw()

DUMMY_MATERIAL = Material('Example')

def loadOBJ(filename):  
    numVerts = 0  
    verts = []  
    norms = []  
    vertsOut = []  
    normsOut = []  
    for line in open(filename, "r"):  
        vals = line.split()  
        if vals[0] == "v":  
            v = map(float, vals[1:4])  
            verts.append(v)  
        if vals[0] == "vn":  
            n = map(float, vals[1:4])  
            norms.append(n)  
        if vals[0] == "f":  
            for f in vals[1:]:  
                w = f.split("/")  
                # OBJ Files are 1-indexed so we must subtract 1 below  
                vertsOut.append(list(verts[int(w[0])-1]))  
                normsOut.append(list(norms[int(w[2])-1]))  
                numVerts += 1  
    return vertsOut, normsOut  

class Man(object):
  def __init__(self, filename):
    vertices, normals = loadOBJ(filename)
    self.vertices = vertices
    self.normals = normals
    
    #import pdb; pdb.set_trace()

    #c_vertices = (GLfloat * len(vertices))(*vertices)
    #c_normals  = (GLfloat * len(normals))(*normals)
    
    raw_vertices = [value for vertex in vertices for value in vertex]
    raw_normals  = [value for normal in normals  for value in normal]

    c_vertices = (GLfloat * len(raw_vertices))(*raw_vertices)
    c_normals  = (GLfloat * len(raw_normals)) (*raw_normals)

    indices = []
    for i in range(len(raw_vertices) - 1):
      if (i + 1) % 3 == 0:
        #indices.append(raw_vertices[i])
        indices.append(i)

    indices = (GLuint * len(indices))(*indices)

    self.list = glGenLists(1)
    glNewList(self.list, GL_COMPILE)

    glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, c_vertices)
    glNormalPointer(GL_FLOAT, 0, c_normals)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, indices)
    glPopClientAttrib()

  def draw(self):
    glCallList(self.list)
