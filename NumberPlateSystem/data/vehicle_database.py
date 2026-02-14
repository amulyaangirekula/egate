"""
Database operations for registered vehicles
"""
import json
import os
from datetime import datetime
from NumberPlateSystem.config import DATA_FILE

def load_database():
    """
    Load vehicle database from file
    
    Returns:
        List of registered vehicle entries
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading database: {e}")
            return []
    else:
        return []

def save_database(data):
    """
    Save vehicle database to file
    
    Args:
        data: List of vehicle entries
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
            
        return True
    except IOError as e:
        print(f"Error saving database: {e}")
        return False

def register_vehicle(plate):
    """
    Register a new vehicle in database
    
    Args:
        plate: Plate number text
        
    Returns:
        Dict with registration result
    """
    # Load current database
    registered_data = load_database()
    
    # Check if already registered
    if plate in [entry['plate'] for entry in registered_data]:
        return {
            'success': False,
            'message': 'Plate already registered'
        }
    
    # Add new entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {"plate": plate, "registered_at": timestamp}
    registered_data.append(new_entry)
    
    # Save updated database
    save_database(registered_data)
    
    return {
        'success': True,
        'message': 'Plate registered successfully',
        'timestamp': timestamp
    }

def verify_vehicle(plate):
    """
    Verify if a vehicle is registered
    
    Args:
        plate: Plate number text
        
    Returns:
        Dict with verification result
    """
    # Load current database
    registered_data = load_database()
    
    # Check if plate exists
    for entry in registered_data:
        if entry['plate'] == plate:
            return {
                'exists': True,
                'registered_at': entry.get('registered_at', 'Unknown')
            }
    
    return {
        'exists': False
    }

def get_all_vehicles():
    """
    Get all registered vehicles
    
    Returns:
        List of all vehicle entries
    """
    return load_database()

def remove_vehicle(plate):
    """
    Remove a vehicle from database
    
    Args:
        plate: Plate number text
        
    Returns:
        Boolean indicating success
    """
    # Load current database
    registered_data = load_database()
    
    # Filter out the entry
    updated_data = [entry for entry in registered_data if entry['plate'] != plate]
    
    # Check if any entry was removed
    if len(updated_data) < len(registered_data):
        save_database(updated_data)
        return True
    
    return False