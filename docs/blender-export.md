# Blender Export Guide for VRChat Skyscraper

## Overview

This guide covers the process of exporting the procedurally-generated skyscraper from Blender in a format optimized for Unity and VRChat.

## Prerequisites

- Blender 4.0 or later
- Skyscraper model generated using `skyscraper_superior_design.py`
- ~10 GB free disk space for export files

---

## Step 1: Prepare the Scene

### 1.1 Open Generated Skyscraper

1. Launch Blender
2. Run the skyscraper generation script if not already done
3. Verify the building appears complete with all systems

### 1.2 Scene Cleanup

Remove unnecessary objects that won't be needed in VRChat:

```python
# Optional: Run this Python script in Blender
import bpy

# Delete cameras (VRChat will use its own)
for obj in bpy.data.objects:
    if obj.type == 'CAMERA':
        bpy.data.objects.remove(obj, do_unlink=True)

# Delete lights (VRChat handles lighting differently)
for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

print("Scene cleanup complete")
```

### 1.3 Check Scale

VRChat uses Unity's coordinate system (1 unit = 1 meter). Blender's default matches this.

**Verify scale:**
- Select the building root
- Check dimensions: Should be ~50m × 50m × 200m
- If incorrect, scale entire model before export

---

## Step 2: Optimization Before Export

### 2.1 Join Similar Objects

Reduce object count by joining identical floor elements:

```python
import bpy

# Join all floor slabs
floor_objects = [obj for obj in bpy.data.objects if obj.name.startswith('Floor_')]
if floor_objects:
    bpy.context.view_layer.objects.active = floor_objects[0]
    for obj in floor_objects:
        obj.select_set(True)
    bpy.ops.object.join()
    
print(f"Joined {len(floor_objects)} floor objects")
```

### 2.2 Material Simplification

For each complex material:

1. **Bake Procedural Textures:**
   - Select object with material
   - **Shading** workspace
   - Add **Image Texture** node
   - **Render** → **Bake**
   - Type: **Diffuse**, **Normal**, **Roughness** (separate bakes)
   - Save baked textures

2. **Simplify Material Nodes:**
   - Remove noise/procedural nodes
   - Use baked textures instead
   - Keep only: Base Color, Metallic, Roughness, Normal

### 2.3 Create LOD Versions

**LOD 0 (Full Detail)**
- Original model with all details
- Use for close-up viewing
- No modifications needed

**LOD 1 (Medium Detail)**
1. Duplicate entire model
2. Add **Decimate** modifier
3. **Ratio**: 0.5 (50% polygon reduction)
4. **Apply** modifier
5. Rename: Add "_LOD1" suffix to all objects

**LOD 2 (Low Detail)**
1. Duplicate LOD1 model
2. Add **Decimate** modifier
3. **Ratio**: 0.2 (80% total reduction from original)
4. **Apply** modifier
5. Simplify to basic box with facade texture
6. Rename: Add "_LOD2" suffix

---

## Step 3: Export Settings

### 3.1 FBX Export Configuration

**File** → **Export** → **FBX (.fbx)**

#### Export Settings Panel

```
Main Tab:
├── Include
│   ├── ☑ Selected Objects (if exporting selection)
│   ├── ☑ Active Collection (for full export)
│   ├── ☑ Mesh
│   ├── ☑ Other: (uncheck all - no cameras, lights, etc.)
│   └── ☑ Custom Properties
│
├── Transform
│   ├── Scale: 1.00
│   ├── Apply Scalings: FBX All
│   ├── Forward: -Z Forward
│   ├── Up: Y Up
│   └── ☑ Apply Unit
│   └── ☑ Use Space Transform
│
├── Geometry
│   ├── ☑ Apply Modifiers
│   ├── Smoothing: Face
│   ├── ☐ Export Subdivision Surface
│   ├── ☑ Triangulate Faces
│   ├── ☐ Apply Modifiers
│   └── ☑ Tangent Space
│
└── Armature, Animation (leave all unchecked)
```

### 3.2 Material Settings

```
Bake Animation
├── ☐ (disabled - no animation needed)

Path Mode
├── Copy (Embed textures into FBX)
├── Or: Absolute (keep textures as separate files)
```

