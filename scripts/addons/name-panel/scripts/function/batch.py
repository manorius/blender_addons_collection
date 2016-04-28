
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# imports
import bpy
import re
from random import random
from .. import storage

tag = False

# shared
class shared:
  '''
    Contains Lists;
      greasePencils
      objectData
      materials
      textures
  '''

  # grease pencils
  greasePencils = []

  particleSettings = []

  # object data
  objectData = []

  # materials
  materials = []

  # textures
  textures = []

# main
def main(context, quickBatch):
  '''
    Send datablock values to sort then send collections to process, action group & lineset names are sent to name.
  '''

  # tag
  global tag

  # panel
  panel = context.scene.NamePanel

  # option
  option = context.scene.BatchName

  # quick batch
  if quickBatch:

    # display names
    if panel.displayNames:

      # mode
      if panel.mode == 'SELECTED':

        for object in context.selected_objects[:]:

          # quick
          quick(context, object, panel, option)

          # all
        all = [
          # object
          storage.batch.objects,

          # cameras
          storage.batch.cameras,

          # meshes
          storage.batch.meshes,

          # curves
          storage.batch.curves,

          # lamps
          storage.batch.lamps,

          # lattices
          storage.batch.lattices,

          # metaballs
          storage.batch.metaballs,

          # speakers
          storage.batch.speakers,

          # armatures
          storage.batch.armatures,
          ]
        for collection in all:

          # process
          process(context, collection)

          # clear
          collection.clear()

        # mode
      else:
        for object in context.scene.objects[:]:
          if True in [x&y for (x,y) in zip(object.layers, context.scene.layers)]:

            # quick
            quick(context, object, panel, option)

        # all
        all = [
          # object
          storage.batch.objects,

          # cameras
          storage.batch.cameras,

          # meshes
          storage.batch.meshes,

          # curves
          storage.batch.curves,

          # lamps
          storage.batch.lamps,

          # lattices
          storage.batch.lattices,

          # metaballs
          storage.batch.metaballs,

          # speakers
          storage.batch.speakers,

          # armatures
          storage.batch.armatures,
          ]
        for collection in all:

          # process
          process(context, collection)

          # clear
          collection.clear()

    # display names
    else:

      # quick
      quick(context, context.active_object, panel, option)

      # all
      all = [
        # object
        storage.batch.objects,

        # cameras
        storage.batch.cameras,

        # meshes
        storage.batch.meshes,

        # curves
        storage.batch.curves,

        # lamps
        storage.batch.lamps,

        # lattices
        storage.batch.lattices,

        # metaballs
        storage.batch.metaballs,

        # speakers
        storage.batch.speakers,

        # armatures
        storage.batch.armatures,
        ]
      for collection in all:

        # process
        process(context, collection)

        # clear
        collection.clear()


  # quick batch
  else:
    # batch type
    if option.batchType in {'SELECTED', 'OBJECTS'}:

      # actions
      if option.actions:
        for object in bpy.data.objects[:]:
          if hasattr(object.animation_data, 'action'):

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:

                # object type
                if option.objectType in 'ALL':

                  # sort
                  sort(context, object.animation_data.action)

                # object type
                elif option.objectType in object.type:

                  # sort
                  sort(context, object.animation_data.action)

            # batch type
            else:

              # object type
              if option.objectType in 'ALL':

                # sort
                sort(context, object.animation_data.action)

              # object type
              elif option.objectType in object.type:

                # sort
                sort(context, object.animation_data.action)

        # clear duplicates
        actions = []
        [actions.append(item) for item in storage.batch.actions if item not in actions]
        storage.batch.actions.clear()

        # process
        process(context, actions)

      # action groups
      if option.actionGroups:
        for object in bpy.data.objects[:]:
          if hasattr(object.animation_data, 'action'):
            if hasattr(object.animation_data.action, 'name'):

              # batch type
              if option.batchType in 'SELECTED':
                if object.select:

                  # object type
                  if option.objectType in 'ALL':

                    # sort
                    sort(context, object.animation_data.action)

                  # object type
                  elif option.objectType in object.type:

                    # sort
                    sort(context, object.animation_data.action)

              # batch type
              else:

                # object type
                if option.objectType in 'ALL':

                  # sort
                  sort(context, object.animation_data.action)

                # object type
                elif option.objectType in object.type:

                  # sort
                  sort(context, object.animation_data.action)

        # clear duplicates
        actions = []
        [actions.append(item) for item in storage.batch.actions if item not in actions]
        storage.batch.actions.clear()

        # name action groups
        for action in actions:
          for group in action[1][1].groups:
            group.name = name(context, group.name) if not option.suffixLast else name(context, group.name) + option.suffix

      # grease pencil
      if option.greasePencil:
        for object in bpy.data.objects[:]:
          if hasattr(object.grease_pencil, 'name'):

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:

                # object type
                if option.objectType in 'ALL':
                  if object.grease_pencil.users == 1:

                    # sort
                    sort(context, object.grease_pencil)
                  else:

                    # shared
                    if object.grease_pencil not in shared.greasePencils[:]:
                      shared.greasePencils.append(object.grease_pencil)

                      # sort
                      sort(context, object.grease_pencil)

                # object type
                elif option.objectType in object.type:
                  if object.grease_pencil.users == 1:

                    # sort
                    sort(context, object.grease_pencil)
                  else:

                    # shared
                    if object.grease_pencil not in shared.greasePencils[:]:
                      shared.greasePencils.append(object.grease_pencil)

                      # sort
                      sort(context, object.grease_pencil)

            # batch type
            else:

              # object type
              if option.objectType in 'ALL':
                if object.grease_pencil.users == 1:

                  # sort
                  sort(context, object.grease_pencil)
                else:

                  # shared
                  if object.grease_pencil not in shared.greasePencils[:]:
                    shared.greasePencils.append(object.grease_pencil)

                    # sort
                    sort(context, object.grease_pencil)

              # object type
              elif option.objectType in object.type:
                if object.grease_pencil.users == 1:

                  # sort
                  sort(context, object.grease_pencil)

                else:

                  # shared
                  if object.grease_pencil not in shared.greasePencils[:]:
                    shared.greasePencils.append(object.grease_pencil)

                    # sort
                    sort(context, object.grease_pencil)

        # clear shared
        shared.greasePencils.clear()

        # process
        process(context, storage.batch.greasePencils)

        # clear collection
        storage.batch.greasePencils.clear()

      # pencil layers
      if option.pencilLayers:
        for object in bpy.data.objects[:]:
          if hasattr(object.grease_pencil, 'name'):

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:

                # object type
                if option.objectType in 'ALL':
                  if object.grease_pencil.users == 1:

                    # layers
                    for layer in object.grease_pencil.layers[:]:

                      # sort
                      sort(context, layer)
                  else:

                    # shared
                    if object.grease_pencil not in shared.greasePencils[:]:
                      shared.greasePencils.append(object.grease_pencil)

                      # layers
                      for layer in object.grease_pencil.layers[:]:

                        # sort
                        sort(context, layer)

                # object type
                elif option.objectType in object.type:
                  if object.grease_pencil.users == 1:

                    # layers
                    for layer in object.grease_pencil.layers[:]:

                      # sort
                      sort(context, layer)
                  else:

                    # shared
                    if object.grease_pencil not in shared.greasePencils[:]:
                      shared.greasePencils.append(object.grease_pencil)

                      # layers
                      for layer in object.grease_pencil.layers[:]:

                        # sort
                        sort(context, layer)

            # batch type
            else:

              # object type
              if option.objectType in 'ALL':
                if object.grease_pencil.users == 1:

                  # layers
                  for layer in object.grease_pencil.layers[:]:

                    # sort
                    sort(context, layer)
                else:

                  # shared
                  if object.grease_pencil not in shared.greasePencils[:]:
                    shared.greasePencils.append(object.grease_pencil)

                    # layers
                    for layer in object.grease_pencil.layers[:]:

                      # sort
                      sort(context, layer)

              # object type
              elif option.objectType in object.type:
                if object.grease_pencil.users == 1:

                  # layers
                  for layer in object.grease_pencil.layers[:]:

                    # sort
                    sort(context, layer)
                else:

                  # shared
                  if object.grease_pencil not in shared.greasePencils[:]:
                    shared.greasePencils.append(object.grease_pencil)

                    # layers
                    for layer in object.grease_pencil.layers[:]:

                      # sort
                      sort(context, layer)

            # process
            process(context, storage.batch.pencilLayers)

            print(storage.batch.pencilLayers)

            # clear collection
            storage.batch.pencilLayers.clear()

        # clear shared
        shared.greasePencils.clear()

      # objects
      if option.objects:
        for object in bpy.data.objects[:]:

          # batch type
          if option.batchType in 'SELECTED':
            if object.select:

              # object type
              if option.objectType in 'ALL':

                # sort
                sort(context, object)

              # object type
              elif option.objectType in object.type:

                # sort
                sort(context, object)

              # batch type
              else:

                # object type
                if option.objectType in 'ALL':

                  # sort
                  sort(context, object)

                # object type
                elif option.objectType in object.type:

                  # sort
                  sort(context, object)

        # process
        process(context, storage.batch.objects)

        # clear collection
        storage.batch.objects.clear()

      # groups
      if option.groups:
        for object in bpy.data.objects[:]:

          # batch type
          if option.batchType in 'SELECTED':
            if object.select:

              # object type
              if option.objectType in 'ALL':
                for group in bpy.data.groups[:]:
                  if object in group.objects[:]:

                    # sort
                    sort(context, group)


                    # object type
                  elif option.objectType in object.type:
                    for group in bpy.data.groups[:]:
                      if object in group.objects[:]:

                        # sort
                        sort(context, group)

                        # batch type
                      else:

                        # object type
                        if option.objectType in 'ALL':
                          for group in bpy.data.groups[:]:
                            if object in group.objects[:]:

                              # sort
                              sort(context, group)

                              # object type
                            elif option.objectType in object.type:
                              for group in bpy.data.groups[:]:
                                if object in group.objects[:]:

                                  # sort
                                  sort(context, group)

        # clear duplicates
        objectGroups = []
        [objectGroups.append(item) for item in storage.batch.groups if item not in objectGroups]
        storage.batch.groups.clear()

        # process
        process(context, objectGroups)

      # constraints
      if option.constraints:
        for object in bpy.data.objects[:]:

          # batch type
          if option.batchType in 'SELECTED':
            if object.select:
              for constraint in object.constraints[:]:

                # constraint type
                if option.constraintType in 'ALL':

                  # sort
                  sort(context, constraint)

                # constraint type
                elif option.constraintType in constraint.type:

                  # sort
                  sort(context, constraint)

          # batch type
          else:
            for constraint in object.constraints[:]:

              # constraint type
              if option.constraintType in 'ALL':

                # sort
                sort(context, constraint)

              # constraint type
              elif option.constraintType in constraint.type:

                # sort
                sort(context, constraint)

          # process
          process(context, storage.batch.constraints)

          # clear collection
          storage.batch.constraints.clear()

      # modifiers
      if option.modifiers:
        for object in bpy.data.objects[:]:

          # batch type
          if option.batchType in 'SELECTED':
            if object.select:
              for modifier in object.modifiers[:]:

                # modifier type
                if option.modifierType in 'ALL':

                  # sort
                  sort(context, modifier)

                # modifier tye
                elif option.modifierType in modifier.type:

                  # sort
                  sort(context, modifier)

          # batch type
          else:
            for modifier in object.modifiers[:]:

              # modifier type
              if option.modifierType in 'ALL':

                # sort
                sort(context, modifier)

              # modifier tye
              elif option.modifierType in modifier.type:

                # sort
                sort(context, modifier)

          # process
          process(context, storage.batch.modifiers)

          # clear collection
          storage.batch.modifiers.clear()

      # object data
      if option.objectData:
        for object in bpy.data.objects[:]:
          if object.type not in 'EMPTY':

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:

                # object type
                if option.objectType in 'ALL':
                  if object.data.users == 1:

                    # sort
                    sort(context, object.data)
                  else:

                    # shared
                    if object.data.name not in shared.objectData[:]:
                      shared.objectData.append(object.data.name)

                      # sort
                      sort(context, object.data)

                # object type
                elif option.objectType in object.type:
                  if object.data.users == 1:

                    # sort
                    sort(context, object.data)
                  else:

                    # shared shared
                    if object.data.name not in shared.objectData[:]:
                      shared.objectData.append(object.data.name)

                      # sort
                      sort(context, object.data)

            # batch type
            else:

              # object type
              if option.objectType in 'ALL':
                if object.data.users == 1:

                  # sort
                  sort(context, object.data)
                else:

                  # shared shared
                  if object.data.name not in shared.objectData[:]:
                    shared.objectData.append(object.data.name)

                    # sort
                    sort(context, object.data)

              # object type
              elif option.objectType in object.type:
                if object.data.users == 1:

                  # sort
                  sort(context, object.data)
                else:

                  # shared shared
                  if object.data.name not in shared.objectData[:]:
                    shared.objectData.append(object.data.name)

                    # sort
                    sort(context, object.data)

        # clear shared
        shared.objectData.clear()

        # object data
        objectData = [
          storage.batch.curves,
          storage.batch.cameras,
          storage.batch.meshes,
          storage.batch.lamps,
          storage.batch.lattices,
          storage.batch.metaballs,
          storage.batch.speakers,
          storage.batch.armatures
        ]

        # process collection
        for collection in objectData:

          # process
          process(context, collection)

          # clear collection
          collection.clear()

      # bone groups
      if option.boneGroups:
        for object in bpy.data.objects[:]:

          # batch type
          if option.batchType in 'SELECTED':
            if object.select:
              if object.type in 'ARMATURE':
                for group in object.pose.bone_groups[:]:
                  if object.select:

                    # sort
                    sort(context, group)

          # batch type
          else:
            if object.type in 'ARMATURE':
              for group in object.pose.bone_groups[:]:

                # sort
                sort(context, group)

          # process
          process(context, storage.batch.boneGroups)

          # clear collection
          storage.batch.boneGroups.clear()

      # bones
      if option.bones:
        for object in bpy.data.objects[:]:
          if object.type in 'ARMATURE':

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:

                # edit mode
                if object.mode in 'EDIT':
                  for bone in bpy.data.armatures[object.data.name].edit_bones[:]:
                    if bone.select:

                      # sort
                      sort(context, bone)

                # pose or object mode
                else:
                  for bone in bpy.data.armatures[object.data.name].bones[:]:
                    if bone.select:

                      # sort
                      sort(context, bone)

            # batch type
            else:

              # edit mode
              if object.mode in 'EDIT':
                for bone in bpy.data.armatures[object.data.name].edit_bones[:]:

                    # sort
                    sort(context, bone)

              # pose or object mode
              else:
                for bone in bpy.data.armatures[object.data.name].bones[:]:

                    # sort
                    sort(context, bone)

            # process
            process(context, storage.batch.bones)

            # clear collection
            storage.batch.bones.clear()

      # bone constraints
      if option.boneConstraints:
        for object in bpy.data.objects[:]:
          if object.type in 'ARMATURE':

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:
                for bone in object.pose.bones[:]:
                  if bone.bone.select:
                    for constraint in bone.constraints[:]:

                      # constraint type
                      if option.constraintType in 'ALL':

                        # sort
                        sort(context, constraint)

                      # constraint type
                      elif option.constraintType in constraint.type:

                        # sort
                        sort(context, constraint)

                    # process
                    process(context, storage.batch.constraints)

                    # clear collection
                    storage.batch.constraints.clear()

            # batch type
            else:
              for bone in object.pose.bones[:]:
                for constraint in bone.constraints[:]:

                  # constraint type
                  if option.constraintType in 'ALL':

                    # sort
                    sort(context, constraint)

                  # constraint type
                  elif option.constraintType in constraint.type:

                    # sort
                    sort(context, constraint)

                # process
                process(context, storage.batch.constraints)

                # clear collection
                storage.batch.constraints.clear()

      # vertex groups
      if option.vertexGroups:
        for object in bpy.data.objects[:]:
          if hasattr(object, 'vertex_groups'):

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:
                for group in object.vertex_groups[:]:

                  # object type
                  if option.objectType in 'ALL':

                    # sort
                    sort(context, group)

                  # object type
                  elif option.objectType in object.type:

                    # sort
                    sort(context, group)

                # process
                process(context, storage.batch.vertexGroups)

                # clear collection
                storage.batch.vertexGroups.clear()

            # batch type
            else:
              for group in object.vertex_groups[:]:

                # object type
                if option.objectType in 'ALL':

                  # sort
                  sort(context, group)

                # object type
                elif option.objectType in object.type:

                  # sort
                  sort(context, group)

              # process
              process(context, storage.batch.vertexGroups)

              # clear collection
              storage.batch.vertexGroups.clear()


      # shapekeys
      if option.shapekeys:
        for object in bpy.data.objects[:]:
          if hasattr(object.data, 'shape_keys'):
            if hasattr(object.data.shape_keys, 'key_blocks'):

              # batch type
              if option.batchType in 'SELECTED':
                if object.select:
                  for block in object.data.shape_keys.key_blocks[:]:

                    # object type
                    if option.objectType in 'ALL':

                      # sort
                      sort(context, block)

                    # object type
                    elif option.objectType in object.type:

                      # sort
                      sort(context, block)

              # batch type
              else:
                for block in object.data.shape_keys.key_blocks[:]:

                  # object type
                  if option.objectType in 'ALL':

                    # sort
                    sort(context, block)

                  # object type
                  elif option.objectType in object.type:

                    # sort
                    sort(context, block)

              # process
              process(context, storage.batch.shapekeys)

              # clear collection
              storage.batch.shapekeys.clear()

      # uvs
      if option.uvs:
        for object in bpy.data.objects[:]:
          if object.type in 'MESH':

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:
                for uv in object.data.uv_textures[:]:

                  # sort
                  sort(context, uv)

            # batch type
            else:
             for uv in object.data.uv_textures[:]:

                # sort
                sort(context, uv)

            # process
            process(context, storage.batch.uvs)

            # clear collection
            storage.batch.uvs.clear()

      # vertex colors
      if option.vertexColors:
        for object in bpy.data.objects[:]:
          if object.type in 'MESH':

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:
                for color in object.data.vertex_colors[:]:

                  # sort
                  sort(context, color)

            # batch type
            else:
              for color in object.data.vertex_colors[:]:

                # sort
                sort(context, color)

            # process
            process(context, storage.batch.vertexColors)

            # clear collection
            storage.batch.vertexColors.clear()

      # materials
      if option.materials:
        for object in bpy.data.objects[:]:

          # batch type
          if option.batchType in 'SELECTED':
            if object.select:
              for slot in object.material_slots[:]:
                if slot.material != None:
                  if slot.material.users == 1:

                    # object type
                    if option.objectType in 'ALL':

                      # sort
                      sort(context, slot.material)

                    # object type
                    elif option.objectType in object.type:

                      # sort
                      sort(context, slot.material)
                  else:

                    # shared
                    if slot.material not in shared.materials[:]:
                      shared.materials.append(slot.material)

                      # sort
                      sort(context, slot.material)

          # batch type
          else:
            for slot in object.material_slots[:]:
              if slot.material != None:
                if slot.material.users == 1:

                  # object type
                  if option.objectType in 'ALL':

                    # sort
                    sort(context, slot.material)

                  # object type
                  elif option.objectType in object.type:

                    # sort
                    sort(context, slot.material)
                else:

                  # shared
                  if slot.material not in shared.materials[:]:
                    shared.materials.append(slot.material)

                    # sort
                    sort(context, slot.material)

        # clear shared
        shared.materials.clear()

        # process
        process(context, storage.batch.materials)

        # clear collection
        storage.batch.materials.clear()

      # textures
      if option.textures:
        for object in bpy.data.objects[:]:
          if context.scene.render.engine not in 'CYCLES':

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:
                for slot in object.material_slots[:]:
                  if slot.material != None:
                    if slot.material.users == 1:
                      for texslot in slot.material.texture_slots[:]:
                        if texslot != None:
                          if texslot.texture.users == 1:

                            # object type
                            if option.objectType in 'ALL':

                              # sort
                              sort(context, texslot.texture)

                            # object type
                            elif option.objectType in object.type:

                              # sort
                              sort(context, texslot.texture)
                          else:

                            # shared
                            if texslot.texture not in shared.textures[:]:
                              shared.textures.append(texslot.texture)

                              # sort
                              sort(context, texslot.texture)
                    else:

                      # shared
                      if slot.material not in shared.materials[:]:
                        shared.materials.append(slot.material)
                        for texslot in slot.material.texture_slots[:]:
                          if texslot != None:
                            if texslot.texture.users == 1:

                              # object type
                              if option.objectType in 'ALL':

                                # sort
                                sort(context, texslot.texture)

                              # object type
                              elif option.objectType in object.type:

                                # sort
                                sort(context, texslot.texture)
                            else:

                              # shared
                              if texslot.texture not in shared.textures[:]:
                                shared.textures.append(texslot.texture)

                                # sort
                                sort(context, texslot.texture)

            # batch type
            else:
              for slot in object.material_slots[:]:
                if slot.material != None:
                  if slot.material.users == 1:
                    for texslot in slot.material.texture_slots[:]:
                      if texslot != None:
                        if texslot.texture.users == 1:

                          # object type
                          if option.objectType in 'ALL':

                            # sort
                            sort(context, texslot.texture)

                          # object type
                          elif option.objectType in object.type:

                            # sort
                            sort(context, texslot.texture)
                        else:

                          # shared
                          if texslot.texture not in shared.textures[:]:
                            shared.textures.append(texslot.texture)

                            # sort
                            sort(context, texslot.texture)
                  else:

                    # shared
                    if slot.material not in shared.materials[:]:
                      shared.materials.append(slot.material)
                      for texslot in slot.material.texture_slots[:]:
                        if texslot != None:
                          if texslot.texture.users == 1:

                            # object type
                            if option.objectType in 'ALL':

                              # sort
                              sort(context, texslot.texture)

                            # object type
                            elif option.objectType in object.type:

                              # sort
                              sort(context, texslot.texture)
                          else:

                            # shared
                            if texslot.texture not in shared.textures[:]:
                              shared.textures.append(texslot.texture)

                              # sort
                              sort(context, texslot.texture)

        # clear shared
        shared.textures.clear()

        # process
        process(context, storage.batch.textures)

        # clear collection
        storage.batch.textures.clear()

      # particle systems
      if option.particleSystems:
        for object in bpy.data.objects[:]:
          if object.type in 'MESH':

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:
                for system in object.particle_systems[:]:

                  # object type
                  if option.objectType in 'ALL':

                    # sort
                    sort(context, system)

                  # object type
                  elif option.objectType in object.type:

                    # sort
                    sort(context, system)

            # batch type
            else:
              for system in object.particle_systems[:]:

                # object type
                if option.objectType in 'ALL':

                  # sort
                  sort(context, system)

                # object type
                elif option.objectType in object.type:

                  # sort
                  sort(context, system)

            # process
            process(context, storage.batch.particleSystems)

            # clear collection
            storage.batch.particleSystems.clear()

      # particle settings
      if option.particleSettings:
        for object in bpy.data.objects[:]:
          if object.type in 'MESH':

            # batch type
            if option.batchType in 'SELECTED':
              if object.select:
                for system in object.particle_systems[:]:

                  # object type
                  if option.objectType in 'ALL':
                    if system.settings.users == 1:

                      # sort
                      sort(context, system.settings)
                    else:

                      # shared
                      if system.settings not in shared.particleSettings[:]:
                        shared.particleSettings.append(system.settings)

                        # sort
                        sort(context, system.settings)

                  # object type
                  elif option.objectType in object.type:
                    if system.settings.users == 1:

                      # sort
                      sort(context, system.settings)
                    else:

                      # shared
                      if system.settings not in shared.particleSettings[:]:
                        shared.particleSettings.append(system.settings)

                        # sort
                        sort(context, system.settings)

            # batch type
            else:
              for system in object.particle_systems[:]:

                # object type
                if option.objectType in 'ALL':
                  if system.settings.users == 1:

                    # sort
                    sort(context, system.settings)
                  else:

                    # shared
                    if system.settings not in shared.particleSettings[:]:
                      shared.particleSettings.append(system.settings)

                      # sort
                      sort(context, system.settings)

                # object type
                elif option.objectType in object.type:
                  if system.settings.users == 1:

                    # sort
                    sort(context, system.settings)
                  else:

                    # shared
                    if system.settings not in shared.particleSettings[:]:
                      shared.particleSettings.append(system.settings)

                      # sort
                      sort(context, system.settings)

        # clear shared
        shared.particleSettings.clear()

        # process
        process(context, storage.batch.particleSettings)

        # clear collection
        storage.batch.particleSettings.clear()

    # sensors
    if option.sensors:
      for object in bpy.data.objects[:]:

        # batch type
        if option.batchType in 'SELECTED':
          if object.select:

            # object type
            if option.objectType in 'ALL':

              # sort
              for sensor in object.game.sensors[:]:
                sort(context, sensor)

            # object type
            elif option.objectType in object.type:

              # sort
              for sensor in object.game.sensors[:]:
                sort(context, sensor)

        # batch type
        else:

          # object type
          if option.objectType in 'ALL':

            # sort
            for sensor in object.game.sensors[:]:
              sort(context, sensor)

          # object type
          elif option.objectType in object.type:

            # sort
            for sensor in object.game.sensors[:]:
              sort(context, sensor)

        # process
        process(context, storage.batch.sensors)

        # clear collection
        storage.batch.sensors.clear()

    # controllers
    if option.controllers:
      for object in bpy.data.objects[:]:

        # batch type
        if option.batchType in 'SELECTED':
          if object.select:

            # object type
            if option.objectType in 'ALL':

              # sort
              for controller in object.game.controllers[:]:
                sort(context, controller)

            # object type
            elif option.objectType in object.type:

              # sort
              for controller in object.game.controllers[:]:
                sort(context, controller)

        # batch type
        else:

          # object type
          if option.objectType in 'ALL':

            # sort
            for controller in object.game.controllers[:]:
              sort(context, controller)

          # object type
          elif option.objectType in object.type:

            # sort
            for controller in object.game.controllers[:]:
              sort(context, controller)

        # process
        process(context, storage.batch.controllers)

        # clear collection
        storage.batch.controllers.clear()

    # actuators
    if option.actuators:
      for object in bpy.data.objects[:]:

        # batch type
        if option.batchType in 'SELECTED':
          if object.select:

            # object type
            if option.objectType in 'ALL':

              # sort
              for actuator in object.game.actuators[:]:
                sort(context, actuator)

            # object type
            elif option.objectType in object.type:

              # sort
              for actuator in object.game.actuators[:]:
                sort(context, actuator)

        # batch type
        else:

          # object type
          if option.objectType in 'ALL':

            # sort
            for actuator in object.game.actuators[:]:
              sort(context, actuator)

          # object type
          elif option.objectType in object.type:

            # sort
            for actuator in object.game.actuators[:]:
              sort(context, actuator)

        # process
        process(context, storage.batch.actuators)

        # clear collection
        storage.batch.actuators.clear()

    # batch type
    if option.batchType in 'SCENE':

      # actions
      if option.actions:
        for object in context.scene.objects[:]:
          if hasattr(object.animation_data, 'action'):
            if hasattr(object.animation_data.action, 'name'):

              # object type
              if option.objectType in 'ALL':

                # sort
                sort(context, object.animation_data.action)

              # object type
              elif option.objectType in object.type:

                # sort
                sort(context, object.animation_data.action)

        # clear duplicates
        actions = []
        [actions.append(item) for item in storage.batch.actions if item not in actions]
        storage.batch.actions.clear()

        # process
        process(context, actions)

      # action groups
      if option.actionGroups:
        for object in context.scene.objects[:]:
          if hasattr(object.animation_data, 'action'):
            if hasattr(object.animation_data.action, 'name'):

              # object type
              if option.objectType in 'ALL':

                # sort
                sort(context, object.animation_data.action)

              # object type
              elif option.objectType in object.type:

                # sort
                sort(context, object.animation_data.action)

        # clear duplicates
        actions = []
        [actions.append(item) for item in storage.batch.actions if item not in actions]
        storage.batch.actions.clear()

        # name action groups
        for action in actions:
          for group in action[1][1].groups:
            group.name = name(context, group.name) if not option.suffixLast else name(context, group.name) + option.suffix

      # grease pencil
      if option.greasePencil:
        for object in context.scene.objects[:]:
          if hasattr(object.grease_pencil, 'name'):

            # object type
            if option.objectType in 'ALL':
              if object.grease_pencil.users == 1:

                # sort
                sort(context, object.grease_pencil)

              else:

                # shared
                if object.grease_pencil not in shared.greasePencils[:]:
                  shared.greasePencils.append(object.grease_pencil)

                  # sort
                  sort(context, object.grease_pencil)

            # object type
            elif option.objectType in object.type:
              if object.grease_pencil.users == 1:

                # sort
                sort(context, object.grease_pencil)

              else:

                # shared
                if object.grease_pencil not in shared.greasePencils[:]:
                  shared.greasePencils.append(object.grease_pencil)

                  # sort
                  sort(context, object.grease_pencil)

        # clear shared
        shared.greasePencils.clear()

        # process
        process(context, storage.batch.greasePencils)

        # clear collection
        storage.batch.greasePencils.clear()

      # pencil layers
      if option.pencilLayers:
        for object in context.scene.objects[:]:
          if hasattr(object.grease_pencil, 'name'):

            # object type
            if option.objectType in 'ALL':
              if object.grease_pencil.users == 1:

                # layers
                for layer in object.grease_pencil.layers[:]:

                  # sort
                  sort(context, layer)
              else:

                # shared
                if object.grease_pencil not in shared.greasePencils[:]:
                  shared.greasePencils.append(object.grease_pencil)

                  # layers
                  for layer in object.grease_pencil.layers[:]:

                    # sort
                    sort(context, layer)

            # object type
            elif option.objectType in object.type:
              if object.grease_pencil.users == 1:

                # layers
                for layer in object.grease_pencil.layers[:]:

                  # sort
                  sort(context, layer)
              else:

                # shared
                if object.grease_pencil not in shared.greasePencils[:]:
                  shared.greasePencils.append(object.grease_pencil)

                  # layers
                  for layer in object.grease_pencil.layers[:]:

                    # sort
                    sort(context, layer)

            # process
            process(context, storage.batch.pencilLayers)

            # clear collection
            storage.batch.pencilLayers.clear()

        # clear shared
        shared.greasePencils.clear()

      # objects
      if option.objects:
        for object in context.scene.objects[:]:

          # object type
          if option.objectType in 'ALL':

            # sort
            sort(context, object)

          # object type
          elif option.objectType in object.type:

            # sort
            sort(context, object)

        # process
        process(context, storage.batch.objects)

        # clear collection
        storage.batch.objects.clear()

      # groups
      if option.groups:
        for object in context.scene.objects[:]:

          # object type
          if option.objectType in 'ALL':
            for group in bpy.data.groups[:]:
              if object in group.objects[:]:

                # sort
                sort(context, group)

          # object type
          elif option.objectType in object.type:
            for group in bpy.data.groups[:]:
              if object in group.objects[:]:

                # sort
                sort(context, group)

        # clear duplicates
        objectGroups = []
        [objectGroups.append(item) for item in storage.batch.groups if item not in objectGroups]
        storage.batch.groups.clear()

        # process
        process(context, objectGroups)

      # constraints
      if option.constraints:
        for object in context.scene.objects[:]:
          for constraint in object.constraints[:]:

            # constraint type
            if option.constraintType in 'ALL':

              # sort
              sort(context, constraint)

            # constraint type
            elif option.constraintType in constraint.type:

              # sort
              sort(context, constraint)

          # process
          process(context, storage.batch.constraints)

          # clear collection
          storage.batch.constraints.clear()

      # modifiers
      if option.modifiers:
        for object in context.scene.objects[:]:
          for modifier in object.modifiers[:]:

            # modifier type
            if option.modifierType in 'ALL':

              # sort
              sort(context, modifier)

            # modifier tye
            elif option.modifierType in modifier.type:

              # sort
              sort(context, modifier)

          # process
          process(context, storage.batch.modifiers)

          # clear collection
          storage.batch.modifiers.clear()

      # object data
      if option.objectData:
        for object in context.scene.objects[:]:
          if object.type not in 'EMPTY':

            # object type
            if option.objectType in 'ALL':
              if object.data.users == 1:

                # sort
                sort(context, object.data)
              else:

                # shared shared
                if object.data.name not in shared.objectData[:]:
                  shared.objectData.append(object.data.name)

                  # sort
                  sort(context, object.data)

            # object type
            elif option.objectType in object.type:
              if object.data.users == 1:

                # sort
                sort(context, object.data)
              else:

                # shared shared
                if object.data.name not in shared.objectData[:]:
                  shared.objectData.append(object.data.name)

                  # sort
                  sort(context, object.data)

        # clear shared
        shared.objectData.clear()

        # object data
        objectData = [
          storage.batch.curves,
          storage.batch.cameras,
          storage.batch.meshes,
          storage.batch.lamps,
          storage.batch.lattices,
          storage.batch.metaballs,
          storage.batch.speakers,
          storage.batch.armatures
        ]
        for collection in objectData:

          # process
          process(context, collection)

      # bone groups
      if option.boneGroups:
        for object in context.scene.objects[:]:
          if object.type in 'ARMATURE':
            for group in object.pose.bone_groups[:]:

              # sort
              sort(context, group)

          # process
          process(context, storage.batch.boneGroups)

          # clear collection
          storage.batch.boneGroups.clear()

      # bones
      if option.bones:
        for object in context.scene.objects[:]:
          if object.type in 'ARMATURE':

            # edit mode
            if object.mode in 'EDIT':
              for bone in bpy.data.armatures[object.data.name].edit_bones[:]:

                  # sort
                  sort(context, bone)

            # pose or object mode
            else:
              for bone in bpy.data.armatures[object.data.name].bones[:]:

                  # sort
                  sort(context, bone)

            # process
            process(context, storage.batch.bones)

            # clear collection
            storage.batch.bones.clear()

      # bone constraints
      if option.boneConstraints:
        for object in context.scene.objects[:]:
          if object.type in 'ARMATURE':
            for bone in object.pose.bones[:]:
              for constraint in bone.constraints[:]:

                # constraint type
                if option.constraintType in 'ALL':

                  # sort
                  sort(context, constraint)

                # constraint type
                elif option.constraintType in constraint.type:

                  # sort
                  sort(context, constraint)

              # process
              process(context, storage.batch.constraints)

              # clear collection
              storage.batch.constraints.clear()

      # vertex groups
      if option.vertexGroups:
        for object in context.scene.objects[:]:
          if hasattr(object, 'vertex_groups'):
            for group in object.vertex_groups[:]:

              # object type
              if option.objectType in 'ALL':

                # sort
                sort(context, group)

              # object type
              elif option.objectType in object.type:

                # sort
                sort(context, group)

            # process
            process(context, storage.batch.vertexGroups)

            # clear collection
            storage.batch.vertexGroups.clear()

      # shapekeys
      if option.shapekeys:
        for object in context.scene.objects[:]:
          if hasattr(object.data, 'shape_keys'):
            if hasattr(object.data.shape_keys, 'key_blocks'):
              for block in object.data.shape_keys.key_blocks[:]:

                # object type
                if option.objectType in 'ALL':

                  # sort
                  sort(context, block)

                # object type
                elif option.objectType in object.type:

                  # sort
                  sort(context, block)

              # process
              process(context, storage.batch.shapekeys)

              # clear collection
              storage.batch.shapekeys.clear()

      # uvs
      if option.uvs:
        for object in context.scene.objects[:]:
          if object.type in 'MESH':
            for uv in object.data.uv_textures[:]:

              # sort
              sort(context, uv)

            # process
            process(context, storage.batch.uvs)

            # clear collection
            storage.batch.uvs.clear()

      # vertex colors
      if option.vertexColors:
        for object in context.scene.objects[:]:
          if object.type in 'MESH':
            for color in object.data.vertex_colors[:]:

              # sort
              sort(context, color)

            # process
            process(context, storage.batch.vertexColors)

            # clear collection
            storage.batch.vertexColors.clear()

      # materials
      if option.materials:
        for object in context.scene.objects[:]:
          for slot in object.material_slots[:]:
            if slot.material != None:
              if slot.material.users == 1:

                # object type
                if option.objectType in 'ALL':

                  # sort
                  sort(context, slot.material)

                # object type
                elif option.objectType in object.type:

                  # sort
                  sort(context, slot.material)
              else:

                # shared
                if slot.material not in shared.materials[:]:
                  shared.materials.append(slot.material)

                  # sort
                  sort(context, slot.material)

        # clear shared
        shared.materials.clear()

        # process
        process(context, storage.batch.materials)

        # clear collection
        storage.batch.materials.clear()

      # textures
      if option.textures:
        for object in context.scene.objects[:]:
          if context.scene.render.engine not in 'CYCLES':
            for slot in object.material_slots[:]:
              if slot.material != None:
                if slot.material.users == 1:
                  for texslot in slot.material.texture_slots[:]:
                    if texslot != None:
                      if texslot.texture.users == 1:

                        # object type
                        if option.objectType in 'ALL':

                          # sort
                          sort(context, texslot.texture)

                        # object type
                        elif option.objectType in object.type:

                          # sort
                          sort(context, texslot.texture)
                      else:

                        # shared
                        if texslot.texture not in shared.textures[:]:
                          shared.textures.append(texslot.texture)

                          # sort
                          sort(context, texslot.texture)
                else:

                  # shared
                  if slot.material not in shared.materials[:]:
                    shared.materials.append(slot.material)
                    for texslot in slot.material.texture_slots[:]:
                      if texslot != None:
                        if texslot.texture.users == 1:

                          # object type
                          if option.objectType in 'ALL':

                            # sort
                            sort(context, texslot.texture)

                          # object type
                          elif option.objectType in object.type:

                            # sort
                            sort(context, texslot.texture)
                        else:

                          # shared
                          if texslot.texture not in shared.textures[:]:
                            shared.textures.append(texslot.texture)

                            # sort
                            sort(context, texslot.texture)

        # clear shared
        shared.textures.clear()

        # process
        process(context, storage.batch.textures)

        # clear collection
        storage.batch.textures.clear()

      # particle systems
      if option.particleSystems:
        for object in context.scene.objects[:]:
          if object.type in 'MESH':
            for system in object.particle_systems[:]:

              # object type
              if option.objectType in 'ALL':

                # sort
                sort(context, system)

              # object type
              elif option.objectType in object.type:

                # sort
                sort(context, system)

            # process
            process(context, storage.batch.particleSystems)

            # clear collection
            storage.batch.particleSystems.clear()

      # particle settings
      if option.particleSettings:
        for object in context.scene.objects[:]:
          if object.type in 'MESH':
            for system in object.particle_systems[:]:

              # object type
              if option.objectType in 'ALL':
                if system.settings.users == 1:

                  # sort
                  sort(context, system.settings)
                else:

                  # shared
                  if system.settings not in shared.particleSettings[:]:
                    shared.particleSettings.append(system.settings)

                    # sort
                    sort(context, system.settings)

              # object type
              elif option.objectType in object.type:
                if system.settings.users == 1:

                  # sort
                  sort(context, system.settings)
                else:

                  # shared
                  if system.settings not in shared.particleSettings[:]:
                    shared.particleSettings.append(system.settings)

                    # sort
                    sort(context, system.settings)

        # clear shared
        shared.particleSettings.clear()

        # process
        process(context, storage.batch.particleSettings)

        # clear collection
        storage.batch.particleSettings.clear()

      # sensors
      if option.sensors:
        for object in context.scene.objects[:]:

          # object type
          if option.objectType in 'ALL':

            # sort
            for sensor in object.game.sensors[:]:
              sort(context, sensor)

          # object type
          elif option.objectType in object.type:

            # sort
            for sensor in object.game.sensors[:]:
              sort(context, sensor)

          # process
          process(context, storage.batch.sensors)

          # clear collection
          storage.batch.sensors.clear()

      # controllers
      if option.controllers:
        for object in context.scene.objects[:]:

          # object type
          if option.objectType in 'ALL':

            # sort
            for controller in object.game.controllers[:]:
              sort(context, controller)

          # object type
          elif option.objectType in object.type:

            # sort
            for controller in object.game.controllers[:]:
              sort(context, controller)

          # process
          process(context, storage.batch.controllers)

          # clear collection
          storage.batch.controllers.clear()

      # actuators
      if option.actuators:
        for object in context.scene.objects[:]:

          # object type
          if option.objectType in 'ALL':

            # sort
            for actuator in object.game.actuators[:]:
              sort(context, actuator)

          # object type
          elif option.objectType in object.type:

            # sort
            for actuator in object.game.actuators[:]:
              sort(context, actuator)

          # process
          process(context, storage.batch.actuators)

          # clear collection
          storage.batch.actuators.clear()

    # batch type
    elif option.batchType in 'GLOBAL':

      # actions
      if option.actions:
        for action in bpy.data.actions[:]:

          # sort
          sort(context, action)

        # process
        process(context, storage.batch.actions)

        # clear collection
        storage.batch.actions.clear()

      # action groups
      if option.actionGroups:
        for action in bpy.data.actions[:]:

          # sort
          sort(context, action)

        # process
        for action in storage.batch.actions:
          for group in action[1][1].groups:
            group.name = name(context, group.name) if not option.suffixLast else name(context, group.name) + option.suffix

        # clear collection
        storage.batch.actions.clear()

      # grease pencil
      if option.greasePencil:
        for pencil in bpy.data.grease_pencil[:]:

          # sort
          sort(context, pencil)

        # process
        process(context, storage.batch.greasePencils)

        # clear collection
        storage.batch.greasePencils.clear()

      # pencil layers
      if option.pencilLayers:
        for pencil in bpy.data.grease_pencil[:]:

          # layers
          for layer in pencil.layers[:]:

            # sort
            sort(context, layer)

          # process
          process(context, storage.batch.pencilLayers)

          # clear collection
          storage.batch.pencilLayers.clear()

      # objects
      if option.objects:
        for object in bpy.data.objects[:]:

          # object type
          if option.objectType in 'ALL':

            # sort
            sort(context, object)

          # object type
          elif option.objectType in object.type:

            # sort
            sort(context, object)

        # process
        process(context, storage.batch.objects)

        # clear collection
        storage.batch.objects.clear()

      # groups
      if option.groups:
        for group in bpy.data.groups[:]:

          # sort
          sort(context, group)

        # process
        process(context, storage.batch.groups)

        # clear collection
        storage.batch.groups.clear()

      # constraints
      if option.constraints:
        for object in bpy.data.objects[:]:
          for constraint in object.constraints[:]:

            # object type
            if option.objectType in 'ALL':

              # constraint type
              if option.constraintType in 'ALL':

                # sort
                sort(context, constraint)

              # constraint type
              elif option.constraintType in constraint.type:

                # sort
                sort(context, constraint)

            # object type
            elif option.objectType in object.type:

              # constraint type
              if option.constraintType in 'ALL':

                # sort
                sort(context, constraint)

                # constraint type
              elif option.constraintType in constraint.type:

                # sort
                sort(context, constraint)

          # process
          process(context, storage.batch.constraints)

          # clear collection
          storage.batch.constraints.clear()

      # modifiers
      if option.modifiers:
        for object in bpy.data.objects[:]:
          for modifier in object.modifiers[:]:

            # object type
            if option.objectType in 'ALL':

              # modifier type
              if option.modifierType in 'ALL':

                # sort
                sort(context, modifier)

              # modifier type
              elif option.modifierType in modifier.type:

                # sort
                sort(context, modifier)

            # object type
            elif option.objectType in object.type:

              # modifier type
              if option.modifierType in 'ALL':

                # sort
                sort(context, modifier)

              # modifier type
              elif option.modifierType in modifier.type:

                # sort
                sort(context, modifier)

          # process
          process(context, storage.batch.modifiers)

          # clear collection
          storage.batch.modifiers.clear()

      # object data
      if option.objectData:

        # cameras
        for camera in bpy.data.cameras[:]:

          # sort
          sort(context, camera)

        # process
        process(context, storage.batch.cameras)

        # clear collection
        storage.batch.cameras.clear()

        # meshes
        for mesh in bpy.data.meshes[:]:

          # sort
          sort(context, mesh)

        # process
        process(context, storage.batch.meshes)

        # clear collection
        storage.batch.meshes.clear()

        # curves
        for curve in bpy.data.curves[:]:

          # sort
          sort(context, curve)

        # process
        process(context, storage.batch.curves)

        # clear collection
        storage.batch.curves.clear()

        # lamps
        for lamp in bpy.data.lamps[:]:

          # sort
          sort(context, lamp)

        # process
        process(context, storage.batch.lamps)

        # clear collection
        storage.batch.lamps.clear()

        # lattices
        for lattice in bpy.data.lattices[:]:

          # sort
          sort(context, lattice)

        # process
        process(context, storage.batch.lattices)

        # clear collection
        storage.batch.lattices.clear()

        # metaballs
        for metaball in bpy.data.metaballs[:]:

          # sort
          sort(context, metaball)

        # process
        process(context, storage.batch.metaballs)

        # clear collection
        storage.batch.metaballs.clear()

        # speakers
        for speaker in bpy.data.speakers[:]:

          # sort
          sort(context, speaker)

        # process
        process(context, storage.batch.speakers)

        # clear collection
        storage.batch.speakers.clear()

        # armatures
        for armature in bpy.data.armatures[:]:

          # sort
          sort(context, armature)

        # process
        process(context, storage.batch.armatures)

        # clear collection
        storage.batch.armatures.clear()

      # bone groups
      if option.boneGroups:
        for object in bpy.data.objects[:]:
          if object.type in 'ARMATURE':
            for group in object.pose.bone_groups[:]:

              # sort
              sort(context, group)

            # process
            process(context, storage.batch.boneGroups)

            # clear collection
            storage.batch.boneGroups.clear()

      # bones
      if option.bones:
        for armature in bpy.data.armatures[:]:
          for bone in armature.bones[:]:

            # sort
            sort(context, bone)

          # process
          process(context, storage.batch.bones)

          # clear collection
          storage.batch.bones.clear()

      # bone constraints
      if option.boneConstraints:
        for object in bpy.data.objects[:]:
          if object.type in 'ARMATURE':
            for bone in object.pose.bones[:]:
              for constraint in bone.constraints[:]:

                # sort
                sort(context, constraint)

              # process
              process(context, storage.batch.constraints)

              # clear collection
              storage.batch.constraints.clear()

      # vertex groups
      if option.vertexGroups:
        for object in bpy.data.objects[:]:
          if object.type in {'MESH', 'LATTICE'}:
            for group in object.vertex_groups[:]:

              # sort
              sort(context, group)

            # process
            process(context, storage.batch.vertexGroups)

            # clear collection
            storage.batch.vertexGroups.clear()

      # shape keys
      if option.shapekeys:
        for shapekey in bpy.data.shape_keys[:]:

            # sort
            sort(context, shapekey)
            for block in shapekey.key_blocks[:]:

              # sort
              sort(context, block)

            # process
            process(context, storage.batch.shapekeys)

            # clear collection
            storage.batch.shapekeys.clear()

      # uvs
      if option.uvs:
        for object in bpy.data.objects[:]:
          if object.type in 'MESH':
            for uv in object.data.uv_textures[:]:

              # sort
              sort(context, uv)

            # process
            process(context, storage.batch.uvs)

            # clear collection
            storage.batch.uvs.clear()

      # vertex colors
      if option.vertexColors:
        for object in bpy.data.objects[:]:
          if object.type in 'MESH':
            for color in object.data.vertex_colors[:]:

              # sort
              sort(context, color)

            # process
            process(context, storage.batch.vertexColors)

            # clear collection
            storage.batch.vertexColors.clear()

      # materials
      if option.materials:
        for material in bpy.data.materials[:]:

          # sort
          sort(context, material)

        # process
        process(context, storage.batch.materials)

        # clear collection
        storage.batch.materials.clear()

      # textures
      if option.textures:
        for texture in bpy.data.textures[:]:

          # sort
          sort(context, texture)

        # process
        process(context, storage.batch.textures)

        # clear collection
        storage.batch.textures.clear()

      # particles systems
      if option.particleSystems:
        for object in bpy.data.objects[:]:
          if object.type in 'MESH':
            for system in object.particle_systems[:]:

              # sort
              sort(context, system)

            # process
            process(context, storage.batch.particleSystems)

            # clear collection
            storage.batch.particleSystems.clear()

      # particles settings
      if option.particleSettings:
        for settings in bpy.data.particles[:]:

          # sort
          sort(context, settings)

        # process
        process(context, storage.batch.particleSettings)

        # clear collection
        storage.batch.particleSettings.clear()

      # sensors
      if option.sensors:
        for object in bpy.data.objects[:]:

          # object type
          if option.objectType in 'ALL':

            # sort
            for sensor in object.game.sensors[:]:
              sort(context, sensor)

          # object type
          elif option.objectType in object.type:

            # sort
            for sensor in object.game.sensors[:]:
              sort(context, sensor)

          # process
          process(context, storage.batch.sensors)

          # clear collection
          storage.batch.sensors.clear()

      # controllers
      if option.controllers:
        for object in bpy.data.objects[:]:

          # object type
          if option.objectType in 'ALL':

            # sort
            for controller in object.game.controllers[:]:
              sort(context, controller)

          # object type
          elif option.objectType in object.type:

            # sort
            for controller in object.game.controllers[:]:
              sort(context, controller)

          # process
          process(context, storage.batch.controllers)

          # clear collection
          storage.batch.controllers.clear()

      # actuators
      if option.actuators:
        for object in bpy.data.objects[:]:

          # object type
          if option.objectType in 'ALL':

            # sort
            for actuator in object.game.actuators[:]:
              sort(context, actuator)

          # object type
          elif option.objectType in object.type:

            # sort
            for actuator in object.game.actuators[:]:
              sort(context, actuator)

          # process
          process(context, storage.batch.actuators)

          # clear collection
          storage.batch.actuators.clear()

    # line sets
    if option.lineSets:
      for scene in bpy.data.scenes[:]:
        for layer in scene.render.layers[:]:
          for lineset in layer.freestyle_settings.linesets[:]:
            if hasattr(lineset, 'name'):
              lineset.name = name(context, lineset.name) if not option.suffixLast else name(context, lineset.name) + option.suffix

    # linestyles
    if option.linestyles:
      for style in bpy.data.linestyles[:]:

        # sort
        sort(context, style)

      # process
      process(context, storage.batch.linestyles)

      # clear collection
      storage.batch.linestyles.clear()

    # linestyle modifiers
    if option.linestyleModifiers:
      for style in bpy.data.linestyles[:]:


        # color
        for modifier in style.color_modifiers[:]:

          # linestyle modifier type
          if option.linestyleModifierType in 'ALL':

            # sort
            sort(context, modifier)

          # linestyle modifier type
          elif option.linestyleModifierType in modifier.type:

            # sort
            sort(context, modifier)

        # process
        process(context, storage.batch.modifiers)

        # clear storage
        storage.batch.modifiers.clear()


        # alpha
        for modifier in style.alpha_modifiers[:]:

          # linestyle modifier type
          if option.linestyleModifierType in 'ALL':

            # sort
            sort(context, modifier)

          # linestyle modifier type
          elif option.linestyleModifierType in modifier.type:

            # sort
            sort(context, modifier)

        # process
        process(context, storage.batch.modifiers)

        # clear storage
        storage.batch.modifiers.clear()


        # thickness
        for modifier in style.thickness_modifiers[:]:

          # linestyle modifier type
          if option.linestyleModifierType in 'ALL':

            # sort
            sort(context, modifier)

          # linestyle modifier type
          elif option.linestyleModifierType in modifier.type:

            # sort
            sort(context, modifier)

        # process
        process(context, storage.batch.modifiers)

        # clear storage
        storage.batch.modifiers.clear()


        # geometry
        for modifier in style.geometry_modifiers[:]:

          # linestyle modifier type
          if option.linestyleModifierType in 'ALL':

            # sort
            sort(context, modifier)

          # linestyle modifier type
          elif option.linestyleModifierType in modifier.type:

            # sort
            sort(context, modifier)

        # process
        process(context, storage.batch.modifiers)

        # clear storage
        storage.batch.modifiers.clear()

    # scenes
    if option.scenes:
      for scene in bpy.data.scenes[:]:

        # sort
        sort(context, scene)

      # process
      process(context, storage.batch.scenes)

      # clear collection
      storage.batch.scenes.clear()

    # render layers
    if option.renderLayers:
      for scene in bpy.data.scenes[:]:
        for layer in scene.render.layers[:]:

          # sort
          sort(context, layer)

        # process
        process(context, storage.batch.renderLayers)

        # clear collection
        storage.batch.renderLayers.clear()

    # worlds
    if option.worlds:
      for world in bpy.data.worlds[:]:

        # sort
        sort(context, world)

      # process
      process(context, storage.batch.worlds)

      # clear collection
      storage.batch.worlds.clear()

    # libraries
    if option.libraries:
      for library in bpy.data.libraries[:]:

        # sort
        sort(context, library)

      # process
      process(context, storage.batch.libraries)

      # clear collection
      storage.batch.libraries.clear()

    # images
    if option.images:
      for image in bpy.data.images[:]:

        # sort
        sort(context, image)

      # process
      process(context, storage.batch.images)

      # clear collection
      storage.batch.images.clear()

    # masks
    if option.masks:
      for mask in bpy.data.masks[:]:

        # sort
        sort(context, mask)

      # process
      process(context, storage.batch.masks)

      # clear collection
      storage.batch.masks.clear()

    # sequences
    if option.sequences:
      for scene in bpy.data.scenes[:]:
        if hasattr(scene.sequence_editor, 'sequence_all'):
          for sequence in scene.sequence_editor.sequences_all[:]:

            # sort
            sort(context, sequence)

          # process
          process(context, storage.batch.sequences)

          # clear collection
          storage.batch.sequences.clear()

    # movie clips
    if option.movieClips:
      for clip in bpy.data.movieclips[:]:

        # sort
        sort(context, clip)

      # process
      process(context, storage.batch.movieClips)

      # clear collection
      storage.batch.movieClips.clear()

    # sounds
    if option.sounds:
      for sound in bpy.data.sounds[:]:

        # sort
        sort(context, sound)

      # process
      process(context, storage.batch.sounds)

      # clear collection
      storage.batch.sounds.clear()

    # screens
    if option.screens:
      for screen in bpy.data.screens[:]:

        # sort
        sort(context, screen)

      # process
      process(context, storage.batch.screens)

      # clear collection
      storage.batch.screens.clear()

    # keying sets
    if option.keyingSets:
      for scene in bpy.data.scenes[:]:
        for keyingSet in scene.keying_sets[:]:

          # sort
          sort(context, keyingSet)

        # process
        process(context, storage.batch.keyingSets)

        # clear collection
        storage.batch.keyingSets.clear()

    # palettes
    if option.palettes:
      for palette in bpy.data.palettes[:]:

        # sort
        sort(context, palette)

      # process
      process(context, storage.batch.palettes)

      # clear collection
      storage.batch.palettes.clear()

    # brushes
    if option.brushes:
      for brush in bpy.data.brushes[:]:

        # sort
        sort(context, brush)

      # process
      process(context, storage.batch.brushes)

      # clear collection
      storage.batch.brushes.clear()

    # nodes
    if option.nodes:

      # shader
      for material in bpy.data.materials[:]:
        if hasattr(material.node_tree, 'nodes'):
          for node in material.node_tree.nodes[:]:

            # sort
            sort(context, node)

          # process
          process(context, storage.batch.nodes)

          # clear collection
          storage.batch.nodes.clear()

      # compositing
      for scene in bpy.data.scenes[:]:
        if hasattr(scene.node_tree, 'nodes'):
          for node in scene.node_tree.nodes[:]:

            # sort
            sort(context, node)

          # process
          process(context, storage.batch.nodes)

          # clear collection
          storage.batch.nodes.clear()

      # texture
      for texture in bpy.data.textures[:]:
        if hasattr(texture.node_tree, 'nodes'):
          for node in texture.node_tree.nodes[:]:

            # sort
            sort(context, node)

          # process
          process(context, storage.batch.nodes)

          # clear collection
          storage.batch.nodes.clear()

      # groups
      for group in bpy.data.node_groups[:]:
        for node in group.nodes[:]:

          # sort
          sort(context, node)

        # process
        process(context, storage.batch.nodes)

        # clear collection
        storage.batch.nodes.clear()

    # node labels
    if option.nodeLabels:

      # batch tag
      tag = True

      # shader
      for material in bpy.data.materials[:]:
        if hasattr(material.node_tree, 'nodes'):
          for node in material.node_tree.nodes[:]:

            # sort
            sort(context, node)

          # process
          process(context, storage.batch.nodeLabels)

          # clear collection
          storage.batch.nodeLabels.clear()

      # compositing
      for scene in bpy.data.scenes[:]:
        if hasattr(scene.node_tree, 'nodes'):
          for node in scene.node_tree.nodes[:]:

            # sort
            sort(context, node)

          # process
          process(context, storage.batch.nodeLabels)

          # clear collection
          storage.batch.nodeLabels.clear()

      # texture
      for texture in bpy.data.textures[:]:
        if hasattr(texture.node_tree, 'nodes'):
          for node in texture.node_tree.nodes[:]:

            # sort
            sort(context, node)

          # process
          process(context, storage.batch.nodeLabels)

          # clear collection
          storage.batch.nodeLabels.clear()

      # groups
      for group in bpy.data.node_groups[:]:
        for node in group.nodes[:]:

          # sort
          sort(context, node)

        # process
        process(context, storage.batch.nodeLabels)

        # clear collection
        storage.batch.nodeLabels.clear()

      # batch tag
      tag = False

    # node groups
    if option.nodeGroups:
      for group in bpy.data.node_groups[:]:

        # sort
        sort(context, group)

      # process
      process(context, storage.batch.nodeGroups)

      # clear collection
      storage.batch.nodeGroups.clear()

    # texts
    if option.texts:
      for text in bpy.data.texts[:]:

        # sort
        sort(context, text)

      # process
      process(context, storage.batch.texts)

      # clear collection
      storage.batch.texts.clear()

