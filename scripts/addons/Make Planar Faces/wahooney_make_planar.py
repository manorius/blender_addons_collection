# wahooney_make_planar.py Copyright (C) 2014, Keith "Wahooney" Boshoff
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****

'''
History
==

* 1.0 : Initial Version


Future
==

* 1.1 : Select between Last/Active, Average Plane, Per Face

'''

bl_info = {
    'name': 'Make Faces Planar',
    'author': 'Keith (Wahooney) Boshoff',
    'version': '1.0',
    'blender': (2, 7, 3),
    'location': 'Mesh > Make Faces Planar',
    'url': '',
    'category': 'Mesh'}


import bpy
from bpy.props import *
import bmesh
from mathutils import Vector
from mathutils import geometry

def main(self, context):
    obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    face_sets = []

    faces = []

    force_orthogonal = self.properties.force_orthogonal
    method = self.properties.method

    # store data
    for f in bm.faces:
        if f.select:
            if method == 'AVERAGE':
                faces.append (f)

            elif method == 'INDIVIDUAL':
                face_sets.append ([f])

    if method == 'AVERAGE':
        face_sets.append (faces)

    for fs in face_sets:

        normal = Vector ()
        center = Vector ()

        for f in fs:
            normal += f.normal
            center += f.calc_center_median_weighted ()

        normal.normalize ()
        center /= len (fs)

        if force_orthogonal:
            x = abs (normal.x)
            y = abs (normal.y)
            z = abs (normal.z)

            if x > y and x > z:
                normal.x /= x
                normal.y = 0.0
                normal.z = 0.0

            if y > x and y > z:
                normal.x = 0.0
                normal.y /= y
                normal.z = 0.0

            if z > y and z > x:
                normal.x = 0.0
                normal.y = 0.0
                normal.z /= z

        for f in fs:
            for v in f.verts:
                d = geometry.distance_point_to_plane (v.co, center, normal)
                v.co -= normal * d

    bmesh.update_edit_mesh(me)


class MakeFacesPlanar(bpy.types.Operator):
    """Makes faces planar to each other"""
    bl_idname = "mesh.make_faces_planar"
    bl_label = "Make Faces Planar"
    bl_options = {'REGISTER', 'UNDO'}

    force_orthogonal = BoolProperty(name="Force orthogonal", description="Force the plane to be fully on X, Y or Z",
            default=False)

    method = EnumProperty(items=(
                        ('AVERAGE', "Selection Average", "Average plane of all selected faces"),
                        ('CONTIGUOUS', "Contiguos Faces", "Make each continuous selection planar to iself"),
                        ('INDIVIDUAL', "Individual Faces", "Make each face planar to itself")),
                name="Method",
                description="Method planes are calculated",
                default='AVERAGE')

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        main(self, context)
        return {'FINISHED'}

addon_keymaps = []

def register_keymaps():

    kc = bpy.context.window_manager.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name="Mesh")

        # Orthogonal Make Planar
        kmi = km.keymap_items.new("mesh.make_faces_planar", 'P', 'PRESS', ctrl=True, shift=True, alt=True)
        kmi.properties.force_orthogonal = True

        # Regular Make Planar
        kmi = km.keymap_items.new("mesh.make_faces_planar", 'P', 'PRESS', ctrl=True, shift=True)
        kmi.properties.force_orthogonal = False

        addon_keymaps.append (km)


def unregister_keymaps():

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        for km in addon_keymaps:
            for kmi in km.keymap_items:
                km.keymap_items.remove(kmi)

            wm.keyconfigs.addon.keymaps.remove(km)

    # clear the list
    del addon_keymaps[:]

def register():

    bpy.utils.register_class(MakeFacesPlanar)

    register_keymaps ()

def unregister():
    bpy.utils.unregister_class(MakeFacesPlanar)

    unregister_keymaps ()

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.mesh.make_faces_planar()
