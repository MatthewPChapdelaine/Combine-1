"""
Automated Blender Skyscraper Export Script for VRChat
=====================================================

This script automates the export of the procedurally-generated skyscraper
from Blender in formats optimized for Unity and VRChat.

Usage:
1. Generate skyscraper using skyscraper_superior_design.py
2. Run this script in Blender's Scripting workspace
3. Exports will be saved to the specified directory

Author: Integration Project
Date: January 2026
"""

import bpy
import os
from pathlib import Path

# ===== CONFIGURATION =====
# Change these paths to match your setup
EXPORT_BASE_PATH = "C:/VRChat_Export/Skyscraper"  # Windows
# EXPORT_BASE_PATH = "/Users/username/VRChat_Export/Skyscraper"  # Mac
# EXPORT_BASE_PATH = "/home/username/VRChat_Export/Skyscraper"  # Linux

# Export options
EXPORT_FULL = True          # Full building with all interior
EXPORT_EXTERIOR = True      # Facade only (for hub integration)
EXPORT_LODS = True          # Multiple detail levels
EXPORT_TEXTURES = True      # Extract and save textures

# LOD settings
CREATE_LODS = True          # Generate LOD levels if they don't exist
LOD_RATIOS = {
    1: 0.5,   # LOD1: 50% polygons
    2: 0.2    # LOD2: 20% polygons
}

# ===== UTILITY FUNCTIONS =====

def create_export_directories():
    """Create necessary export directory structure"""
    dirs = [
        EXPORT_BASE_PATH,
        os.path.join(EXPORT_BASE_PATH, "Models"),
        os.path.join(EXPORT_BASE_PATH, "Textures"),
        os.path.join(EXPORT_BASE_PATH, "Documentation")
    ]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created export directories at: {EXPORT_BASE_PATH}")

def cleanup_scene():
    """Remove cameras and lights not needed for VRChat"""
    removed = 0
    for obj in bpy.data.objects:
        if obj.type in ['CAMERA', 'LIGHT']:
            bpy.data.objects.remove(obj, do_unlink=True)
            removed += 1
    print(f"✓ Removed {removed} cameras and lights")