# quick
def quick(context, object, panel, option):
  '''
    Quick batch mode for main.
  '''

  # search
  search = panel.search if panel.regex else re.escape(panel.search)

  # search
  if search == '' or re.search(search, object.name, re.I):

    # ignore Object
    if not option.ignoreObject:

      # storage
      storage.batch.objects.append([object.name, [1, object]])

  # action
  if panel.action:

    # ignore action
    if not option.ignoreAction:
      if hasattr(object.animation_data, 'action'):
        if hasattr(object.animation_data.action, 'name'):

          # search
          if search == '' or re.search(search, object.animation_data.action.name, re.I):

            # name
            object.animation_data.action.name = name(context, object.animation_data.action.name) if not option.suffixLast else name(object.animation_data.action.name) + option.suffix

  # grease pencils
  if panel.greasePencil:

    # ignore grease pencil
    if not option.ignoreGreasePencil:
      if hasattr(object.grease_pencil, 'name'):

        # search
        if search == '' or re.search(search, object.grease_pencil.name, re.I):

          # name
          object.grease_pencil.name = name(context, object.grease_pencil.name) if not option.suffixLast else name(context, object.grease_pencil.name) + option.suffix

        # layers
        for layer in object.grease_pencil.layers[:]:

          # search
          if search == '' or re.search(search, layer.info, re.I):

            # append
            storage.batch.pencilLayers.append([layer.info, [1, layer]])

        # process
        process(context, storage.batch.pencilLayers)

        # clear
        storage.batch.pencilLayers.clear()

  # groups
  if panel.groups:

    # ignore group
    if not option.ignoreGroup:
      for group in bpy.data.groups[:]:
        for groupObject in group.objects[:]:
          if groupObject == object:

            # search
            if search == '' or re.search(search, group.name, re.I):

              # name
              group.name = name(context, group.name) if not option.suffixLast else name(context, group.name) + option.suffix

  # constraints
  if panel.constraints:

    # ignore constraint
    if not option.ignoreConstraint:
      for constraint in object.constraints[:]:

        # search
        if search == '' or re.search(search, constraint.name, re.I):

          # append
          storage.batch.constraints.append([constraint.name, [1, constraint]])

      # process
      process(context, storage.batch.constraints)

      # clear
      storage.batch.constraints.clear()

  # modifiers
  if panel.modifiers:

    # ignore modifier
    if not option.ignoreModifier:
      for modifier in object.modifiers[:]:

        # search
        if search == '' or re.search(search, modifier.name, re.I):

          # append
          storage.batch.modifiers.append([modifier.name, [1, modifier]])

      # process
      process(context, storage.batch.modifiers)

      # clear
      storage.batch.modifiers.clear()

  # bone groups
  if panel.boneGroups:

    # ignore bone group
    if not option.ignoreBoneGroup:
      if object.type in 'ARMATURE':
        for group in object.pose.bone_groups[:]:

          # search
          if search == '' or re.search(search, group.name, re.I):

            # sort
            storage.batch.boneGroups.append([group.name, [1, group]])

        # process
        process(context, storage.batch.boneGroups)

        # clear
        storage.batch.boneGroups.clear()

  # bones
  if object == context.active_object:

    # ignore bone
    if not option.ignoreBone:
      if object.type == 'ARMATURE':
        if object.mode in {'POSE', 'EDIT'}:

          # display bones
          if panel.displayBones:

            # bone mode
            if panel.boneMode == 'SELECTED':

              # pose
              if object.mode == 'POSE':

                # bones
                bones = context.selected_pose_bones[:]

              # edit
              elif object.mode == 'EDIT':

                # bones
                bones = context.selected_bones[:]

              # bone
              for bone in bones:

                # search
                if search == '' or re.search(search, bone.name, re.I):

                  # append
                  storage.batch.bones.append([bone.name, [1, bone]])

              # process
              process(context, storage.batch.bones)

              # clear
              storage.batch.bones.clear()

            # bone mode
            else:

              # pose
              if object.mode == 'POSE':

                # bones
                bones = [bone for bone in object.data.bones if True in [x&y for (x, y) in zip(bone.layers, object.data.layers)]]

                # edit
              elif object.mode == 'EDIT':

                # bones
                bones = [bone for bone in object.data.edit_bones if True in [x&y for (x, y) in zip(bone.layers, object.data.layers)]]

              # bone
              for bone in bones:

                # search
                if search == '' or re.search(search, bone.name, re.I):

                  # append
                  storage.batch.bones.append([bone.name, [1, bone]])

              # process
              process(context, storage.batch.bones)

              # clear
              storage.batch.bones.clear()

          # display bones
          else:

            # mode
            if object.mode == 'EDIT':

              # search
              if search == '' or re.search(search, context.active_bone, re.I):

                # name
                context.active_bone.name = name(context, context.active_bone.name) if option.suffixLast else name(context, context.active_bone.name) + option.suffix

            # mode
            elif object.mode == 'POSE':

              # search
              if search == '' or re.search(search, context.active_pose_bone, re.I):

                # name
                context.active_pose_bone.name = name(context, context.active_pose_bone.name) if option.suffixLast else name(context, context.active_pose_bone.name) + option.suffix

    # bone constraints
    if panel.boneConstraints:

      # ignore bone constraint
      if not option.ignoreBoneConstraint:
        if object.mode == 'POSE':

          # display bones
          if panel.displayBones:

            # bone mode
            if panel.boneMode == 'SELECTED':
              for bone in context.selected_pose_bones[:]:
                for constraint in bone.constraints[:]:

                  # search
                  if search == '' or re.search(search, constraint.name, re.I):

                    # append
                    storage.batch.constraints.append([constraint.name, [1, constraint]])

                # process
                process(context, storage.batch.constraints)

                # clear
                storage.batch.constraints.clear()

            # bone mode
            else:
              for bone in object.pose.bones[:]:
                if True in [x&y for (x, y) in zip(bone.bone.layers, object.data.layers)]:
                  for constraint in bone.constraints[:]:

                    # search
                    if search == '' or re.search(search, constraint.name, re.I):

                      # append
                      storage.batch.constraints.append([constraint.name, [1, constraint]])

                  # process
                  process(context, storage.batch.constraints)

                  # clear
                  storage.batch.constraints.clear()

          # display bones
          else:
            for constraint in context.active_pose_bone.constraints[:]:

              # search
              if search == '' or re.search(search, constraint.name, re.I):

                # append
                storage.batch.constraints.append([constraint.name, [1, constraint]])

            # process
            process(context, storage.batch.constraints)

            # clear
            storage.batch.constraints.clear()

  # object data
  if object.type != 'EMPTY':

    # ignore object data
    if not option.ignoreObjectData:

      # search
      if search == '' or re.search(search, object.data.name, re.I):

        # cameras
        if object.data.rna_type.identifier == 'Camera':
          storage.batch.cameras.append([object.data.name, [1, object.data]])

        # meshes
        if object.data.rna_type.identifier == 'Mesh':
          storage.batch.meshes.append([object.data.name, [1, object.data]])

        # curves
        if object.data.rna_type.identifier in {'SurfaceCurve', 'TextCurve', 'Curve'}:
          storage.batch.curves.append([object.data.name, [1, object.data]])

        # lamps
        if hasattr(object.data.rna_type.base, 'identifier'):
          if object.data.rna_type.base.identifier == 'Lamp':
            storage.batch.lamps.append([object.data.name, [1, object.data]])

        # lattices
        if object.data.rna_type.identifier == 'Lattice':
          storage.batch.lattices.append([object.data.name, [1, object.data]])

        # metaballs
        if object.data.rna_type.identifier == 'MetaBall':
          storage.batch.metaballs.append([object.data.name, [1, object.data]])

        # speakers
        if object.data.rna_type.identifier == 'Speaker':
          storage.batch.speakers.append([object.data.name, [1, object.data]])

        # armatures
        if object.data.rna_type.identifier == 'Armature':
          storage.batch.armatures.append([object.data.name, [1, object.data]])

  # vertex groups
  if panel.vertexGroups:

    # ignore vertex group
    if not option.ignoreVertexGroup:
      if hasattr(object, 'vertex_groups'):
        for group in object.vertex_groups[:]:

          # search
          if search == '' or re.search(search, group.name, re.I):

            # sort
            storage.batch.vertexGroups.append([group.name, [1, group]])

        # process
        process(context, storage.batch.vertexGroups)

        # clear
        storage.batch.vertexGroups.clear()

  # shapekeys
  if panel.shapekeys:

    # ignore shapekey
    if not option.ignoreShapekey:
      if hasattr(object.data, 'shape_keys'):
        if hasattr(object.data.shape_keys, 'key_blocks'):
          for key in object.data.shape_keys.key_blocks[:]:

            # search
            if search == '' or re.search(search, key.name, re.I):

              # sort
              storage.batch.shapekeys.append([key.name, [1, key]])

          # process
          process(context, storage.batch.shapekeys)

          # clear
          storage.batch.shapekeys.clear()

  # uv maps
  if panel.uvs:

    # ignore uv
    if not option.ignoreUV:
      if object.type in 'MESH':
        for uv in object.data.uv_textures[:]:

          # search
          if search == '' or re.search(search, uv.name, re.I):

            # append
            storage.batch.uvs.append([uv.name, [1, uv]])

        # process
        process(context, storage.batch.uvs)

        # clear
        storage.batch.uvs.clear()

  # vertex colors
  if panel.vertexColors:

    # ignore vertex color
    if not option.ignoreVertexColor:
      if object.type in 'MESH':
        for vertexColor in object.data.vertex_colors[:]:

          # search
          if search == '' or re.search(search, vertexColor.name, re.I):

            # append
            storage.batch.vertexColors.append([vertexColor.name, [1, vertexColor]])

        # process
        process(context, storage.batch.vertexColors)

        # clear
        storage.batch.vertexColors.clear()

  # materials
  if panel.materials:

    # ignore material
    if not option.ignoreMaterial:
      for slot in object.material_slots:
        if slot.material != None:

          # search
          if search == '' or re.search(search, slot.material.name, re.I):

            # append
            storage.batch.materials.append([slot.material.name, [1, slot.material]])

      # process
      process(context, storage.batch.materials)

      # clear
      storage.batch.materials.clear()

  # textures
  if panel.textures:

    # ignore texture
    if not option.ignoreTexture:

      # material textures
      for slot in object.material_slots:
        if slot.material != None:
          if context.scene.render.engine in {'BLENDER_RENDER', 'BLENDER_GAME'}:
            for tslot in slot.material.texture_slots[:]:
              if hasattr(tslot, 'texture'):
                if tslot.texture != None:

                  # search
                  if search == '' or re.search(search, tslot.texture.name, re.I):

                    # append
                    storage.batch.textures.append([tslot.texture.name, [1, tslot.texture]])

            # process
            process(context, storage.batch.textures)

            # clear
            storage.batch.textures.clear()

      # particle system textures
      if panel.particleSystems:
        for modifier in object.modifiers[:]:
          if modifier.type == 'PARTICLE_SYSTEM':
            for slot in modifier.particle_system.settings.texture_slots[:]:
              if hasattr(slot, 'texture'):
                if slot.texture != None:

                  # search
                  if search == '' or re.search(search, slot.texture.name, re.I):

                    # append
                    storage.batch.textures.append([slot.texture.name, [1, slot.texture]])

            # process
            process(context, storage.batch.textures)

            # clear
            storage.batch.textures.clear()

      # modifier textures
      if panel.modifiers:
        for modifier in object.modifiers[:]:

          # texture
          if modifier.type in {'DISPLACE', 'WARP'}:
            if modifier.texture:

              # search
              if search == '' or re.search(search, modifier.texture.name, re.I):

                # append
                storage.batch.textures.append([modifier.texture.name, [1, modifier.texture]])

          # mask texture
          elif modifier.type in {'VERTEX_WEIGHT_MIX', 'VERTEX_WEIGHT_EDIT', 'VERTEX_WEIGHT_PROXIMITY'}:
            if modifier.mask_texture:

              # search
              if search == '' or re.search(search, modifier.mask_texture.name, re.I):

                # append
                storage.batch.textures.append([modifier.mask_texture.name, [1, modifier.mask_texture]])

        # process
        process(context, storage.batch.textures)

        # clear
        storage.batch.textures.clear()

  # particle systems
  if panel.particleSystems:

    # ignore particle system
    if not option.ignoreParticleSystem:
      for modifier in object.modifiers[:]:
        if modifier.type in 'PARTICLE_SYSTEM':

          # search
          if search == '' or re.search(search, modifier.particle_system.name, re.I):

            # append
            storage.batch.particleSystems.append([modifier.particle_system.name, [1, modifier.particle_system]])

      # process
      process(context, storage.batch.particleSystems)

      # clear
      storage.batch.particleSystems.clear()

  # particle settings
  if panel.particleSystems:

    # ignore particle setting
    if not option.ignoreParticleSetting:
      for modifier in object.modifiers[:]:
        if modifier.type in 'PARTICLE_SYSTEM':

          # search
          if search == '' or re.search(search, modifier.particle_system.settings.name, re.I):

            # append
            storage.batch.particleSettings.append([modifier.particle_system.settings.name, [1, modifier.particle_system.settings]])

      # process
      process(context, storage.batch.particleSettings)

      # clear
      storage.batch.particleSettings.clear()

