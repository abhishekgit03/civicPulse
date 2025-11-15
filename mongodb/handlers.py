from mongodb.mongo_client import complaints_collection
from datetime import datetime
from bson import ObjectId
from typing import List
from llm.chat import embed_generator
from llm import agents  # ✅ Import agents for summary generation


# =====================================================
# ✅ Create a new complaint
# =====================================================
def create_complaint(complaint_data: dict) -> str:
    required_fields = {
        "resident_name": str,
        "block": str,
        "description": str,
        "category": str,
        "sentiment": str,
        "severity_level": str,
        "urgency_score": int,
        "llm_summary": str,
        "action_recommendation": str,
        "embedding": list,
        "status": str
    }

    # Validation
    for field, field_type in required_fields.items():
        if field not in complaint_data:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(complaint_data[field], field_type):
            raise TypeError(f"Invalid type for {field}. Expected {field_type}")

    # ✅ Generate and attach AI summary (only once)
    try:
        if "summary" not in complaint_data or not complaint_data["summary"]:
            complaint_data["summary"] = agents.generate_complaint_summary(
                complaint_data.get("description", "")
            )
    except Exception as e:
        print(f"Error generating summary during complaint creation: {e}")
        complaint_data["summary"] = "Summary temporarily unavailable."

    # Add timestamps
    complaint_data["created_at"] = datetime.utcnow()
    complaint_data["updated_at"] = datetime.utcnow()

    result = complaints_collection.insert_one(complaint_data)
    return str(result.inserted_id)


# =====================================================
# ✅ Retrieve a single complaint
# =====================================================
def get_complaint(complaint_id: str) -> dict:
    try:
        return complaints_collection.find_one({"_id": ObjectId(complaint_id)}) or {}
    except Exception as e:
        print(f"Error fetching complaint: {e}")
        return {}


# =====================================================
# ✅ Retrieve all complaints
# =====================================================
def get_all_complaints(query: dict = None) -> list:
    try:
        return list(complaints_collection.find(query or {}))
    except Exception as e:
        print(f"Error fetching complaints: {e}")
        return []


# =====================================================
# ✅ Update complaint details (Regenerate summary if description changes)
# =====================================================
def update_complaint(complaint_id: str, update_data: dict) -> bool:
    """
    Updates a complaint. If the description changes, regenerate the AI summary.
    """
    try:
        update_data["updated_at"] = datetime.utcnow()

        # ✅ Fetch the old complaint data to compare description
        old_complaint = complaints_collection.find_one({"_id": ObjectId(complaint_id)})
        old_description = old_complaint.get("description") if old_complaint else None
        new_description = update_data.get("description")

        # ✅ If description changed → regenerate summary
        if new_description and new_description != old_description:
            try:
                update_data["summary"] = agents.generate_complaint_summary(new_description)
            except Exception as e:
                print(f"Error regenerating summary on update: {e}")
                update_data["summary"] = "Summary temporarily unavailable."

        result = complaints_collection.update_one(
            {"_id": ObjectId(complaint_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    except Exception as e:
        print(f"Error updating complaint: {e}")
        return False


# =====================================================
# ✅ Delete a complaint
# =====================================================
def delete_complaint(complaint_id: str) -> bool:
    try:
        result = complaints_collection.delete_one({"_id": ObjectId(complaint_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Error deleting complaint: {e}")
        return False


# =====================================================
# ✅ Get complaints by status
# =====================================================
def get_complaints_by_status(status: str) -> list:
    try:
        return list(complaints_collection.find({"status": status}))
    except Exception as e:
        print(f"Error fetching complaints by status: {e}")
        return []


# =====================================================
# ✅ Update complaint status (Pending → Resolved/Junk)
# =====================================================
def update_complaint_status(complaint_id: str, new_status: str, extra_fields: dict = None) -> bool:
    """
    Updates complaint status and timestamps.
    Supports optional extra_fields (e.g., resolved_at).
    """
    try:
        update_fields = {
            "status": new_status,
            "updated_at": datetime.utcnow()
        }

        # Merge any additional fields like resolved_at or updated_at
        if extra_fields:
            update_fields.update(extra_fields)

        # Automatically add resolved_at if status is 'closed' and not provided
        if new_status == "closed" and "resolved_at" not in update_fields:
            update_fields["resolved_at"] = datetime.utcnow()

        result = complaints_collection.update_one(
            {"_id": ObjectId(complaint_id)},
            {"$set": update_fields}
        )

        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating complaint status: {e}")
        return False
