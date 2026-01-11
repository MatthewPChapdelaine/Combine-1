# VRChat Optimization Guide for Skyscraper

## Overview

This guide covers advanced optimization techniques to ensure the skyscraper performs well in VRChat, targeting a **Medium** performance rank or better.

## Performance Targets

### VRChat Performance Ranks

| Rank | Color | Description |
|------|-------|-------------|
| Excellent | Green | Optimal performance |
| Good | Green | Great performance |
| Medium | Yellow | Acceptable performance ⭐ TARGET |
| Poor | Orange | Degraded performance |
| Very Poor | Red | Major performance issues |

### Skyscraper-Specific Targets

```
Polygon Count: 200,000 - 250,000 triangles
Texture Memory: < 100 MB
Draw Calls: < 100
Material Count: < 50
Mesh Renderers: < 200
Particle Systems: < 10
Download Size: 40-50 MB
```

---

## Part 1: Polygon Optimization

### 1.1 Current vs. Target

**Blender Export:**
- Original: ~7,850 objects
- Estimated polygons: 500k - 1M+ triangles

**VRChat Target:**
- Optimized: ~2,000 objects
- Target polygons: 200k - 250k triangles

**Reduction needed:** 50-80% polygon reduction

### 1.2 LOD Strategy

Implement 3 levels of detail:

#### LOD0: High Detail (0-25% distance)
- Full detail geometry
- All interior features
- Use when player is inside or nearby
- ~200k triangles

#### LOD1: Medium Detail (25-50% distance)
- Simplified interior (or removed entirely)
- Facade detail reduced 50%
- Windows become textures
- ~50k triangles

#### LOD2: Low Detail (50-100% distance)
- Simple box shape
- Facade texture only
- No interior
- ~5k triangles

#### Culled (100% distance)
- Not rendered at all
- Saves maximum resources

### 1.3 Polygon Reduction Techniques

**A. Merge Floor Instances**

Instead of 50 unique floor slabs:
```csharp
// Floors 1-10: Share one geometry instance
// Floors 11-20: Share another instance
// etc.

Result: 50 → 5 unique floor meshes
```

**B. Simplify Facade**

- Windows: Don't model frames, use texture
- Mullions: Bake into normal map instead of geometry
- Columns: Reduce from cylinder to box with texture

**C. Remove Hidden Geometry**