**Recommended:** Use **Copy** to embed textures, OR export textures separately (Step 4)

---

## Step 4: Export Process

### 4.1 Full Building Export

**Purpose:** Complete skyscraper for interior exploration

1. **Select All** (A key)
2. **File** → **Export** → **FBX**
3. **File Name:** `Skyscraper_Full.fbx`
4. **Location:** Create dedicated export folder
5. **Export FBX**
6. **Wait:** Large models take 2-5 minutes

**Expected Size:** 30-60 MB (before Unity optimization)

### 4.2 Exterior Only Export

**Purpose:** Lightweight version for distant viewing or hub integration

1. **Select only:**
   - Facade elements
   - Roof
   - Ground floor entrance
   - External structural columns
2. **Deselect:**
   - All interior elements
   - Floor slabs (except ground)
   - Interior walls
   - Elevators, stairs
3. **File** → **Export** → **FBX**
4. **File Name:** `Skyscraper_Exterior.fbx`
5. **Export FBX**

**Expected Size:** 5-15 MB

### 4.3 LOD Exports

Export each LOD level separately:

**LOD0 (Full Detail):**
```
Filename: Skyscraper_LOD0.fbx
Selection: All high-detail geometry
```

**LOD1 (Medium):**
```
Filename: Skyscraper_LOD1.fbx
Selection: All medium-detail geometry (with _LOD1 suffix)
```

**LOD2 (Low):**
```
Filename: Skyscraper_LOD2.fbx
Selection: Low-detail geometry only (with _LOD2 suffix)
```

---

## Step 5: Texture Export

### 5.1 Automatic Texture Extraction

If textures were embedded in FBX, extract them:

1. **File** → **External Data** → **Unpack Resources**
2. Choose **Write Files to subfolder**
3. Folder name: `Textures`
4. Textures are extracted to this folder

### 5.2 Manual Texture Export

For materials with Image Texture nodes:

1. **UV Editing** workspace
2. For each texture:
   - Select texture in **Shader Editor**
   - **Image** → **Save As**
   - Format: **PNG** (lossless) or **JPEG** (smaller)
   - Save to `Textures/` folder

### 5.3 Baked Texture Maps

If you baked procedural materials (Step 2.2):

1. For each baked texture:
   - **Image Editor** → Select baked image
   - **Image** → **Save As**
   - Naming convention:
     - `MaterialName_Diffuse.png`
     - `MaterialName_Normal.png`
     - `MaterialName_Roughness.png`
     - `MaterialName_Metallic.png`

---

## Step 6: Verify Export

### 6.1 Re-import Test

1. **File** → **New**
2. **File** → **Import** → **FBX**
3. Select exported `Skyscraper_Full.fbx`
4. **Import**
5. Verify:
   - ☑ Geometry appears intact
   - ☑ Materials are assigned
   - ☑ Textures load (if embedded)
   - ☑ Scale is correct (50m × 50m × 200m)

### 6.2 File Size Check

Expected file sizes:

| Export | Size Range | Notes |
|--------|------------|-------|
| Full Building | 30-60 MB | With all geometry |
| Exterior Only | 5-15 MB | Facade + roof only |
| LOD0 | 30-60 MB | Same as full |
| LOD1 | 15-30 MB | 50% polygons |
| LOD2 | 3-8 MB | 10-20% polygons |
| Textures Folder | 10-40 MB | All texture files |

**If files are too large:**
- Apply Decimate modifier more aggressively
- Reduce texture resolution before export
- Export without embedding textures

---

## Step 7: Organization for Unity

### 7.1 Create Export Package

Organize all files for Unity import:

```
Skyscraper_Export/
├── Models/
│   ├── Skyscraper_Full.fbx
│   ├── Skyscraper_Exterior.fbx
│   ├── Skyscraper_LOD0.fbx
│   ├── Skyscraper_LOD1.fbx
│   └── Skyscraper_LOD2.fbx
├── Textures/
│   ├── LeatherMaterial_Diffuse.png
│   ├── LeatherMaterial_Normal.png
│   ├── GlassMaterial_Diffuse.png
│   └── [... all texture files ...]
└── README.txt (export notes)
```

### 7.2 Create Export Documentation

