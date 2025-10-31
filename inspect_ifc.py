"""
IFC File Inspector - Verify what data actually exists in your IFC file
"""

import ifcopenshell
import ifcopenshell.util.element
import sys


def inspect_ifc_file(file_path):
    """Inspect IFC file and show actual data"""
    print("=" * 70)
    print("IFC FILE INSPECTION REPORT")
    print("=" * 70)
    
    ifc = ifcopenshell.open(file_path)
    
    # 1. Basic Info
    print("\n📋 BASIC INFORMATION:")
    print(f"  Schema: {ifc.schema}")
    
    projects = ifc.by_type("IfcProject")
    if projects:
        print(f"  Project: {projects[0].Name}")
    
    buildings = ifc.by_type("IfcBuilding")
    if buildings:
        print(f"  Building: {buildings[0].Name}")
    
    # 2. Element Counts
    print("\n📊 ELEMENT COUNTS:")
    element_types = [
        "IfcWall", "IfcDoor", "IfcWindow", "IfcSpace",
        "IfcSlab", "IfcRoof", "IfcStair", "IfcColumn", "IfcBeam"
    ]
    
    for elem_type in element_types:
        count = len(ifc.by_type(elem_type))
        if count > 0:
            print(f"  {elem_type}: {count}")
    
    # 3. Wall Details
    print("\n🧱 WALL DETAILS:")
    walls = ifc.by_type("IfcWall")
    print(f"  Total Walls: {len(walls)}")
    
    for i, wall in enumerate(walls, 1):
        print(f"\n  Wall #{i}:")
        print(f"    Name: {wall.Name or 'Unnamed'}")
        print(f"    GlobalId: {wall.GlobalId}")
        print(f"    Type: {wall.is_a()}")
        
        # Check for properties
        try:
            psets = ifcopenshell.util.element.get_psets(wall)
            if psets:
                print(f"    Properties found: {len(psets)} property sets")
                for pset_name, pset_data in psets.items():
                    print(f"      - {pset_name}")
                    if isinstance(pset_data, dict):
                        for key, value in pset_data.items():
                            if 'area' in key.lower() or 'length' in key.lower() or 'height' in key.lower():
                                print(f"          {key}: {value}")
            else:
                print(f"    ⚠️  No properties found")
        except Exception as e:
            print(f"    ⚠️  Error reading properties: {e}")
        
        # Check for geometry
        if hasattr(wall, 'Representation') and wall.Representation:
            print(f"    ✓ Has geometric representation")
        else:
            print(f"    ⚠️  No geometric representation")
    
    # 4. Window Details
    print("\n🪟 WINDOW DETAILS:")
    windows = ifc.by_type("IfcWindow")
    print(f"  Total Windows: {len(windows)}")
    
    for i, window in enumerate(windows, 1):
        print(f"    Window #{i}: {window.Name or 'Unnamed'}")
    
    # 5. Door Details
    print("\n🚪 DOOR DETAILS:")
    doors = ifc.by_type("IfcDoor")
    print(f"  Total Doors: {len(doors)}")
    
    for i, door in enumerate(doors, 1):
        print(f"    Door #{i}: {door.Name or 'Unnamed'}")
    
    # 6. Space/Room Details
    print("\n🏠 SPACE DETAILS:")
    spaces = ifc.by_type("IfcSpace")
    print(f"  Total Spaces: {len(spaces)}")
    
    total_area = 0
    for i, space in enumerate(spaces, 1):
        print(f"\n  Space #{i}:")
        print(f"    Name: {space.Name or 'Unnamed'}")
        
        try:
            psets = ifcopenshell.util.element.get_psets(space)
            for pset_name, pset_data in psets.items():
                if isinstance(pset_data, dict):
                    for key, value in pset_data.items():
                        if 'area' in key.lower():
                            print(f"    {key}: {value}")
                            if isinstance(value, (int, float)):
                                total_area += value
        except:
            pass
    
    if total_area > 0:
        print(f"\n  Total Floor Area: {total_area} sqm")
    else:
        print(f"\n  ⚠️  No area data found in spaces")
    
    # 7. Quantity Sets
    print("\n📏 CHECKING FOR QUANTITY DATA:")
    has_quantities = False
    
    for wall in walls:
        try:
            # Check for IfcElementQuantity
            for definition in wall.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    prop_def = definition.RelatingPropertyDefinition
                    if prop_def.is_a('IfcElementQuantity'):
                        has_quantities = True
                        print(f"  ✓ Found quantity data in: {wall.Name or 'Unnamed Wall'}")
                        for quantity in prop_def.Quantities:
                            print(f"    - {quantity.Name}: {quantity[3]} {getattr(quantity, 'Unit', '')}")
        except:
            pass
    
    if not has_quantities:
        print("  ⚠️  No IfcElementQuantity data found")
        print("  ℹ️  This means area/volume calculations need to be computed from geometry")
    
    print("\n" + "=" * 70)
    print("INSPECTION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspect_ifc.py <path_to_ifc_file>")
        print("Example: python inspect_ifc.py sample_building.ifc")
        sys.exit(1)
    
    inspect_ifc_file(sys.argv[1])