def apply_all_transforms():
    """Apply all transforms to ensure correct scale in Unity"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.select_all(action='DESELECT')
    print("✓ Applied all transforms")

def create_lod_version(objects, lod_level, ratio):
    """Create a decimated LOD version of objects"""
    lod_objects = []
    
    for obj in objects:
        if obj.type != 'MESH':
            continue
            
        # Duplicate object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.duplicate()
        
        new_obj = bpy.context.active_object
        new_obj.name = f"{obj.name}_LOD{lod_level}"
        
        # Add and apply Decimate modifier
        decimate = new_obj.modifiers.new(name='Decimate', type='DECIMATE')
        decimate.ratio = ratio
        decimate.use_collapse_triangulate = True
        
        bpy.context.view_layer.objects.active = new_obj
        bpy.ops.object.modifier_apply(modifier='Decimate')
        
        lod_objects.append(new_obj)
    
    print(f"✓ Created LOD{lod_level} with {len(lod_objects)} objects at {ratio*100}% detail")
    return lod_objects

def export_fbx(filename, objects=None):
    """Export FBX with optimized settings for Unity/VRChat"""
    filepath = os.path.join(EXPORT_BASE_PATH, "Models", filename)
    
    # Select objects if specified
    if objects:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            if obj and obj.name in bpy.data.objects:
                obj.select_set(True)
        use_selection = True
    else:
        bpy.ops.object.select_all(action='SELECT')
        use_selection = False
    
    # Export with Unity-compatible settings
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=use_selection,
        
        # Transform settings
        global_scale=1.0,
        apply_scale_options='FBX_SCALE_ALL',
        axis_forward='-Z',
        axis_up='Y',
        bake_space_transform=True,
        
        # Geometry settings
        mesh_smooth_type='FACE',
        use_mesh_modifiers=True,
        use_tspace=True,
        
        # Material/Texture settings
        path_mode='COPY',  # Copy textures to export folder
        embed_textures=False,  # Keep as separate files
        
        # Exclude unnecessary elements
        object_types={'MESH'},
        use_custom_props=False,
        
        # No animation
        bake_anim=False
    )
    
    file_size = os.path.getsize(filepath) / (1024 * 1024)  # Size in MB
    print(f"✓ Exported {filename} ({file_size:.1f} MB)")
    return filepath

def export_textures():
    """Export all textures used in materials"""
    texture_path = os.path.join(EXPORT_BASE_PATH, "Textures")
    exported_count = 0
    
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
            
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                img = node.image
                
                # Create safe filename
                safe_name = "".join(c for c in img.name if c.isalnum() or c in (' ', '_', '-')).rstrip()
                ext = '.png'  # Default to PNG
                
                if img.filepath:
                    ext = os.path.splitext(img.filepath)[1] or ext
                
                output_path = os.path.join(texture_path, safe_name + ext)
                
                # Save image
                img.filepath_raw = output_path
                img.file_format = 'PNG' if ext == '.png' else 'JPEG'
                img.save()
                
                exported_count += 1
    
    print(f"✓ Exported {exported_count} textures")

def get_building_objects():
    """Get all objects that are part of the building"""
    # Exclude objects that shouldn't be exported
    exclude_types = {'CAMERA', 'LIGHT', 'EMPTY', 'SPEAKER'}
    
    building_objects = [
        obj for obj in bpy.data.objects 
        if obj.type not in exclude_types
    ]
    return building_objects

def get_exterior_objects():
    """Get only exterior facade objects"""
    keywords = ['facade', 'exterior', 'curtain', 'wall', 'column', 'roof', 'ground']
    
    exterior = []
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        
        # Check if object name contains exterior keywords
        obj_name_lower = obj.name.lower()
        if any(keyword in obj_name_lower for keyword in keywords):
            # Exclude if it's explicitly interior
            if 'interior' not in obj_name_lower and 'inside' not in obj_name_lower:
                exterior.append(obj)
    
    return exterior

def generate_export_report():
    """Create a text file documenting the export"""
    report_path = os.path.join(EXPORT_BASE_PATH, "Documentation", "export_report.txt")
    
    with open(report_path, 'w') as f:
        f.write("Skyscraper Export Report\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Export Date: {bpy.context.scene.name}\n")
        f.write(f"Blender Version: {bpy.app.version_string}\n")
        f.write(f"Export Path: {EXPORT_BASE_PATH}\n\n")
        
        f.write("Building Specifications:\n")
        f.write(f"  - Dimensions: 50m × 50m × 200m\n")
        f.write(f"  - Floors: 50\n")
        f.write(f"  - Floor Height: 4m\n\n")
        
        f.write("Exported Files:\n")
        models_path = os.path.join(EXPORT_BASE_PATH, "Models")
        for filename in os.listdir(models_path):
            if filename.endswith('.fbx'):
                size = os.path.getsize(os.path.join(models_path, filename)) / (1024 * 1024)
                f.write(f"  - {filename} ({size:.1f} MB)\n")
        
        f.write("\nNext Steps:\n")
        f.write("  1. Import FBX files to Unity 2022.3.22f1\n")
        f.write("  2. Apply VRChat-compatible materials\n")
        f.write("  3. Set up LOD Group component\n")
        f.write("  4. Configure for VRChat world\n")
        f.write("\nSee INTEGRATION_GUIDE.md for detailed instructions.\n")
    
    print(f"✓ Generated export report: {report_path}")

# ===== MAIN EXPORT PROCESS =====

def main():
    """Main export process"""
    print("\n" + "=" * 50)
    print("SKYSCRAPER EXPORT FOR VRCHAT")
    print("=" * 50 + "\n")
    
    # Step 1: Setup
    print("Step 1: Preparing export directories...")
    create_export_directories()
    
    # Step 2: Cleanup
    print("\nStep 2: Cleaning scene...")
    cleanup_scene()
    apply_all_transforms()
    
    # Step 3: Get objects
    print("\nStep 3: Collecting objects...")
    all_objects = get_building_objects()
    print(f"  Found {len(all_objects)} building objects")
    
    exterior_objects = get_exterior_objects()
    print(f"  Found {len(exterior_objects)} exterior objects")
    
    # Step 4: Export full building
    if EXPORT_FULL:
        print("\nStep 4: Exporting full building...")
        export_fbx("Skyscraper_Full.fbx", all_objects)
    
    # Step 5: Export exterior
    if EXPORT_EXTERIOR:
        print("\nStep 5: Exporting exterior only...")
        export_fbx("Skyscraper_Exterior.fbx", exterior_objects)
    
    # Step 6: Create and export LODs
    if EXPORT_LODS:
        print("\nStep 6: Creating and exporting LOD levels...")
        
        # LOD0 is full detail (already exported)
        export_fbx("Skyscraper_LOD0.fbx", all_objects)
        
        # Create and export LOD1
        if CREATE_LODS:
            lod1_objects = create_lod_version(all_objects, 1, LOD_RATIOS[1])
            export_fbx("Skyscraper_LOD1.fbx", lod1_objects)
            
            # Create and export LOD2
            lod2_objects = create_lod_version(lod1_objects, 2, LOD_RATIOS[2])
            export_fbx("Skyscraper_LOD2.fbx", lod2_objects)
    
    # Step 7: Export textures
    if EXPORT_TEXTURES:
        print("\nStep 7: Exporting textures...")
        export_textures()
    
    # Step 8: Generate report
    print("\nStep 8: Generating export report...")
    generate_export_report()
    
    # Complete
    print("\n" + "=" * 50)
    print("EXPORT COMPLETE!")
    print("=" * 50)
    print(f"\nExported files location: {EXPORT_BASE_PATH}")
    print("\nNext: Import to Unity (see INTEGRATION_GUIDE.md)")
    print()

# ===== RUN EXPORT =====

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR during export: {str(e)}")
        import traceback
        traceback.print_exc()