# sort
def sort(context, datablock):
  '''
    Sort datablocks into proper storage list.
  '''

  # tag
  global tag

  # option
  option = context.scene.BatchName

  # objects
  if option.objects:
    if datablock.rna_type.identifier == 'Object':
      storage.batch.objects.append([datablock.name, [1, datablock]])

  # groups
  if option.groups:
    if datablock.rna_type.identifier == 'Group':
      storage.batch.groups.append([datablock.name, [1, datablock]])

  # actions
  if option.actions or option.actionGroups:
    if datablock.rna_type.identifier == 'Action':
      storage.batch.actions.append([datablock.name, [1, datablock]])

  # grease pencils
  if option.greasePencil:
    if datablock.rna_type.identifier == 'GreasePencil':
      storage.batch.greasePencils.append([datablock.name, [1, datablock]])

  # pencil layers
  if option.pencilLayers:
    if datablock.rna_type.identifier == 'GPencilLayer':
      storage.batch.pencilLayers.append([datablock.info, [1, datablock]])

  # constraints
  if option.constraints or option.boneConstraints:
    if hasattr(datablock.rna_type.base, 'identifier'):
      if datablock.rna_type.base.identifier == 'Constraint':
        storage.batch.constraints.append([datablock.name, [1, datablock]])

  # modifiers
  if option.modifiers:
    if hasattr(datablock.rna_type.base, 'identifier'):
      if datablock.rna_type.base.identifier in 'Modifier':
        storage.batch.modifiers.append([datablock.name, [1, datablock]])

  # object data
  if option.objectData:

    # cameras
    if datablock.rna_type.identifier == 'Camera':
      storage.batch.cameras.append([datablock.name, [1, datablock]])

    # meshes
    if datablock.rna_type.identifier == 'Mesh':
      storage.batch.meshes.append([datablock.name, [1, datablock]])

    # curves
    if datablock.rna_type.identifier in {'SurfaceCurve', 'TextCurve', 'Curve'}:
      storage.batch.curves.append([datablock.name, [1, datablock]])

    # lamps
    if hasattr(datablock.rna_type.base, 'identifier'):
      if datablock.rna_type.base.identifier == 'Lamp':
        storage.batch.lamps.append([datablock.name, [1, datablock]])

    # lattices
    if datablock.rna_type.identifier == 'Lattice':
      storage.batch.lattices.append([datablock.name, [1, datablock]])

    # metaballs
    if datablock.rna_type.identifier == 'MetaBall':
      storage.batch.metaballs.append([datablock.name, [1, datablock]])

    # speakers
    if datablock.rna_type.identifier == 'Speaker':
      storage.batch.speakers.append([datablock.name, [1, datablock]])

    # armatures
    if datablock.rna_type.identifier == 'Armature':
      storage.batch.armatures.append([datablock.name, [1, datablock]])

  # bones
  if option.bones:
    if datablock.rna_type.identifier in {'PoseBone', 'EditBone', 'Bone'}:
      storage.batch.bones.append([datablock.name, [1, datablock]])

  # vertex groups
  if option.vertexGroups:
    if datablock.rna_type.identifier == 'VertexGroup':
      storage.batch.vertexGroups.append([datablock.name, [1, datablock]])

  # shapekeys
  if option.shapekeys:
    if datablock.rna_type.identifier == 'ShapeKey':
      storage.batch.shapekeys.append([datablock.name, [1, datablock]])

  # uvs
  if option.uvs:
    if datablock.rna_type.identifier == 'MeshTexturePolyLayer':
      storage.batch.uvs.append([datablock.name, [1, datablock]])

  # vertex colors
  if option.vertexColors:
    if datablock.rna_type.identifier == 'MeshLoopColorLayer':
      storage.batch.vertexColors.append([datablock.name, [1, datablock]])

  # materials
  if option.materials:
    if datablock.rna_type.identifier == 'Material':
      storage.batch.materials.append([datablock.name, [1, datablock]])

  # textures
  if option.textures:
    if hasattr(datablock.rna_type.base, 'identifier'):
      if datablock.rna_type.base.identifier == 'Texture':
        storage.batch.textures.append([datablock.name, [1, datablock]])

  # particle systems
  if option.particleSystems:
    if datablock.rna_type.identifier == 'ParticleSystem':
      storage.batch.particleSystems.append([datablock.name, [1, datablock]])

  # particle settings
  if option.particleSettings:
    if datablock.rna_type.identifier == 'ParticleSettings':
      storage.batch.particleSettings.append([datablock.name, [1, datablock]])

  # line style
  if option.linestyles:
    if datablock.rna_type.identifier == 'FreestyleLineStyle':
      storage.batch.linestyles.append([datablock.name, [1, datablock]])

  # line style modifiers
  if option.linestyleModifiers:
    if hasattr(datablock.rna_type.base, 'identifier'):
      if hasattr(datablock.rna_type.base.base, 'identifier'):
        if datablock.rna_type.base.base.identifier == 'LineStyleModifier':
          storage.batch.modifiers.append([datablock.name, [1, datablock]])

  # sensors
  if option.sensors:
    if hasattr(datablock.rna_type.base, 'identifier'):
      if datablock.rna_type.base.identifier == 'Sensor':
        storage.batch.sensors.append([datablock.name, [1, datablock]])

  # controllers
  if option.controllers:
    if hasattr(datablock.rna_type.base, 'identifier'):
      if datablock.rna_type.base.identifier == 'Controller':
        storage.batch.controllers.append([datablock.name, [1, datablock]])

  # actuators
  if option.actuators:
    if hasattr(datablock.rna_type.base, 'identifier'):
      if datablock.rna_type.base.identifier == 'Actuator':
        storage.batch.actuators.append([datablock.name, [1, datablock]])

  # scenes
  if option.scenes:
    if datablock.rna_type.identifier == 'Scene':
      storage.batch.scenes.append([datablock.name, [1, datablock]])

  # render layers
  if option.renderLayers:
    if datablock.rna_type.identifier == 'SceneRenderLayer':
      storage.batch.renderLayers.append([datablock.name, [1, datablock]])

  # worlds
  if option.worlds:
    if datablock.rna_type.identifier == 'World':
      storage.batch.worlds.append([datablock.name, [1, datablock]])

  # libraries
  if option.libraries:
    if datablock.rna_type.identifier == 'Library':
      storage.batch.libraries.append([datablock.name, [1, datablock]])

  # images
  if option.images:
    if datablock.rna_type.identifier == 'Image':
      storage.batch.images.append([datablock.name, [1, datablock]])

  # masks
  if option.masks:
    if datablock.rna_type.identifier == 'Mask':
      storage.batch.masks.append([datablock.name, [1, datablock]])

  # sequences
  if option.sequences:
    if hasattr(datablock.rna_type.base, 'identifier'):
      if datablock.rna_type.base.identifier == 'Sequence':
        storage.batch.sequences.append([datablock.name, [1, datablock]])

  # movie clips
  if option.movieClips:
    if datablock.rna_type.identifier == 'MovieClip':
      storage.batch.movieClips.append([datablock.name, [1, datablock]])

  # sounds
  if option.sounds:
    if datablock.rna_type.identifier == 'Sound':
      storage.batch.sounds.append([datablock.name, [1, datablock]])

  # screens
  if option.screens:
    if datablock.rna_type.identifier == 'Screen':
      storage.batch.screens.append([datablock.name, [1, datablock]])

  # keying sets
  if option.keyingSets:
    if datablock.rna_type.identifier == 'KeyingSet':
      storage.batch.keyingSets.append([datablock.bl_label, [1, datablock]])

  # palettes
  if option.palettes:
    if datablock.rna_type.identifier == 'Palette':
      storage.batch.palettes.append([datablock.name, [1, datablock]])

  # brushes
  if option.brushes:
    if datablock.rna_type.identifier == 'Brush':
      storage.batch.brushes.append([datablock.name, [1, datablock]])

  # nodes
  if option.nodes:
    if hasattr(datablock.rna_type.base, 'base'):
      if hasattr(datablock.rna_type.base.base, 'base'):
        if hasattr(datablock.rna_type.base.base.base, 'identifier'):
          if datablock.rna_type.base.base.base.identifier == 'Node':
            storage.batch.nodes.append([datablock.name, [1, datablock]])

            if tag:
              datablock.label = name(context, datablock.label)

  # node groups
  if option.nodeGroups:
    if hasattr(datablock.rna_type.base, 'identifier'):
      if datablock.rna_type.base.identifier == 'NodeTree':
        storage.batch.nodeGroups.append([datablock.name, [1, datablock]])

  # texts
  if option.texts:
    if datablock.rna_type.identifier == 'Text':
      storage.batch.texts.append([datablock.name, [1, datablock]])

