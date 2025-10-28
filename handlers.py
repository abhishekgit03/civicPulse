from mongo_client import complaints_collection
from datetime import datetime
from bson import ObjectId

def create_complaint(complaint_data: dict) -> str:
    """Create a new complaint document in MongoDB with required fields"""
    required_fields = {
        'resident_name': str,
        'block': str,
        'description': str,
        'category': str,
        'sentiment': str,
        'severity_level': str,
        'urgency_score': int,
        'llm_summary': str,
        'action_recommendation': str,
        'status': str
    }

    # Validate required fields
    for field, field_type in required_fields.items():
        if field not in complaint_data:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(complaint_data[field], field_type):
            raise TypeError(f"Invalid type for {field}. Expected {field_type}")

    # Add timestamps
    complaint_data['created_at'] = datetime.utcnow()
    complaint_data['updated_at'] = datetime.utcnow()

    result = complaints_collection.insert_one(complaint_data)
    return str(result.inserted_id)

def get_complaint(complaint_id: str) -> dict:
    """Retrieve a single complaint by ID"""
    try:
        complaint = complaints_collection.find_one({'_id': ObjectId(complaint_id)})
        return complaint if complaint else {}
    except:
        return {}

def get_all_complaints(query: dict = None) -> list:
    """Retrieve all complaints, optionally filtered by query"""
    if query is None:
        query = {}
    return list(complaints_collection.find(query))

def update_complaint(complaint_id: str, update_data: dict) -> bool:
    """Update an existing complaint"""
    try:
        update_data['updated_at'] = datetime.utcnow()
        result = complaints_collection.update_one(
            {'_id': ObjectId(complaint_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    except:
        return False

def delete_complaint(complaint_id: str) -> bool:
    """Delete a complaint by ID"""
    try:
        result = complaints_collection.delete_one({'_id': ObjectId(complaint_id)})
        return result.deleted_count > 0
    except:
        return False

# Example usage/testing
if __name__ == "__main__":
    # Sample complaint data
    sample_complaint = {
        "resident_name": "John Doe",
        "block": "B-123",
        "description": "Water leakage in kitchen pipeline causing dampness in walls",
        "category": "Water",
        "sentiment": "negative",
        "severity_level": "high",
        "urgency_score": 8,
        "llm_summary": "Urgent water leakage issue in kitchen requiring immediate plumbing intervention",
        "action_recommendation": "Dispatch plumbing team for immediate inspection and repair",
        "status": "open"
    }

    try:
        # Create a test complaint
        new_complaint_id = create_complaint(sample_complaint)
        print(f"Created test complaint with ID: {new_complaint_id}")
    except Exception as e:
        print(f"Error creating test complaint: {str(e)}")