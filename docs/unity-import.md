# Unity Import Guide: Skyscraper to VRChat

## Overview

This guide covers importing the Blender-exported skyscraper into Unity 2022.3.22f1 and preparing it for VRChat deployment.

## Prerequisites

✅ Completed Blender export (see [blender-export.md](blender-export.md))
✅ Unity 2022.3.22f1 installed
✅ VRChat Creator Companion set up
✅ Matt's Lair project opened in VCC

---

## Part 1: Unity Project Setup

### Step 1.1: Open Matt's Lair Project

1. **Launch VRChat Creator Companion**
2. **Add existing project** (if not already added)
   - Navigate to `MattsLair-01-04-26` folder
3. **Manage Project** → Install VRChat Worlds SDK
4. **Open Project** button

Unity will launch with the project.

### Step 1.2: Create Integration Structure

Create folder structure for skyscraper assets:

```
Assets/
└── Empire Worlds/
    └── Skyscraper/
        ├── Models/
        ├── Textures/
        ├── Materials/
        ├── Prefabs/
        └── Scenes/
```

**In Unity:**
1. **Project** panel → **Assets/Empire Worlds**
2. Right-click → **Create** → **Folder** → Name: `Skyscraper`
3. Repeat to create subfolders

---

## Part 2: Import FBX Models

### Step 2.1: Copy FBX Files

1. **Windows Explorer/Finder**: Navigate to Blender export folder
2. Copy all `.fbx` files from `Models/` folder
3. Drag into Unity: `Assets/Empire Worlds/Skyscraper/Models/`

**Wait for import** (may take 2-10 minutes depending on file size)

### Step 2.2: Configure Import Settings

For each FBX file:

1. **Select FBX** in Project panel
2. **Inspector** → Configure settings:

#### Model Tab
```
Scale Factor: 1
Convert Units: ✓
Bake Axis Conversion: ✓

Meshes:
- Read/Write: ✓ (for editing)
- Optimize Mesh: ✓
- Generate Colliders: ☐ (we'll add custom)

Blend Shape Normals: Import
Normals: Import
Tangents: Calculate Mikk T Space

Blend Shapes: Import
```

#### Rig Tab
```
Animation Type: None
```

#### Animation Tab
```
(Skip - no animations)
```

#### Materials Tab
```
Material Creation Mode: Standard (Legacy)
Location: Use External Materials (Legacy)

Naming: By Base Texture Name
Search: Recursive-Up

On Demand Remap:
- Remapped Materials: (will populate after)
```

3. **Click Apply**

### Step 2.3: Extract Materials

Unity creates materials from FBX, but they need textures:

1. **Select FBX** in Project
2. **Inspector** → **Materials** tab
3. **Extract Materials** button
4. Choose location: `Assets/Empire Worlds/Skyscraper/Materials/`
5. **Extract**

Materials are now separate files that can be edited.

---

## Part 3: Import and Assign Textures

### Step 3.1: Copy Texture Files

1. Copy all textures from Blender export `Textures/` folder
2. Drag into Unity: `Assets/Empire Worlds/Skyscraper/Textures/`

### Step 3.2: Configure Texture Import Settings

For **each texture**, configure based on type:

#### Base Color/Diffuse Textures
```
Texture Type: Default
Texture Shape: 2D
sRGB (Color Texture): ✓

Advanced:
- Alpha Source: From Gray Scale
- Alpha Is Transparency: ✓

Max Size: 2048 (reduce to 1024 if needed)
Compression: High Quality
Format: BC7 (best quality/size for color)

Generate Mip Maps: ✓
```

#### Normal Maps
```
Texture Type: Normal map
Create from Grayscale: ☐

Max Size: 2048
Compression: High Quality
Format: BC7

Generate Mip Maps: ✓
```

#### Metallic/Roughness Maps
```
Texture Type: Default
sRGB (Color Texture): ☐ (Linear)

Max Size: 2048
Compression: High Quality
Format: BC7

Generate Mip Maps: ✓
```

**Apply settings** to each texture.

### Step 3.3: Assign Textures to Materials

For each material in `Materials/` folder:

1. **Double-click material** to edit
2. **Inspector** → Shader settings
3. Assign textures to appropriate slots:

