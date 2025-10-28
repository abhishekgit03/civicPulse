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

def get_user_complaint_data():
    """Get complaint data from user input"""
    return {
        "resident_name": input("Enter resident name: "),
        "block": input("Enter block number: "),
        "description": input("Enter complaint description: "),
        "category": input("Enter category (Water/Electricity/Sanitation/Other): "),
        "sentiment": input("Enter sentiment (positive/negative/neutral): "),
        "severity_level": input("Enter severity level (low/medium/high): "),
        "urgency_score": int(input("Enter urgency score (0-10): ")),
        "llm_summary": input("Enter LLM summary: "),
        "action_recommendation": input("Enter action recommendation: "),
        "status": input("Enter status (open/in_progress/resolved): ")
    }

# Example usage/testing
if __name__ == "__main__":
    while True:
        print("\nCivic Pulse Complaint Management System")
        print("1. Create new complaint")
        print("2. View complaint by ID")
        print("3. View all complaints")
        print("4. Update complaint")
        print("5. Delete complaint")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        try:
            if choice == "1":
                complaint_data = get_user_complaint_data()
                new_id = create_complaint(complaint_data)
                print(f"Created complaint with ID: {new_id}")
                
            elif choice == "2":
                complaint_id = input("Enter complaint ID: ")
                complaint = get_complaint(complaint_id)
                print(f"Retrieved complaint: {complaint}")
                
            elif choice == "3":
                complaints = get_all_complaints()
                print(f"Total complaints: {len(complaints)}")
                for complaint in complaints:
                    print(f"\nID: {complaint['_id']}")
                    print(f"Resident: {complaint['resident_name']}")
                    print(f"Description: {complaint['description']}")
                    print("-" * 50)
                
            elif choice == "4":
                complaint_id = input("Enter complaint ID: ")
                new_status = input("Enter new status: ")
                success = update_complaint(complaint_id, {"status": new_status})
                print(f"Update successful: {success}")
                
            elif choice == "5":
                complaint_id = input("Enter complaint ID to delete: ")
                success = delete_complaint(complaint_id)
                print(f"Delete successful: {success}")
                
            elif choice == "6":
                print("Exiting program...")
                break
                
            else:
                print("Invalid choice! Please try again.")
                
        except Exception as e:
            print(f"Error: {str(e)}")