- Interior walls between rooms (players can't access)
- Detailed mechanical systems
- Decorative elements too small to see

**D. Decimate Modifier**

In Unity or Blender:
1. Select mesh
2. Apply Decimate modifier
3. Target ratio: 0.5 (50% reduction)
4. Check result visually

---

## Part 2: Texture Optimization

### 2.1 Texture Memory Budget

**Total budget:** < 100 MB texture memory

**Breakdown:**
- Diffuse/Albedo: 40 MB
- Normal maps: 30 MB
- Metallic/Roughness: 20 MB
- Other: 10 MB

### 2.2 Texture Resolution Guidelines

| Type | Distance | Resolution | Format |
|------|----------|------------|--------|
| Hero elements | Close-up | 2048×2048 | BC7 |
| Standard | Medium | 1024×1024 | BC7 |
| Background | Far | 512×512 | BC7 |
| UI elements | Any | 1024×1024 | BC7 |

### 2.3 Texture Atlasing

Combine multiple textures into one:

**Example: Floor Materials**
```
Before: 50 floor textures × 2048×2048 = 200 MB
After: 1 atlas texture × 4096×4096 = 16 MB

Savings: 92% reduction!
```

**How to create texture atlas:**

1. **Unity Sprite Atlas** (for similar textures)
2. **Texture Packer** (external tool)
3. **Manual in Photoshop/GIMP:**
   - Create 4096×4096 canvas
   - Arrange textures in grid
   - Adjust UVs in Unity to match

### 2.4 Compression Settings

For each texture in Unity:

**Albedo/Diffuse:**
```
Max Size: 1024-2048
Compression: High Quality
Format: BC7 (Windows) / ASTC (Mobile)
sRGB: ✓
Generate Mip Maps: ✓
```

**Normal Maps:**
```
Max Size: 1024-2048
Compression: High Quality
Format: BC7 or BC5 (better for normals)
sRGB: ☐ (uncheck!)
Generate Mip Maps: ✓
```

**Metallic/Roughness:**
```
Max Size: 1024
Compression: High Quality
Format: BC7
sRGB: ☐
Generate Mip Maps: ✓
```

---

## Part 3: Material Optimization

### 3.1 Material Count Reduction

**Target:** < 50 unique materials

**Strategy:**

1. **Identify duplicates:**
   - All black leather → 1 material
   - All glass → 1 material
   - All concrete → 1 material

2. **Use variations with single material:**
   - Vertex colors for color variation
   - One material with texture atlas
   - Shader parameters instead of new materials

3. **Merge similar materials:**
   - Dark gray + black → use tint
   - Shiny metal + matte metal → roughness parameter

### 3.2 Shader Selection

**Performance ranking (best to worst):**

1. **VRChat/Mobile/Standard Lite** ⭐ RECOMMENDED
   - Minimal features
   - Best performance
   - Good for most surfaces

2. **VRChat/Mobile/Toon Lit**
   - Stylized look
   - Good performance
   - If you want cartoon aesthetic

3. **Standard**
   - More features
   - Medium performance
   - PC-only acceptable

4. **Custom shaders**
   - Avoid unless necessary
   - Poor performance
   - Use only for special effects

### 3.3 Material Properties

For VRChat/Mobile/Standard Lite:

```
Main Texture: [Diffuse/Albedo]
Tint Color: White (or color variation)
Normal Map: [Normal map] or None
Reflectivity: 0-0.5 (lower is better for performance)
Metallic: 0 or 1 (binary is better than gradients)

GPU Instancing: ✓ ENABLE THIS
```

**Disable unnecessary features:**
- Emission (unless needed for glow effects)
- Parallax mapping
- Detail textures
- Height maps

---

## Part 4: Draw Call Reduction

### 4.1 Understanding Draw Calls

**What is a draw call?**
- Each time GPU draws a different material/mesh
- More draw calls = worse performance
- Target: < 100 draw calls

**What causes draw calls?**
- Each unique material
- Each mesh renderer
- Dynamic batching failures

### 4.2 Static Batching

Combine static geometry:

1. **Select all building geometry**
2. **Inspector** → **Static** → ✓ Batching Static
3. Unity automatically combines at build time

**Requirements:**
- Objects must be marked Static
- Objects share same material
- Objects don't move

### 4.3 GPU Instancing

For repeated objects (like floors):

1. **Select material**
2. **Inspector** → **Enable GPU Instancing** ✓
3. Identical objects now draw in one call

**Best for:**
- Repeated floor geometry
- Window panels
- Columns

### 4.4 Mesh Combining

Manually combine meshes:

```csharp
// Unity Editor: Select multiple objects
// Right-click → Combine Meshes (requires extension)

// Or use this script:
using UnityEngine;
using UnityEditor;

public class MeshCombiner : EditorWindow
{
    [MenuItem("Tools/Combine Meshes")]
    static void CombineSelected()
    {
        GameObject[] selection = Selection.gameObjects;
        MeshFilter[] meshFilters = selection.SelectMany(go => 
            go.GetComponentsInChildren<MeshFilter>()).ToArray();
        
        CombineInstance[] combine = new CombineInstance[meshFilters.Length];
        for (int i = 0; i < meshFilters.Length; i++)
        {
            combine[i].mesh = meshFilters[i].sharedMesh;
            combine[i].transform = meshFilters[i].transform.localToWorldMatrix;
        }
        
        Mesh combinedMesh = new Mesh();
        combinedMesh.CombineMeshes(combine);
        
        GameObject newObj = new GameObject("CombinedMesh");
        newObj.AddComponent<MeshFilter>().sharedMesh = combinedMesh;
        newObj.AddComponent<MeshRenderer>();
    }
}
```

---

## Part 5: Occlusion Culling

### 5.1 What is Occlusion Culling?

- Hides geometry not visible to player
- Massive performance gain for interiors
- Essential for multi-floor buildings

### 5.2 Setup Occlusion Culling

1. **Mark all geometry:**
   - Select building objects
   - **Inspector** → **Static** → ✓ Occluder Static
   - **Inspector** → **Static** → ✓ Occludee Static

2. **Configure occlusion:**
   - **Window** → **Rendering** → **Occlusion Culling**
   - **Object** tab: Verify objects marked
   - **Bake** tab: Configure settings

3. **Bake settings:**
   ```
   Smallest Occluder: 5
   Smallest Hole: 0.25
   Backface Threshold: 100
   ```

4. **Click Bake**

### 5.3 Verify Occlusion

1. **Visualization** tab in Occlusion Culling window
2. Move scene camera around
3. Watch objects appear/disappear as occluded
4. Adjust if too aggressive or too lenient

---

## Part 6: Lighting Optimization

### 6.1 Baked vs. Realtime Lighting

**Performance cost ranking:**

1. **Baked (Best):** Pre-calculated, no runtime cost
2. **Mixed:** Some baked, some realtime
3. **Realtime (Worst):** All calculated at runtime

**Recommendation:** Use Baked for skyscraper.

### 6.2 Lightmap Settings

**Window** → **Rendering** → **Lighting**

```
Mixed Lighting:
- Baked Global Illumination: ✓
- Lighting Mode: Baked Indirect

Lightmapping Settings:
- Lightmapper: Progressive GPU
- Direct Samples: 32
- Indirect Samples: 512
- Bounces: 2
- Max Lightmap Size: 2048
- Compress Lightmaps: ✓
- Ambient Occlusion: ✓
- AO Max Distance: 1
```

### 6.3 Realtime Light Limits

If you must use realtime lights:

**Maximum per area:**
- Directional lights: 1
- Point lights: 2-4
- Spotlights: 2-4

**Total in scene:** < 20 realtime lights

### 6.4 Light Probes

For dynamic objects (players):

1. **GameObject** → **Light** → **Light Probe Group**
2. Position probes throughout interior
3. Players receive lighting from nearest probes

---

## Part 7: Collision Optimization

### 7.1 Collision Cost

**Performance ranking (best to worst):**

1. **Box Collider:** Cheapest
2. **Sphere Collider:** Very cheap
3. **Capsule Collider:** Cheap
4. **Convex Mesh Collider:** Expensive
5. **Mesh Collider:** VERY EXPENSIVE (avoid!)

### 7.2 Collision Strategy

**For floors:**
- One Box Collider per floor
- Size: (50, 0.3, 50)
- Total: 50 box colliders

**For walls:**
- 4 Box Colliders (N, S, E, W walls)
- Full building height

**For stairs:**
- Ramps with Box Colliders
- Or series of small boxes

**For complex areas:**
- Multiple simple shapes
- Never use Mesh Collider

### 7.3 Collision Layers

Use VRChat layers properly:

```
Layer 11: Environment (static building)
Layer 8: Interactive (doors, buttons)
Layer 13: Pickup (movable objects)
```

**Layer collision matrix:**
- Players collide with Environment ✓
- Players collide with Interactive ✓
- Environment does NOT collide with Environment ☐

---

## Part 8: Advanced Techniques

### 8.1 Portal Rendering

For very large buildings, use portal system:

- Each floor is separate "room"
- Portals at stairwells/elevators
- Only render current room + adjacent
- Massive performance gain

**Implementation:**
- Requires custom Udon scripts
- Advanced technique
- Worth it for very large spaces

### 8.2 Impostor Sprites

For distant building views:

1. Render building to texture
2. Create billboard sprite
3. Swap at far distances

**LOD3 = Impostor billboard:**
- 2 triangles
- 1 texture
- Nearly free performance

### 8.3 Asset Bundles

For extremely large projects:

- Split building into chunks
- Load chunks on-demand
- Unload unseen chunks
- Advanced VRChat technique

---

## Part 9: Optimization Checklist

### Pre-Build Checklist

Before building for VRChat:

#### Geometry
- [ ] Polygon count < 250k triangles
- [ ] LOD system implemented (3 levels)
- [ ] Hidden geometry removed
- [ ] Meshes combined where possible

#### Materials
- [ ] Material count < 50
- [ ] All materials use VRChat-compatible shaders
- [ ] GPU instancing enabled on materials
- [ ] Unnecessary texture maps removed

#### Textures
- [ ] Total texture memory < 100 MB
- [ ] Textures compressed (BC7 format)
- [ ] Texture atlasing used where beneficial
- [ ] Mip maps generated

#### Lighting
- [ ] All geometry marked Static
- [ ] Lightmaps baked
- [ ] Realtime lights < 20 total
- [ ] Light probes placed

#### Collision
- [ ] Mesh Colliders removed
- [ ] Simple colliders used (Box/Sphere)
- [ ] Collision layers set correctly

#### Occlusion
- [ ] Occlusion culling baked
- [ ] Occluder/Occludee marked
- [ ] Tested in Scene view

#### VRChat
- [ ] VRC_SceneDescriptor added
- [ ] Spawn points configured
- [ ] SDK validation passes
- [ ] Performance rank acceptable

---

## Part 10: Performance Testing

### 10.1 Unity Stats Panel

**Scene view** → **Stats** (top-right)

Monitor:
```
Tris: [current count] / 250,000 target
Verts: [current count]
SetPass calls: [current count] / 100 target
Batches: [current count] (lower is better)
```

### 10.2 Unity Profiler

**Window** → **Analysis** → **Profiler**

Check:
- **CPU Usage:** Rendering time
- **GPU Usage:** Bottlenecks
- **Memory:** Texture/mesh memory

### 10.3 VRChat SDK Stats

**VRChat SDK** → **Show Control Panel** → **Builder** → **Stats**

Reviews:
- Overall performance rank
- Individual category scores
- Recommendations

### 10.4 In-Game Testing

Test in actual VRChat client:

1. **Build & Test** from SDK
2. **Check FPS:** Should be 60+ FPS
3. **Test with friends:** Check multiplayer performance
4. **Different hardware:** Test on lower-end PCs

---

## Part 11: Troubleshooting Performance

### Issue: Performance Rank "Very Poor"

**Likely causes:**
1. Polygon count too high
2. Too many materials/draw calls
3. Realtime lighting (not baked)
4. Mesh Colliders

**Solutions:**
- Apply aggressive LOD
- Reduce material count
- Bake lighting
- Replace with Box Colliders

### Issue: Low FPS Inside Building

**Likely cause:** Occlusion culling not working

**Solutions:**
- Verify occlusion baked
- Check all objects marked Occluder/Occludee
- Rebake with adjusted settings

### Issue: Texture Memory Warning

**Likely cause:** Textures too large

**Solutions:**
- Reduce texture resolution (2048→1024)
- Use texture atlasing
- Remove unnecessary textures
- Compress more aggressively

### Issue: Too Many Draw Calls

**Likely cause:** Too many unique materials

**Solutions:**
- Combine similar materials
- Enable static batching
- Use GPU instancing
- Texture atlasing

---

## Part 12: Platform-Specific Optimization

### PC-Only World (Easier)

If not targeting Quest:
- Can use higher polygon counts
- Better textures
- More complex shaders
- Still target "Medium" rank

### Quest-Compatible (Harder)

If targeting Quest:
- Much stricter limits
- Polygon count < 100k
- Simple shaders only
- Texture resolution < 1024

**Quest Requirements:**
```
Polygons: < 100k triangles
Textures: < 40 MB
Materials: < 10 unique
Shaders: Mobile-only
Lighting: Baked only
```

---

## Summary: Priority Optimization Order

If performance is poor, optimize in this order:

1. **Polygon reduction** (biggest impact)
2. **Material consolidation** (draw calls)
3. **Texture compression** (memory)
4. **LOD implementation** (distance culling)
5. **Occlusion culling** (interior performance)
6. **Lightmap baking** (lighting cost)
7. **Collision simplification** (physics)
8. **Advanced techniques** (portals, etc.)

---

## Resources

- [VRChat World Optimization](https://docs.vrchat.com/docs/quest-content-optimization)
- [Unity Optimization Manual](https://docs.unity3d.com/Manual/OptimizingGraphicsPerformance.html)
- [VRChat Performance Ranks](https://docs.vrchat.com/docs/avatar-performance-ranking-system)
- [Unity Profiler](https://docs.unity3d.com/Manual/Profiler.html)

---

**Target achieved:** With these optimizations, the skyscraper should achieve **Medium** or better performance rank in VRChat! 🎯
