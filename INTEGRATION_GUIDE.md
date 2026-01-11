# Complete Integration Guide: Skyscraper + Matt's Lair

This guide provides step-by-step instructions for combining the Blender-generated Skyscraper with the Matt's Lair VRChat world.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Part 1: Blender Preparation](#part-1-blender-preparation)
3. [Part 2: Export from Blender](#part-2-export-from-blender)
4. [Part 3: Unity Setup](#part-3-unity-setup)
5. [Part 4: Material Conversion](#part-4-material-conversion)
6. [Part 5: Optimization](#part-5-optimization)
7. [Part 6: VRChat Integration](#part-6-vrchat-integration)
8. [Part 7: Testing](#part-7-testing)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Software Requirements

✅ **Blender**
- Version: 4.0 or later
- Download: https://www.blender.org/download/

✅ **Unity**
- Version: **2022.3.22f1** (EXACT VERSION REQUIRED)
- Download via Unity Hub: https://unity.com/download

✅ **VRChat Creator Companion**
- Download: https://vrchat.com/home/download
- Required for VRChat SDK management

✅ **Git** (optional but recommended)
- For cloning repositories

### Repository Setup

1. **Clone the source repositories:**
   ```bash
   # Skyscraper repository
   git clone https://github.com/MatthewPChapdelaine/Skyscraper-1.git
   
   # Matt's Lair repository
   git clone https://github.com/MatthewPChapdelaine/MattsLair-01-04-26.git
   ```

2. **Create workspace directory:**
   ```bash
   mkdir VRChat-Skyscraper-Project
   cd VRChat-Skyscraper-Project
   ```

---

## Part 1: Blender Preparation

### Step 1.1: Open Skyscraper Project

1. Launch Blender 4.0+
2. **File** → **Open**
3. Navigate to `Skyscraper-1` folder
4. Open Blender and prepare to run the Python script

### Step 1.2: Generate Skyscraper

1. Open Blender's **Scripting** workspace
2. Click **Open** and select `skyscraper_superior_design.py`
3. Click **Run Script** button
4. Wait 5-10 minutes for generation to complete

**Expected Output:**
- 50-story building with all systems
- ~7,850 objects in scene
- Materials applied

### Step 1.3: Initial Optimization in Blender

Before exporting, perform these optimizations:

#### A. Join Floor Instances

Floors can be instance-referenced rather than unique geometry:

1. Select all floor slabs: **Select** → **Select All by Type** → **Mesh**
2. Filter to floors only (Floor_0, Floor_1, etc.)
3. **Object** → **Join** (Ctrl+J) for floors that are identical
4. This reduces object count significantly

#### B. Simplify Materials

The skyscraper may have complex node-based materials:

1. **Shading** workspace
2. For each material, identify which can be simplified:
   - Combine similar materials
   - Bake procedural textures to images
   - Reduce unnecessary nodes

#### C. LOD Preparation

Create 3 levels of detail:

1. **LOD0** (High detail): Full geometry - for close-up viewing
2. **LOD1** (Medium detail): Simplified facade, no interior details
3. **LOD2** (Low detail): Simple box with texture for distant viewing

For LOD creation:
1. **Modifiers** → **Decimate**
2. LOD1: Ratio 0.5 (50% reduction)
3. LOD2: Ratio 0.1 (90% reduction)

### Step 1.4: Scene Cleanup

1. **Delete unnecessary objects:**
   - Cameras (except reference camera)
   - Lights (VRChat will use its own)
   - Hidden objects not needed for export

2. **Apply all transforms:**
   - Select all: **A**
   - **Object** → **Apply** → **All Transforms**

3. **Check scale:**
   - The building should be at real-world scale
   - 50m × 50m footprint, 200m height
   - VRChat uses meters as units (matches Blender default)

---

## Part 2: Export from Blender

### Step 2.1: Export Settings

1. **File** → **Export** → **FBX (.fbx)**
2. **Configure export settings:**

```
Export Settings:
✅ Include:
   - Selected Objects (or Active Collection)
   - Mesh
   - Materials
   - Textures (embed)

✅ Transform:
   - Scale: 1.00
   - Apply Scalings: FBX All
   - Forward: -Z Forward
   - Up: Y Up

✅ Geometry:
   - Apply Modifiers: YES
   - Smoothing: Face
   - Tangent Space: YES

✅ Armature: (leave unchecked)

✅ Animation: (leave unchecked)
```

### Step 2.2: Export Files

Export multiple versions for different uses:

#### A. Full Detail Export
- **Filename**: `Skyscraper_Full.fbx`
- **Purpose**: Interior exploration, detailed viewing
- **Object Count**: All geometry included

#### B. Exterior Only Export
- **Filename**: `Skyscraper_Exterior.fbx`
- **Purpose**: Visible from Matt's Lair hub
- **Object Count**: Facade only, no interior

#### C. LOD Exports
- **Filename**: `Skyscraper_LOD0.fbx` (full detail)
- **Filename**: `Skyscraper_LOD1.fbx` (medium detail)
- **Filename**: `Skyscraper_LOD2.fbx` (low detail)

### Step 2.3: Export Materials

Unity needs texture files:

1. **File** → **External Data** → **Pack Resources**
2. **File** → **External Data** → **Unpack Resources**
3. Select **Write files to subfolder** with name `Textures`
4. This extracts all textures to a folder

---

## Part 3: Unity Setup

### Step 3.1: Open Matt's Lair Project

1. **Open VRChat Creator Companion**
2. **Add Project** → Select `MattsLair-01-04-26` folder
3. **Manage Project** → Install VRChat Worlds SDK
4. **Open Project** in Unity

### Step 3.2: Create Integration Scene

Option A: **New Empire World** (Recommended)

1. **File** → **New Scene**
2. Save as: `Assets/Scenes/EmpireSkyscraper.unity`
3. Add **VRC_SceneDescriptor** component

Option B: **Add to Existing Scene**

1. Open `MattsLair.unity`
2. Create new section for skyscraper

### Step 3.3: Import FBX Files

1. Create folder: `Assets/Empire Worlds/Skyscraper/Models/`
2. Drag all exported FBX files into this folder
3. Wait for Unity to import (may take several minutes)

### Step 3.4: Import Texture Files

1. Create folder: `Assets/Empire Worlds/Skyscraper/Textures/`
2. Drag extracted texture folder from Blender
3. For each texture:
   - Select texture in Unity
   - **Inspector** → **Texture Type** → Adjust settings
   - **Apply**

**Recommended Texture Settings:**
```
Max Size: 2048 (or 1024 for optimization)
Compression: High Quality
Format: BC7 (for best quality/size)
Generate Mip Maps: YES
```

---

## Part 4: Material Conversion

Unity cannot directly use Blender's node-based materials. Conversion is required.

### Step 4.1: Analyze Imported Materials

1. Select imported skyscraper model
2. **Inspector** → **Materials** tab
3. Note all materials listed

### Step 4.2: Convert to Unity Materials

For each Blender material:

#### A. Create Unity Material

1. **Assets** → **Create** → **Material**
2. Name to match Blender material
3. **Shader**: Select `VRChat/Mobile/Standard Lite` (for optimization)
   - Or `Standard` for better quality

#### B. Map Blender Properties to Unity

**Example: Shiny Black Leather Material**

Blender properties:
- Base Color: (0.01, 0.01, 0.01)
- Metallic: 0.15
- Roughness: 0.08

Unity Standard Shader:
- **Albedo**: Set to dark gray/black
- **Metallic**: 0.15
- **Smoothness**: 0.92 (= 1 - Roughness)
- **Normal Map**: If available from textures

#### C. Assign Materials to Model

1. Select model in **Hierarchy**
2. **Inspector** → Expand materials
3. Drag converted Unity materials to slots

### Step 4.3: Material Optimization

For VRChat performance:

1. **Combine similar materials:**
   - Use texture atlasing
   - Reduce unique material count to < 50

2. **Bake complex materials:**
   - For materials with complex nodes in Blender
   - Bake to diffuse, normal, metallic textures

3. **Use VRChat shaders:**
   - Prefer `VRChat/Mobile/` shaders for best performance
   - `Standard` shader is acceptable for PC-only worlds

---

## Part 5: Optimization

### Step 5.1: Polygon Count Reduction

**Target**: 200,000 - 250,000 triangles for entire building

Check current count:
1. Select model
2. **Stats** panel (top-right of Scene view)
3. Note **Tris** count

If too high:

#### A. Use LOD Group

1. Select model root
2. **Component** → **Rendering** → **LOD Group**
3. Add 3 LOD levels:
   - **LOD 0**: Full detail model (0-25% distance)
   - **LOD 1**: Medium detail model (25-50% distance)
   - **LOD 2**: Low detail model (50-100% distance)

#### B. ProBuilder Simplification

1. Install **ProBuilder** (Unity Package Manager)
2. Select mesh
3. **Tools** → **ProBuilder** → **Simplify Mesh**
4. Adjust reduction percentage

### Step 5.2: Collision Optimization

Don't use visual mesh for collision!

1. Select skyscraper model
2. **Inspector** → **Remove** default Mesh Collider
3. **Component** → **Physics** → **Box Collider**
4. Add box colliders for:
   - Each floor (or groups of floors)
   - External walls
   - Core structure

### Step 5.3: Occlusion Culling

Hide interior geometry when outside, and vice versa:

1. **Window** → **Rendering** → **Occlusion Culling**
2. **Object** tab → Mark all geometry as **Occluder** and **Occludee**
3. **Bake** tab → Click **Bake**
4. Wait for baking to complete

### Step 5.4: Lighting Optimization

VRChat performance depends heavily on lighting:

#### A. Bake Lightmaps

1. Mark all static geometry:
   - Select all building parts
   - **Inspector** → Check **Static** → **Lightmap Static**

2. **Window** → **Rendering** → **Lighting**
3. **Mixed Lighting** → **Baked Indirect**
4. **Generate Lighting**
5. Wait for baking (can take 10-60 minutes)

#### B. Limit Realtime Lights

- Remove unnecessary lights
- Use baked lighting where possible
- Keep realtime lights < 4 per area

---

## Part 6: VRChat Integration

### Step 6.1: Add VRChat Components

#### A. Scene Descriptor

1. Create empty GameObject: `SceneSetup`
2. **Component** → **VRChat SDK** → **VRC_SceneDescriptor**
3. Configure:
   - **Spawns**: Add spawn point locations
   - **Respawn Height**: -10 (below ground level)
   - **Reference Camera**: Set to scene camera

#### B. Spawn Points

1. Create empty GameObject: `SpawnPoint`
2. Position at main entrance or lobby
3. Add more spawn points if needed (for multiple players)

### Step 6.2: Portal Integration

#### Option A: Standalone Skyscraper World

If skyscraper is separate world:

1. Build and publish skyscraper world
2. Note World ID from VRChat SDK
3. In Matt's Lair hub:
   - Create portal frame
   - **Component** → **VRC_PortalMarker**
   - Set **Target World ID**

#### Option B: Integrated into Hub

If skyscraper is in same world as hub:

1. Use teleportation instead of portals
2. **Component** → **VRC_SceneDescriptor** → Add multiple spawns
3. Use trigger colliders for teleportation

### Step 6.3: Navigation

Add helper elements:

1. **Directional signs**: Text meshes or UI panels
2. **Teleport points**: For quick travel between floors
3. **Minimap** (optional): 2D map display

---

## Part 7: Testing

### Step 7.1: Local Testing

1. **VRChat SDK** → **Show Control Panel**
2. **Builder** tab
3. **Build & Test**
4. VRChat launches with your world
5. Test:
   - Collision detection
   - Navigation
   - Performance (check framerate)
   - Visual quality

### Step 7.2: Performance Validation

In VRChat SDK Control Panel:

1. **Builder** tab → **Build & Test**
2. Check **Stats** panel:
   - Performance rank: Target **Medium** or better
   - Draw calls: < 100
   - Polygon count: within budget
   - Texture memory: < 100 MB

### Step 7.3: Optimization Iteration

If performance is poor:

1. **Reduce LOD distances**: Force lower detail sooner
2. **Combine meshes**: Reduce draw calls
3. **Simplify materials**: Use simpler shaders
4. **Remove unnecessary geometry**: Delete hidden objects

### Step 7.4: Publish

When ready:

1. **VRChat SDK** → **Show Control Panel**
2. **Builder** tab → **Build & Publish**
3. **Sign in** with VRChat account
4. Fill in:
   - World name: "Matt's Lair - Skyscraper"
   - Description
   - Tags
   - Thumbnail (take screenshot in Unity)
5. **Upload**
6. World is **Private** by default - share World ID for testing

---

## Troubleshooting

### Issue: FBX Import Errors

**Problem**: Unity can't import FBX or shows errors

**Solutions:**
- Re-export from Blender with different settings
- Check Blender export scale (should be 1.0)
- Try exporting smaller sections separately
- Ensure FBX SDK is up to date in Blender

### Issue: Materials Look Wrong

**Problem**: Materials don't match Blender appearance

**Solutions:**
- Manually recreate materials in Unity
- Bake Blender materials to textures first
- Use texture maps instead of procedural materials
- Check texture import settings (sRGB for color, Linear for data)

### Issue: Too Many Polygons

**Problem**: Polygon count exceeds VRChat limits

**Solutions:**
- Implement LOD system (see Step 5.1)
- Use Decimate modifier in Blender before export
- Remove interior details not visible to players
- Use normal maps instead of high-poly geometry

### Issue: World Size Too Large

**Problem**: Exceeds 200 MB total filesize

**Solutions:**
- Compress textures more aggressively
- Reduce texture resolution (2048 → 1024)
- Remove duplicate materials
- Use texture atlasing
- Consider splitting into multiple worlds

### Issue: Performance Rank "Very Poor"

**Problem**: VRChat rates world performance as poor

**Solutions:**
- Reduce polygon count (target < 250k)
- Bake lighting instead of realtime
- Combine meshes to reduce draw calls
- Simplify materials and shaders
- Remove unnecessary scripts
- Use occlusion culling

### Issue: Collisions Not Working

**Problem**: Players fall through floors or can't enter

**Solutions:**
- Add Box Colliders to floors and walls
- Check collider layers (should be **Environment**)
- Ensure colliders are enabled
- Don't use Mesh Collider for complex geometry

### Issue: Portal Doesn't Work

**Problem**: Portal to skyscraper doesn't load

**Solutions:**
- Verify World ID is correct
- Ensure both worlds are published
- Check portal marker placement
- Test portal from VRChat client, not Unity

---

## Next Steps

After successful integration:

1. **Add Interior Details**: Furnish floors, add decorations
2. **Implement Narrative**: Add storytelling elements
3. **Create Quests**: Use Udon scripts for interactive gameplay
4. **User Testing**: Invite friends to test
5. **Iterate**: Refine based on feedback

---

## Additional Resources

- [Blender to Unity Workflow](https://docs.unity3d.com/Manual/HOWTO-ImportObjectBlender.html)
- [VRChat World Creation](https://docs.vrchat.com/docs/creating-your-first-world)
- [VRChat Performance Ranks](https://docs.vrchat.com/docs/avatar-performance-ranking-system)
- [Unity LOD Groups](https://docs.unity3d.com/Manual/class-LODGroup.html)

---

**Good luck with your integration!** 🏢🎮
