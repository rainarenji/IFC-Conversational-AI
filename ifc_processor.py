"""
IFC Processor - Handles IFC file parsing and data extraction
"""

import ifcopenshell
import ifcopenshell.util.element
from typing import Dict, List, Any, Optional
import re


class IFCProcessor:
    """Processes IFC files and extracts building information"""
    
    def __init__(self, file_path: str):
        """
        Initialize IFC Processor
        
        Args:
            file_path: Path to the IFC file
        """
        try:
            self.ifc_file = ifcopenshell.open(file_path)
            self.file_path = file_path
        except Exception as e:
            raise Exception(f"Failed to open IFC file: {str(e)}")
    
    def get_building_info(self) -> Dict[str, Any]:
        """
        Get basic building information
        
        Returns:
            Dictionary with building metadata
        """
        info = {
            "schema": self.ifc_file.schema,
            "project_name": "N/A",
            "building_name": "N/A",
            "site_name": "N/A"
        }
        
        # Get project
        projects = self.ifc_file.by_type("IfcProject")
        if projects:
            info["project_name"] = projects[0].Name or "Unnamed Project"
        
        # Get building
        buildings = self.ifc_file.by_type("IfcBuilding")
        if buildings:
            info["building_name"] = buildings[0].Name or "Unnamed Building"
        
        # Get site
        sites = self.ifc_file.by_type("IfcSite")
        if sites:
            info["site_name"] = sites[0].Name or "Unnamed Site"
        
        return info
    
    def get_elements_by_type(self, ifc_type: str) -> List[Any]:
        """
        Get all elements of a specific IFC type
        
        Args:
            ifc_type: IFC element type (e.g., "IfcWall", "IfcDoor")
            
        Returns:
            List of IFC elements
        """
        try:
            return self.ifc_file.by_type(ifc_type)
        except:
            return []
    
    def count_elements(self, ifc_type: str) -> int:
        """
        Count elements of a specific type
        
        Args:
            ifc_type: IFC element type
            
        Returns:
            Count of elements
        """
        return len(self.get_elements_by_type(ifc_type))
    
    def get_wall_info(self) -> Dict[str, Any]:
        """
        Get detailed information about walls
        
        Returns:
            Dictionary with wall statistics and details
        """
        walls = self.get_elements_by_type("IfcWall")
        
        info = {
            "total_walls": len(walls),
            "walls": []
        }
        
        for wall in walls:
            wall_data = {
                "name": wall.Name or "Unnamed Wall",
                "global_id": wall.GlobalId,
                "type": wall.is_a()
            }
            
            # Get properties
            try:
                psets = ifcopenshell.util.element.get_psets(wall)
                wall_data["properties"] = psets
            except:
                wall_data["properties"] = {}
            
            info["walls"].append(wall_data)
        
        return info
    
    def calculate_plastering_area(self) -> Dict[str, Any]:
        """
        Calculate total plastering area from walls
        
        Returns:
            Dictionary with plastering calculations including data source and confidence
        """
        walls = self.get_elements_by_type("IfcWall")
        
        result = {
            "total_walls": len(walls),
            "total_area": 0.0,
            "unit": "square meters",
            "walls_with_area": 0,
            "data_source": "NONE",  # Track where data comes from
            "confidence": "LOW",     # Indicate reliability
            "note": ""
        }
        
        # If no walls, return immediately
        if len(walls) == 0:
            result["note"] = "⚠️ No walls found in the IFC file."
            result["data_source"] = "NONE"
            result["confidence"] = "NONE"
            return result
        
        # METHOD 1: Try to get IfcElementQuantity (most reliable)
        for wall in walls:
            try:
                for definition in wall.IsDefinedBy:
                    if definition.is_a('IfcRelDefinesByProperties'):
                        prop_def = definition.RelatingPropertyDefinition
                        if prop_def.is_a('IfcElementQuantity'):
                            for quantity in prop_def.Quantities:
                                if quantity.is_a('IfcQuantityArea'):
                                    # Found explicit quantity data
                                    result["total_area"] += float(quantity.AreaValue)
                                    result["walls_with_area"] += 1
                                    result["data_source"] = "IFC_ELEMENT_QUANTITY"
                                    result["confidence"] = "HIGH"
            except Exception as e:
                continue
        
        # METHOD 2: Try property sets if no IfcElementQuantity found
        if result["total_area"] == 0:
            for wall in walls:
                try:
                    psets = ifcopenshell.util.element.get_psets(wall)
                    
                    # Look for area in property sets
                    for pset_name, pset_data in psets.items():
                        if isinstance(pset_data, dict):
                            for key, value in pset_data.items():
                                if 'area' in key.lower() and isinstance(value, (int, float)):
                                    result["total_area"] += float(value)
                                    result["walls_with_area"] += 1
                                    result["data_source"] = "IFC_PROPERTY_SETS"
                                    result["confidence"] = "MEDIUM"
                                    break
                except Exception as e:
                    continue
        
        # Final result evaluation
        if result["total_area"] > 0:
            if result["walls_with_area"] == len(walls):
                result["note"] = f"✓ Found area data for all {len(walls)} walls from {result['data_source']}"
            else:
                result["note"] = f"⚠️ Found area data for {result['walls_with_area']} out of {len(walls)} walls from {result['data_source']}"
                result["confidence"] = "MEDIUM"  # Downgrade if incomplete
        else:
            # NO DATA FOUND
            result["note"] = (
                f"⚠️ NO AREA DATA FOUND IN IFC FILE\n"
                f"  • The file contains {len(walls)} wall(s) but lacks dimensional data\n"
                f"  • Missing: IfcElementQuantity and area properties\n"
                f"  • The walls have geometry but no parametric measurements\n"
                f"  • Cannot calculate plastering area without this data"
            )
            result["data_source"] = "NONE"
            result["confidence"] = "NONE"
        
        return result
    
    def get_door_info(self) -> Dict[str, Any]:
        """Get information about doors"""
        doors = self.get_elements_by_type("IfcDoor")
        
        return {
            "total_doors": len(doors),
            "doors": [
                {
                    "name": door.Name or "Unnamed Door",
                    "id": door.GlobalId
                }
                for door in doors
            ]
        }
    
    def get_window_info(self) -> Dict[str, Any]:
        """Get information about windows"""
        windows = self.get_elements_by_type("IfcWindow")
        
        return {
            "total_windows": len(windows),
            "windows": [
                {
                    "name": window.Name or "Unnamed Window",
                    "id": window.GlobalId
                }
                for window in windows
            ]
        }
    
    def get_space_info(self) -> Dict[str, Any]:
        """Get information about spaces/rooms"""
        spaces = self.get_elements_by_type("IfcSpace")
        
        result = {
            "total_spaces": len(spaces),
            "total_area": 0.0,
            "spaces": [],
            "data_source": "NONE",
            "confidence": "LOW"
        }
        
        if len(spaces) == 0:
            return result
        
        for space in spaces:
            space_data = {
                "name": space.Name or "Unnamed Space",
                "id": space.GlobalId
            }
            
            try:
                # Try IfcElementQuantity first
                for definition in space.IsDefinedBy:
                    if definition.is_a('IfcRelDefinesByProperties'):
                        prop_def = definition.RelatingPropertyDefinition
                        if prop_def.is_a('IfcElementQuantity'):
                            for quantity in prop_def.Quantities:
                                if quantity.is_a('IfcQuantityArea'):
                                    result["total_area"] += float(quantity.AreaValue)
                                    result["data_source"] = "IFC_ELEMENT_QUANTITY"
                                    result["confidence"] = "HIGH"
                
                # Fallback to property sets
                if result["total_area"] == 0:
                    psets = ifcopenshell.util.element.get_psets(space)
                    space_data["properties"] = psets
                    
                    for pset_name, pset_data in psets.items():
                        if isinstance(pset_data, dict):
                            for key, value in pset_data.items():
                                if 'area' in key.lower() and isinstance(value, (int, float)):
                                    result["total_area"] += float(value)
                                    result["data_source"] = "IFC_PROPERTY_SETS"
                                    result["confidence"] = "MEDIUM"
                                    break
            except:
                pass
            
            result["spaces"].append(space_data)
        
        return result

    def calculate_plastering_volume(self, thickness_mm: float, num_coats: int, material_type: str = "plaster") -> Dict[str, Any]:
        """
        Calculate plastering/painting volume based on wall area and specifications

        Args:
            thickness_mm: Material thickness per coat in millimeters
            num_coats: Number of coats to apply
            material_type: Type of material ("plaster" or "paint")

        Returns:
            Dictionary with calculation results
        """
        plastering_data = self.calculate_plastering_area()

        if plastering_data['total_area'] == 0:
            return {
                "success": False,
                "error": "No wall area data available in IFC file",
                "volume": 0,
                "details": plastering_data
            }

        # Convert thickness to meters
        thickness_per_coat_m = thickness_mm / 1000.0
        total_thickness_m = thickness_per_coat_m * num_coats

        # Calculate volume
        area_sqm = plastering_data['total_area']
        volume_m3 = area_sqm * total_thickness_m

        # Also calculate in liters (1 m³ = 1000 liters)
        volume_liters = volume_m3 * 1000

        return {
            "success": True,
            "material_type": material_type,
            "wall_area_sqm": area_sqm,
            "thickness_per_coat_mm": thickness_mm,
            "thickness_per_coat_m": thickness_per_coat_m,
            "num_coats": num_coats,
            "total_thickness_mm": thickness_mm * num_coats,
            "total_thickness_m": total_thickness_m,
            "volume_m3": round(volume_m3, 4),
            "volume_liters": round(volume_liters, 2),
            "calculation": f"{area_sqm} sqm × {total_thickness_m}m = {round(volume_m3, 4)} m³",
            "data_source": plastering_data['data_source'],
            "confidence": plastering_data['confidence']
        }

    def extract_plastering_specs(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Extract plastering specifications from user query

        Args:
            query: User's query string

        Returns:
            Dictionary with thickness and coats, or None if not found
        """
        query_lower = query.lower()

        # Extract thickness (look for patterns like "2mm", "3 mm", "5mm thick")
        thickness_match = re.search(r'(\d+\.?\d*)\s*mm', query_lower)
        thickness = float(thickness_match.group(1)) if thickness_match else None

        # Extract number of coats (look for patterns like "2 coats", "3 coat", "two coats")
        coat_match = re.search(r'(\d+)\s*coats?', query_lower)
        num_coats = int(coat_match.group(1)) if coat_match else None

        # Word-based numbers for coats
        word_numbers = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'single': 1, 'double': 2, 'triple': 3
        }
        if not num_coats:
            for word, number in word_numbers.items():
                if f'{word} coat' in query_lower:
                    num_coats = number
                    break

        if thickness and num_coats:
            return {
                "thickness_mm": thickness,
                "num_coats": num_coats
            }

        return None

    def process_query(self, query: str) -> str:
        """
        Process a user query and return relevant context with data quality indicators
        
        Args:
            query: User's natural language query
            
        Returns:
            Formatted context string for the LLM
        """
        query_lower = query.lower()
        context_parts = []
        
        # Building info is always relevant
        building_info = self.get_building_info()
        context_parts.append(f"Building: {building_info['building_name']}")
        context_parts.append(f"Project: {building_info['project_name']}")
        
        # Detect query intent and add relevant data
        if any(word in query_lower for word in ['plaster', 'plastering', 'wall area', 'paint']):
            # Determine material type
            material_type = "paint" if "paint" in query_lower else "plaster"

            # Check if user provided specific specifications
            specs = self.extract_plastering_specs(query)

            if specs:
                # User provided specifications - do the calculation
                calc_result = self.calculate_plastering_volume(
                    specs['thickness_mm'],
                    specs['num_coats'],
                    material_type
                )

                if calc_result['success']:
                    material_name = material_type.upper()
                    context_parts.append(f"\n🎯 ANSWER TO USER'S QUESTION:")
                    context_parts.append(f"\n📊 FINAL RESULT - {material_name} VOLUME NEEDED:")
                    context_parts.append(f"  ✓ {calc_result['volume_m3']} cubic meters")
                    context_parts.append(f"  ✓ {calc_result['volume_liters']} liters")
                    context_parts.append(f"\nCalculation details:")
                    context_parts.append(f"  - Wall area: {calc_result['wall_area_sqm']} sqm (from IFC file)")
                    context_parts.append(f"  - Thickness per coat: {calc_result['thickness_per_coat_mm']} mm")
                    context_parts.append(f"  - Number of coats: {calc_result['num_coats']}")
                    context_parts.append(f"  - Formula: {calc_result['calculation']}")
                    context_parts.append(f"\n⚠️ INSTRUCTION: Report the result above directly to the user. The calculation is complete.")
                else:
                    context_parts.append(f"\n--- {material_type.upper()} CALCULATION ERROR ---")
                    context_parts.append(f"Error: {calc_result['error']}")
            else:
                # No specifications - just provide area data
                plastering = self.calculate_plastering_area()
                context_parts.append(f"\n--- PLASTERING/WALL AREA DATA ---")
                context_parts.append(f"Total walls: {plastering['total_walls']}")
                context_parts.append(f"Total wall surface area: {plastering['total_area']} {plastering['unit']}")
                context_parts.append(f"Walls with data: {plastering['walls_with_area']}")
                context_parts.append(f"Data source: {plastering['data_source']}")
                context_parts.append(f"Confidence: {plastering['confidence']}")
                context_parts.append(f"Note: {plastering['note']}")
                context_parts.append(f"\n⚠️ IMPORTANT: The wall surface area above is from the IFC file.")
                context_parts.append(f"✓ ALLOWED: You may perform calculations using this area with specifications provided by the user.")
                context_parts.append(f"✓ ALLOWED: If user provides plaster thickness/coats, calculate: Volume = Area × Total_Thickness")
        
        elif any(word in query_lower for word in ['wall', 'walls']):
            wall_info = self.get_wall_info()
            context_parts.append(f"\n--- WALL INFORMATION ---")
            context_parts.append(f"Total walls: {wall_info['total_walls']}")
            if wall_info['walls']:
                context_parts.append(f"Wall names: {', '.join([w['name'] for w in wall_info['walls'][:5]])}")
        
        elif any(word in query_lower for word in ['door', 'doors']):
            door_info = self.get_door_info()
            context_parts.append(f"\n--- DOOR INFORMATION ---")
            context_parts.append(f"Total doors: {door_info['total_doors']}")
            if door_info['doors']:
                context_parts.append(f"Door names: {', '.join([d['name'] for d in door_info['doors'][:5]])}")
        
        elif any(word in query_lower for word in ['window', 'windows']):
            window_info = self.get_window_info()
            context_parts.append(f"\n--- WINDOW INFORMATION ---")
            context_parts.append(f"Total windows: {window_info['total_windows']}")
            if window_info['windows']:
                context_parts.append(f"Window names: {', '.join([w['name'] for w in window_info['windows'][:5]])}")
        
        elif any(word in query_lower for word in ['space', 'room', 'area', 'floor']):
            space_info = self.get_space_info()
            context_parts.append(f"\n--- SPACE/ROOM INFORMATION ---")
            context_parts.append(f"Total spaces: {space_info['total_spaces']}")
            context_parts.append(f"Total floor area: {space_info['total_area']} sqm")
            context_parts.append(f"Data source: {space_info.get('data_source', 'UNKNOWN')}")
            context_parts.append(f"Confidence: {space_info.get('confidence', 'UNKNOWN')}")
        
        else:
            # General query - provide summary
            context_parts.append(f"\n--- BUILDING SUMMARY ---")
            context_parts.append(f"Walls: {self.count_elements('IfcWall')}")
            context_parts.append(f"Doors: {self.count_elements('IfcDoor')}")
            context_parts.append(f"Windows: {self.count_elements('IfcWindow')}")
            context_parts.append(f"Spaces: {self.count_elements('IfcSpace')}")
            context_parts.append(f"Slabs: {self.count_elements('IfcSlab')}")
        
        return "\n".join(context_parts)