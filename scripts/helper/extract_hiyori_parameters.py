"""
Live2D Model Parameter Extractor for Hiyori

This script parses the Hiyori Live2D model files and extracts all
available parameters with their IDs, min/max values, and defaults.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


def extract_parameters_from_cdi3(cdi3_path: str) -> List[Dict[str, Any]]:
    """
    Extract parameters from .cdi3.json file.
    
    Args:
        cdi3_path: Path to the .cdi3.json file
        
    Returns:
        List of parameter dictionaries
    """
    with open(cdi3_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    parameters = []
    
    if 'Parameters' in data:
        for param in data['Parameters']:
            param_info = {
                'id': param.get('Id', 'Unknown'),
                'name': param.get('Name', param.get('Id', 'Unknown')),
                'min': param.get('MinValue', param.get('Min', 0.0)),
                'max': param.get('MaxValue', param.get('Max', 1.0)),
                'default': param.get('DefaultValue', param.get('Default', 0.0))
            }
            
            # Add description if available
            if 'Description' in param:
                param_info['description'] = param['Description']
            
            parameters.append(param_info)
    
    return parameters


def extract_from_model3(model3_path: str) -> Dict[str, Any]:
    """
    Extract basic info from .model3.json file.
    
    Args:
        model3_path: Path to the .model3.json file
        
    Returns:
        Model configuration dictionary
    """
    with open(model3_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data


def generate_markdown_table(parameters: List[Dict[str, Any]]) -> str:
    """
    Generate a Markdown table from parameters list.
    
    Args:
        parameters: List of parameter dictionaries
        
    Returns:
        Markdown formatted table string
    """
    md = "# Hiyori Live2D Model - Parameter Reference\n\n"
    md += f"**Total Parameters**: {len(parameters)}\n\n"
    md += "| Parameter ID | Min | Max | Default | Description |\n"
    md += "|--------------|-----|-----|---------|-------------|\n"
    
    for param in sorted(parameters, key=lambda p: p['id']):
        param_id = param['id']
        min_val = param['min']
        max_val = param['max']
        default_val = param['default']
        desc = param.get('description', '-')
        
        md += f"| `{param_id}` | {min_val} | {max_val} | {default_val} | {desc} |\n"
    
    return md


def generate_json_list(parameters: List[Dict[str, Any]]) -> str:
    """
    Generate a JSON formatted list of parameters.
    
    Args:
        parameters: List of parameter dictionaries
        
    Returns:
        JSON formatted string
    """
    return json.dumps(parameters, indent=2, ensure_ascii=False)


def main():
    """Main execution function."""
    # Define paths
    model_dir = Path(r"D:\hiyori_vts")
    cdi3_file = model_dir / "hiyori.cdi3.json"
    model3_file = model_dir / "hiyori.model3.json"
    
    print("=" * 70)
    print("HIYORI LIVE2D MODEL PARAMETER EXTRACTOR")
    print("=" * 70)
    
    # Check if files exist
    if not cdi3_file.exists():
        print(f"❌ Error: {cdi3_file} not found!")
        return
    
    if not model3_file.exists():
        print(f"⚠ Warning: {model3_file} not found!")
    else:
        print(f"✓ Found model3.json")
    
    print(f"✓ Found cdi3.json\n")
    
    # Extract parameters
    print("Extracting parameters from cdi3.json...")
    parameters = extract_parameters_from_cdi3(str(cdi3_file))
    
    print(f"✓ Extracted {len(parameters)} parameters\n")
    
    # Generate outputs
    print("Generating Markdown table...")
    markdown_output = generate_markdown_table(parameters)
    
    print("Generating JSON list...")
    json_output = generate_json_list(parameters)
    
    # Save to files
    output_dir = Path(r"d:\aigirlfriend\model_control")
    
    md_file = output_dir / "hiyori_parameters.md"
    json_file = output_dir / "hiyori_parameters.json"
    
    print(f"\nSaving to {md_file}...")
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(markdown_output)
    
    print(f"Saving to {json_file}...")
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json_output)
    
    print("\n" + "=" * 70)
    print("EXTRACTION COMPLETE!")
    print("=" * 70)
    print(f"\nGenerated files:")
    print(f"  1. {md_file}")
    print(f"  2. {json_file}")
    
    # Print preview
    print("\n" + "-" * 70)
    print("PARAMETER PREVIEW (first 10):")
    print("-" * 70)
    
    for i, param in enumerate(parameters[:10], 1):
        print(f"{i}. {param['id']:<30} Range: [{param['min']:>6.1f}, {param['max']:>6.1f}]  Default: {param['default']:>6.1f}")
    
    if len(parameters) > 10:
        print(f"... and {len(parameters) - 10} more parameters")
    
    print("\n✅ All parameters documented!")


if __name__ == "__main__":
    main()