**Example for "LeatherMaterial":**
```
Shader: Standard (or VRChat/Mobile/Standard Lite)

Main Maps:
- Albedo: LeatherMaterial_Diffuse
- Metallic: 0.15 (or LeatherMaterial_Metallic texture)
- Smoothness: 0.92
- Normal Map: LeatherMaterial_Normal

```

**Repeat for all materials.**

---

## Part 4: Material Conversion to VRChat Shaders

### Step 4.1: Choose Shader Type

VRChat-compatible shaders:

| Shader | Performance | Quality | Use Case |
|--------|-------------|---------|----------|
| VRChat/Mobile/Standard Lite | Best | Good | Recommended |
| VRChat/Mobile/Toon Lit | Best | Stylized | Cartoon look |
| Standard | Medium | Best | PC-only |
| VRChat/Mobile/Particles/Additive | Best | Effects | Portals, effects |

**Recommended:** Use `VRChat/Mobile/Standard Lite` for building geometry.

### Step 4.2: Convert Materials

For each material:

1. **Select material** in Project panel
2. **Inspector** → **Shader** dropdown
3. Select: `VRChat/Mobile/Standard Lite`
4. Reassign textures if they were cleared

**VRChat/Mobile/Standard Lite settings:**
```
Main Texture: [Albedo/Diffuse texture]
Tint Color: White (or adjust for color variation)
Normal Map: [Normal map texture]

Lighting:
- Reflectivity: 0-1 (controls shine)
- Metallic: 0-1 (metal vs. non-metal)
```

### Step 4.3: Material Optimization

Reduce material count:

1. **Identify duplicate materials**
   - Similar looking materials can often share one material
   - Example: All black leather can use one material

2. **Combine materials:**
   - Merge similar materials
   - Use texture atlasing for variations

**Target:** < 50 unique materials total

---

## Part 5: Create Scene and Add Model

### Step 5.1: Create New Scene

**Option A: New Empire World** (Recommended)
1. **File** → **New Scene**
2. **Save As:** `Assets/Scenes/EmpireSkyscraper.unity`

**Option B: Add to Matt's Lair**
1. **Open:** `Assets/Scenes/MattsLair.unity`
2. Position skyscraper in desired location

### Step 5.2: Place Model in Scene

1. **Drag FBX** from Project into Hierarchy
   - Use `Skyscraper_Full.fbx` for complete building
2. **Position** at origin (0, 0, 0) or desired location
3. **Verify scale:** Should be 50m × 50m × 200m

### Step 5.3: Check Materials

1. **Select model** in Hierarchy
2. **Scene view** → View model
3. Verify materials look correct
4. Adjust if needed

---

## Part 6: Set Up LOD System

### Step 6.1: Create LOD Group

1. **Select model root** in Hierarchy
2. **Component** → **Rendering** → **LOD Group**
3. LOD Group component appears in Inspector

### Step 6.2: Configure LOD Levels

**LOD Group settings:**

```
LOD 0 (0-25% distance):
- Renderers: [Drag Skyscraper_LOD0 here]

LOD 1 (25-50% distance):
- Renderers: [Drag Skyscraper_LOD1 here]

LOD 2 (50-100% distance):
- Renderers: [Drag Skyscraper_LOD2 here]

Culled (100%):
- Fade Mode: None
```

### Step 6.3: Import LOD Models

If you exported separate LOD FBX files:

1. **Import** each LOD FBX (`LOD0.fbx`, `LOD1.fbx`, `LOD2.fbx`)
2. **Create empty GameObject** as LOD container
3. **Parent each LOD model** under this GameObject
4. **Assign to LOD Group** (as shown above)

---

## Part 7: Collision Setup

### Step 7.1: Remove Default Colliders

The FBX import may have added Mesh Colliders (too expensive):

1. **Select model** in Hierarchy
2. **Inspector** → Find any **Mesh Collider** components
3. **Remove** them (right-click → Remove Component)

### Step 7.2: Add Optimized Colliders

Use simple colliders for better performance:

#### Ground Floor
1. **Create empty GameObject:** `FloorColliders`
2. **Add Component** → **Physics** → **Box Collider**
3. **Size:** (50, 0.5, 50)
4. **Center:** (0, 0.25, 0)

#### Each Floor (or groups)
1. **Repeat** for each floor or every 5 floors
2. **Position** at correct height (floor_number × 4m)