def process(context, collection):
  '''
    Process collection, send names to name.
  '''

  if not collection == []:

    # option
    option = context.scene.BatchName

    # count
    counter = [
      # 'datablock.name', ...
    ]

    # datablocks
    datablocks = [
      # ['datablock.name', datablock], [...
    ]

    # duplicates
    duplicates = [
      # 'datablock.name', ...
    ]

    # collection
    for item in collection[:]:

      # sort
      if option.sort:

        # name
        item[0] = name(context, (re.split(r'\W[0-9]*$|_[0-9]*$', item[0]))[0])
      else:
        item[0] = name(context, item[0])

      # count
      counter.append(item[0])

    # name count
    i = 0
    for item in collection[:]:

      # name count
      item[1][0] = counter.count(counter[i])
      i += 1

    # randomize
    for item in collection[:]:

      # sort
      if option.sort:
        if item[1][0] > 1:

          # randomize name
          if hasattr(item[1][1], 'name'):
            item[1][1].name = str(random())
          elif hasattr(item[1][1], 'info'):
            item[1][1].info = str(random())
          elif hasattr(item[1][1], 'bl_label'):
            item[1][1].bl_label = str(random())
        elif not option.sortOnly:

          # randomize name
          if hasattr(item[1][1], 'name'):
            item[1][1].name = str(random())
          elif hasattr(item[1][1], 'info'):
            item[1][1].info = str(random())
          elif hasattr(item[1][1], 'bl_label'):
            item[1][1].bl_label = str(random())
      else:

        # randomize name
        if hasattr(item[1][1], 'name'):
          item[1][1].name = str(random())
        elif hasattr(item[1][1], 'info'):
          item[1][1].info = str(random())
        elif hasattr(item[1][1], 'bl_label'):
          item[1][1].bl_label = str(random())

    # sort
    if option.sort:
      i = 0
      for item in collection[:]:
        datablocks.append([item[0], i])
        i += 1
      i = 0
      for item in sorted(datablocks):

        # name count
        if collection[item[1]][1][0] > 1:

          # duplicates
          if collection[item[1]][0] not in duplicates:

            # suffix last
            if option.suffixLast:

              # rename
              rename = collection[item[1]][0] + option.separator + '0'*option.padding + str(i + option.start).zfill(len(str(collection[item[1]][1][0]))) + option.suffix
            else:

              # rename
              rename = collection[item[1]][0] + option.separator + '0'*option.padding + str(i + option.start).zfill(len(str(collection[item[1]][1][0])))

            # name
            if hasattr(collection[item[1]][1][1], 'name'):
              collection[item[1]][1][1].name = rename
            elif hasattr(collection[item[1]][1][1], 'info'):
              collection[item[1]][1][1].info = rename
            elif hasattr(collection[item[1]][1][1], 'bl_label'):
              collection[item[1]][1][1].bl_label = rename
            i += 1
          if i == collection[item[1]][1][0]:
            i = 0

            # duplicates
            duplicates.append(collection[item[1]][0])

    # assign names
    if not option.sortOnly:
      for item in collection[:]:
        if item[0] not in duplicates:

          # suffix last
          if option.suffixLast:

            # rename
            rename = item[0] + option.suffix
          else:

            # rename
            rename = item[0]

          # name
          if hasattr(item[1][1], 'name'):
            item[1][1].name = rename
          elif hasattr(item[1][1], 'info'):
            item[1][1].info = rename
          elif hasattr(item[1][1], 'bl_label'):
            item[1][1].bl_label = rename

    # clear counter
    counter.clear()

    # clear datablocks
    datablocks.clear()

    # clear duplicates
    duplicates.clear()

# name
def name(context, oldName):
  '''
    Name datablocks received from process.
  '''

  # option
  option = context.scene.BatchName

  # name check
  nameCheck = oldName

  # custom name
  if option.customName != '':

    # new name
    newName = option.customName
  else:

    # new name
    newName = oldName

  # trim start
  newName = newName[option.trimStart:]

  # trim end
  if option.trimEnd > 0:
    newName = newName[:-option.trimEnd]

  # find & replace
  if option.regex:
    newName = re.sub(option.find, option.replace, newName)
  else:
    newName = re.sub(re.escape(option.find), option.replace, newName)

  # prefix & suffix
  newName = option.prefix + newName + option.suffix if not option.suffixLast else option.prefix + newName

  # name check
  if nameCheck != newName:
    return newName
  else:
    return oldName