In `README.txt`:

```
Skyscraper Export Package
Generated: [Date]
Blender Version: 4.0+

Contents:
- Models/: FBX files for Unity import
- Textures/: All material textures

Building Specifications:
- Dimensions: 50m × 50m × 200m
- Floors: 50
- Floor Height: 4m
- Total Objects: ~7,850 (before optimization)
- Optimized Objects: ~2,000 (after joining)

LOD Information:
- LOD0: Full detail, 100% polygons
- LOD1: Medium detail, 50% polygons
- LOD2: Low detail, 10-20% polygons

Material Count: [number]
Texture Resolution: 2048×2048 (most), 1024×1024 (some)

Next Steps:
1. Import FBX files to Unity
2. Import textures to Unity
3. Assign textures to materials
4. Set up LOD Group component
5. Configure for VRChat

See INTEGRATION_GUIDE.md for complete instructions.
```

---

## Automation Script

For repeated exports, use this Python script in Blender:

```python
# File: export_skyscraper.py
# Run in Blender's Scripting workspace

import bpy
import os

# Configuration
EXPORT_PATH = "C:/Export/Skyscraper/"  # Change to your path
EXPORT_FULL = True
EXPORT_EXTERIOR = True
EXPORT_LODS = True

# Create export directory
os.makedirs(EXPORT_PATH + "Models", exist_ok=True)
os.makedirs(EXPORT_PATH + "Textures", exist_ok=True)

# Export settings
def export_fbx(filename, selection=None):
    filepath = os.path.join(EXPORT_PATH, "Models", filename)
    
    if selection:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selection:
            obj.select_set(True)
    
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=(selection is not None),
        mesh_smooth_type='FACE',
        apply_scale_options='FBX_SCALE_ALL',
        axis_forward='-Z',
        axis_up='Y',
        bake_space_transform=True,
        embed_textures=False,
        path_mode='COPY'
    )
    print(f"Exported: {filename}")

# Export full building
if EXPORT_FULL:
    export_fbx("Skyscraper_Full.fbx")

# Export exterior only
if EXPORT_EXTERIOR:
    exterior_objects = [obj for obj in bpy.data.objects 
                       if 'exterior' in obj.name.lower() 
                       or 'facade' in obj.name.lower()]
    export_fbx("Skyscraper_Exterior.fbx", exterior_objects)

# Export LODs
if EXPORT_LODS:
    for lod_level in [0, 1, 2]:
        lod_objects = [obj for obj in bpy.data.objects 
                      if f'_LOD{lod_level}' in obj.name]
        if lod_objects:
            export_fbx(f"Skyscraper_LOD{lod_level}.fbx", lod_objects)

print("Export complete!")
```

---

## Troubleshooting

### Problem: Export Crashes Blender

**Cause:** Too many polygons or complex materials

**Solution:**
- Export in smaller sections (by floor or building component)
- Apply Decimate modifier more aggressively
- Join objects to reduce count before export

### Problem: Textures Not Included

**Cause:** Path mode not set to embed/copy

**Solution:**
- Re-export with **Path Mode: Copy**
- Or manually export textures (Step 5)

### Problem: Scale Wrong in Unity

**Cause:** Transform not applied in Blender

**Solution:**
- Before export: Select all → **Object** → **Apply** → **All Transforms**
- Re-export with corrected scale

### Problem: Materials Look Different

**Cause:** Blender materials don't directly convert to Unity

**Solution:**
- This is expected
- Materials will be recreated in Unity (see Unity Import Guide)
- Bake complex materials to textures first

---

## Next Steps

After successful export:

1. **Proceed to Unity Import Guide**: [docs/unity-import.md](unity-import.md)
2. **Material Conversion**: Recreate materials in Unity
3. **Optimization**: Further reduce polygon count if needed
4. **VRChat Integration**: Add VRChat components

---

## Reference

- [Blender FBX Export Documentation](https://docs.blender.org/manual/en/latest/addons/import_export/scene_fbx.html)
- [Unity FBX Import](https://docs.unity3d.com/Manual/HOWTO-ImportObjectBlender.html)
- [VRChat World Optimization](https://docs.vrchat.com/docs/quest-content-optimization)