#### Exterior Walls
1. **Add 4 Box Colliders** for walls:
   - North wall: Size (50, 200, 0.5), Position (0, 100, 25)
   - South wall: Size (50, 200, 0.5), Position (0, 100, -25)
   - East wall: Size (0.5, 200, 50), Position (25, 100, 0)
   - West wall: Size (0.5, 200, 50), Position (-25, 100, 0)

#### Core/Elevator Shafts
1. **Add colliders** around elevator core if players can access

### Step 7.3: Set Layer

Set colliders to appropriate VRChat layer:

1. **Select all collider objects**
2. **Inspector** → **Layer** → **Environment**

---

## Part 8: Lighting Setup

### Step 8.1: Mark Static Geometry

For baked lightmaps:

1. **Select all building geometry** in Hierarchy
2. **Inspector** → **Static** dropdown (top-right)
3. **Check:** ✓ Lightmap Static
4. Also check: ✓ Occluder Static, ✓ Occludee Static

### Step 8.2: Configure Lighting

1. **Window** → **Rendering** → **Lighting**
2. **Environment** tab:
   - Skybox Material: Default or custom
   - Sun Source: Directional Light
   - Environment Lighting: Gradient
   - Ambient Color: Adjust for scene mood

3. **Mixed Lighting** tab:
   - Baked Global Illumination: ✓
   - Lighting Mode: Baked Indirect

### Step 8.3: Bake Lightmaps

1. **Lighting** window → **Baked Lightmaps** section
2. **Lightmap Settings:**
   ```
   Lightmapper: Progressive GPU (faster)
   Direct Samples: 32
   Indirect Samples: 512
   Bounces: 2
   Max Lightmap Size: 2048
   
   Compress Lightmaps: ✓
   Ambient Occlusion: ✓
   ```

3. **Generate Lighting** button
4. **Wait:** 10-60 minutes depending on complexity

**Note:** Baking significantly improves performance vs. realtime lighting.

---

## Part 9: Optimization

### Step 9.1: Check Stats

**Scene view** → **Stats** panel (top-right)

Review:
- **Tris:** Target < 250,000
- **Verts:** Target < 300,000
- **SetPass calls:** Target < 100
- **Batches:** Lower is better

### Step 9.2: Occlusion Culling

Hide geometry not visible to player:

1. **Window** → **Rendering** → **Occlusion Culling**
2. **Object** tab:
   - Select all geometry
   - Check: ✓ Occluder Static
   - Check: ✓ Occludee Static
3. **Bake** tab → **Bake**
4. Wait for baking

### Step 9.3: Mesh Optimization

If polygon count still too high:

**Option 1: Use ProBuilder**
1. **Window** → **Package Manager**
2. Install **ProBuilder**
3. Select mesh → **Tools** → **ProBuilder** → **Decimate Mesh**

**Option 2: Reimport with lower LOD**
- Use LOD1 or LOD2 as primary model for better performance

### Step 9.4: Material Batching

Reduce draw calls:

1. **Combine similar materials** where possible
2. Use **texture atlasing** to merge textures
3. Ensure materials use GPU instancing: ☑ Enable GPU Instancing

---

## Part 10: VRChat Components

### Step 10.1: Add Scene Descriptor

1. **Create empty GameObject:** `SceneSetup`
2. **Add Component** → **VRChat SDK** → **VRC_SceneDescriptor**

**Configure:**
```
Spawns: [List of spawn point transforms]
Respawn Height: -10
Reference Camera: [Assign scene camera]
```

### Step 10.2: Create Spawn Points

1. **Create empty GameObject:** `SpawnPoints`
2. **Create child GameObject:** `Spawn_Entrance`
3. **Position** at building entrance or lobby
4. **Add more spawns** for multiplayer support

**Assign to Scene Descriptor:**
- Drag spawns to **Spawns** list

### Step 10.3: Add Post Processing (Optional)

For better visuals:

1. **Create GameObject** → **3D Object** → **Post-process Volume**
2. **Add Profile**
3. Configure effects (bloom, color grading, etc.)
4. Check: ✓ Is Global

---

## Part 11: Portal Integration

### Option A: Standalone World

If skyscraper is separate world from Matt's Lair:

1. **Build and upload** skyscraper world first
2. **Note World ID** from VRChat SDK
3. **In Matt's Lair scene:**
   - Create portal frame
   - Add **VRC_PortalMarker** component
   - Paste **World ID**

### Option B: Same World

