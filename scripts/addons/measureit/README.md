MeasureIt
=================

MeasureIt is an add-on designed for displaying measures in the viewport, making the process of design objects with exact measures, easier.

These tools are extremely useful for any job that requires exact measurements, including architectural projects, technical design and 3D printing.

You can use it for:
 
- Mesh vertex to vertex measure: Length between vertices in the same mesh.

- Mesh vertex labeling: Add a label to any mesh vertex. This allows identify easily different areas or objects in the scene.

- Object to Object: Distance between object origins, vertex to origin or vertex to vertex. 

- Object to origin: Distance between object origin to scene origin or vertex to scene origin.

- Allows work with different scales.

The measures can be used with Meshes, Empties, Lamps and Cameras. Blender units, Metric and Imperial are supported.

As all measure definitions are saved in the blend file, you can save the file and the next time you use it, the measures will be ready.

Demo video: http://youtu.be/R0jCdCoaRvs

Changes in version 1.1
=============================
- New scale parameter

Changes in version 1.2
=============================
- New scale text.
- New scale precision.
- New select units (scene or manual selection (meters, cm, mm, ft or in)).
- New override parameteres for scene (color, font, line width).
- Precision allows 0.
- Fix error after loading new .blend.

Changes in version 1.3
=============================
- New Mesh angles.
- Show measure changes in EDIT mode.
- Cleaning measures not used when saving.
- Small bug fixing.


Changes in version 1.4
=============================
- Now several segments can be created at the same time selecting by vertex, edge, face or edge loops.
- Now you can use or not selected axis in distances.
- Added degrees symbol to angles.
- New button for deleting all object measures
- Fixed bug if scene scale is different of 1.

 Video: https://youtu.be/nu3hxPSBLsU

Changes in version 1.4.1
=============================
- Fixed bug if vertex are not linked by edge

Changes in version 1.5
=============================

Note: REMOVE previous version before installing V1.5

- New: Measures can be rendered (opengl and final render).
- New: Arc measures with radio, angle and length.
- New: Sum automatically several segments.
- New: Calculate Areas. Edit and Object mode.
- New: Arrows (line, triangle, TShape).
- New: Vertex to origin in one axis measure.
- New: Text can be multiline using pipe (|).
- New: Create annotations.
- New: Display orthogonal segments.
- Improved customization options and UI.
- Fixed error for Quadview.
- Fixed error for Object to vertex link.
- Fixed error on alpha for lines.
- Small bug fixing.
- Tested on versions 2.74 and 2.75.

Demo video: http://youtu.be/hiEZxnPHq70

Also, I have created a basic tutorial of how create a Blueprint.

How create a Blueprint: http://youtu.be/Qb1U7g4JFbA
Changes in version 1.5.1
=============================
- New funtion to include sum totals in text using <#letter>
- Fixed error whith huge scaling.
- Fixed error for labeling text position

Changes in version 1.6
=============================
- Show button moved to top of the panel.
- New debug meshes option.

Changes in version 1.6.1
=============================
- Option to disable normal details.

Changes in version 1.6.2
=============================
- Allow bigger number in some parameters

Changes in version 1.6.3
=============================
- Improve tools panel

Changes in version 1.6.4
=============================
- Fix scale factor for radius and circunference length.

Changes in version 1.6.5
=============================
- Fix render error due API change in 2.77.
