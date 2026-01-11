# VRChat Matt's Lair with Skyscraper Integration

## Project Overview

This project combines two existing repositories to create a VRChat world featuring **Matt's Lair** with an integrated **Skyscraper**:

- **Source 1**: [Skyscraper-1](https://github.com/MatthewPChapdelaine/Skyscraper-1) - Procedural 50-story skyscraper generated in Blender
- **Source 2**: [MattsLair-01-04-26](https://github.com/MatthewPChapdelaine/MattsLair-01-04-26) - VRChat hub-and-spoke world project

## Vision

Create a VRChat instance that combines:
- **Matt's Lair**: Central navigation hub with portals to 4 Empire worlds
- **Skyscraper**: A procedurally-generated 50-story office building integrated into one of the Empire worlds or as a standalone destination

## Technical Architecture

### Skyscraper Repository
- **Technology**: Blender Python API
- **Output**: 50-story procedurally generated building
- **Features**:
  - 200m height (50 floors × 4m)
  - 50m × 50m footprint
  - Core walls, elevators, stairs
  - Curtain wall facade
  - Physics-based materials

### Matt's Lair Repository
- **Technology**: Unity 2022.3.22f1 + VRChat SDK3
- **Architecture**: Hub-and-spoke design
- **Features**:
  - Central hub (25-30 MB)
  - 4 Empire worlds (40-50 MB each)
  - Portal system for world transitions
  - State persistence

## Integration Strategy

### Approach 1: Skyscraper as Empire World
Integrate the skyscraper as one of the four Empire worlds accessible from Matt's Lair.

**Advantages**:
- Fits existing hub-and-spoke architecture
- Clear navigation path
- Allows for narrative integration

**Filesize Target**: 40-50 MB for skyscraper world

### Approach 2: Skyscraper Within Matt's Lair Hub
Place a scaled-down version of the skyscraper visible from the central hub.

**Advantages**:
- Immediate visual impact
- Creates architectural landmark
- Can serve as portal to full-scale version

**Filesize Target**: Additional 10-15 MB to hub budget

### Approach 3: Hybrid Approach (Recommended)
- Exterior visible from Matt's Lair hub (low-poly version)
- Portal leads to full interior experience in separate world
- Best of both worlds: visual presence + detailed exploration

## Workflow

### Phase 1: Export from Blender
1. Run skyscraper generation script in Blender
2. Optimize geometry for VRChat
3. Export as FBX with materials

### Phase 2: Import to Unity
1. Import FBX into Unity project
2. Apply VRChat-compatible shaders
3. Set up collision meshes
4. Optimize for performance

### Phase 3: VRChat Integration
1. Add VRC_SceneDescriptor
2. Configure spawn points
3. Add portal connections
4. Test and optimize

## Repository Structure

```
Combine-1/
├── README.md                    # This file
├── INTEGRATION_GUIDE.md         # Detailed step-by-step guide
├── docs/
│   ├── blender-export.md       # Blender export instructions
│   ├── unity-import.md         # Unity import process
│   └── vrchat-optimization.md  # VRChat-specific optimizations
├── scripts/
│   ├── blender/
│   │   └── export_skyscraper.py    # Automated export script
│   └── unity/
│       └── optimize_materials.cs    # Material conversion script
└── assets/
    └── reference/                   # Reference images and docs
```

## Requirements

### For Blender Work
- Blender 4.0+
- Python 3.10+
- 8GB+ RAM

### For Unity/VRChat Work
- Unity 2022.3.22f1 (exactly)
- VRChat Creator Companion
- VRChat SDK3 Worlds
- 16GB+ RAM recommended

## Performance Targets

### Skyscraper Optimization Goals
- **Polygon Count**: 200k-250k triangles (from ~7,850 objects)
- **Texture Memory**: < 40 MB
- **Draw Calls**: < 100
- **LOD Levels**: 3 levels for distance culling

### VRChat Performance Rank
- Target: **Medium** or better
- Quest compatibility: Optional (PC-only acceptable)

## Getting Started

1. **Clone this repository**
   ```bash
   git clone https://github.com/MatthewPChapdelaine/Combine-1.git
   cd Combine-1
   ```

2. **Follow the Integration Guide**
   See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for complete setup instructions

3. **Export Skyscraper from Blender**
   See [docs/blender-export.md](docs/blender-export.md)

4. **Import to Unity/VRChat**
   See [docs/unity-import.md](docs/unity-import.md)

## Key Considerations

### Filesize Management
- **Original Skyscraper**: Blender native (varies)
- **Exported FBX**: 20-40 MB (before optimization)
- **Optimized for VRChat**: Target 40-50 MB
- **Total Project**: Stay under 200 MB

### Optimization Strategies
1. **LOD Implementation**: 3 detail levels
2. **Occlusion Culling**: Bake occlusion data
3. **Texture Atlasing**: Combine materials
4. **Instance Repetition**: Reuse floor geometry
5. **Collider Simplification**: Box colliders for floors

### Material Conversion
- Blender PBR materials → Unity Standard/VRChat shaders
- Bake complex shader nodes to textures
- Maintain visual fidelity while reducing complexity

## Development Phases

### Phase 1: Proof of Concept (Week 1-2)
- [ ] Export basic skyscraper from Blender
- [ ] Import to Unity
- [ ] Verify VRChat compatibility
- [ ] Initial performance test

### Phase 2: Optimization (Week 3-4)
- [ ] Implement LOD system
- [ ] Optimize materials and textures
- [ ] Set up occlusion culling
- [ ] Reduce polygon count

### Phase 3: Integration (Week 5-6)
- [ ] Integrate with Matt's Lair hub
- [ ] Add portal connections
- [ ] Implement spawn points
- [ ] Add navigation aids

### Phase 4: Polish & Testing (Week 7-8)
- [ ] Final optimization pass
- [ ] VRChat SDK validation
- [ ] User testing
- [ ] Bug fixes and refinement

## Resources

### Documentation
- [Skyscraper-1 Repository](https://github.com/MatthewPChapdelaine/Skyscraper-1)
- [MattsLair-01-04-26 Repository](https://github.com/MatthewPChapdelaine/MattsLair-01-04-26)
- [VRChat Documentation](https://docs.vrchat.com/)
- [Unity Documentation](https://docs.unity3d.com/2022.3/Documentation/Manual/)

### Community
- [VRChat Discord](https://discord.gg/vrchat)
- [VRChat Creator Forums](https://ask.vrchat.com/)

## License

This project combines elements from two source repositories. Please respect the original licenses.

## Contact

For questions about this integration project, please open an issue on this repository.

---

**Last Updated**: January 2026