If integrated into Matt's Lair hub:

1. **Position skyscraper** in hub scene
2. Use **teleportation** for quick travel
3. No portal needed

---

## Part 12: Testing

### Step 12.1: VRChat SDK Validation

1. **VRChat SDK** → **Show Control Panel**
2. **Builder** tab
3. Review **Content Validation** section
4. Fix any errors shown

### Step 12.2: Local Test Build

1. **Builder** tab → **Build & Test**
2. VRChat client launches
3. Test:
   - ✓ Can enter building
   - ✓ Collision works
   - ✓ Performance acceptable (check FPS)
   - ✓ Materials look correct
   - ✓ Portals work (if applicable)

### Step 12.3: Performance Check

In VRChat SDK Control Panel:

**Stats Tab:**
- Performance Rank: Target **Medium** or better
- Overall Performance: Check all metrics

If performance is poor, see [vrchat-optimization.md](vrchat-optimization.md)

---

## Part 13: Publishing

### Step 13.1: Prepare Upload

1. **Take thumbnail screenshot:**
   - Position **Reference Camera** for best view
   - **Game** view shows what will be thumbnail

2. **Fill in world info:**
   - Name: "Matt's Lair - Skyscraper"
   - Description
   - Capacity: 20-40 players recommended
   - Tags: "Exploration", "Architecture", etc.

### Step 13.2: Build & Publish

1. **VRChat SDK** → **Show Control Panel**
2. **Sign in** with VRChat account
3. **Builder** tab → **Build & Publish for Windows**
4. **Wait** for upload (5-20 minutes)
5. World uploaded as **Private** (share World ID to test)

### Step 13.3: Test in VRChat

1. **Launch VRChat**
2. Access world via World ID
3. Test with friends
4. Gather feedback
5. Iterate and republish

---

## Troubleshooting

### Issue: FBX Import Shows Pink Materials

**Cause:** Materials can't find textures

**Solution:**
- Extract materials (Step 2.3)
- Manually assign textures (Step 3.3)
- Check texture file names match

### Issue: Model Appears Tiny/Huge

**Cause:** Scale factor incorrect

**Solution:**
- Select FBX → Inspector → Model tab
- Scale Factor: Try 1, 0.01, or 100
- Reapply import settings

### Issue: Materials Don't Work in VRChat

**Cause:** Using incompatible shader

**Solution:**
- Convert all materials to VRChat/Mobile/ shaders
- See Step 4 for shader conversion

### Issue: Too Many Draw Calls

**Cause:** Too many unique materials

**Solution:**
- Combine similar materials
- Use texture atlasing
- Enable GPU instancing on materials

### Issue: Baked Lighting Looks Wrong

**Cause:** Incorrect settings or UVs

**Solution:**
- Ensure all objects marked Static
- Check lightmap UVs exist (FBX import setting)
- Try rebaking with different settings

### Issue: Players Fall Through Floors

**Cause:** Missing or incorrect colliders

**Solution:**
- Add Box Colliders to floors (Step 7)
- Set layer to **Environment**
- Test collision in Play mode

---

## Performance Optimization Checklist

After import, verify:

- [ ] LOD system configured with 3 levels
- [ ] Occlusion culling baked
- [ ] Lightmaps baked (not realtime lighting)
- [ ] Materials use VRChat-compatible shaders
- [ ] Texture sizes appropriate (2048 or 1024)
- [ ] Polygon count < 250k triangles
- [ ] Draw calls < 100
- [ ] Colliders use simple shapes (boxes, not mesh)
- [ ] Static batching enabled (mark Static)

---

## Next Steps

After successful Unity import:

1. **Optimize further** if performance rank is poor
2. **Add interactive elements** (doors, elevators, etc.) using Udon
3. **Create narrative content** for the space
4. **User testing** with friends
5. **Polish and refinement**

See [vrchat-optimization.md](vrchat-optimization.md) for advanced optimization techniques.

---

## Additional Resources

- [Unity Manual - Importing Models](https://docs.unity3d.com/Manual/ImportingModelFiles.html)
- [VRChat World Creation](https://docs.vrchat.com/docs/creating-your-first-world)
- [Unity Optimization](https://docs.unity3d.com/Manual/OptimizingGraphicsPerformance.html)
- [VRChat Performance Ranks](https://docs.vrchat.com/docs/avatar-performance-ranking-system)
