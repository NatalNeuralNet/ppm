from db import personal_data_collection, notes_collection

def get_values(_id):
    return {
        "_id": _id, 
        "general": {
            "name": "",
            "current_college": "Merced College",
            "gpa": 3.0
        },
        "goals": ["Transfer"],
        "completed_courses": {
            "math": "",
            "science": "",
            "english": "",
            "general_ed": "",
            "major_specific": "",  # Corrected typo
            "other": ""
        }
    }

def create_profile(_id):
    profile_values = get_values(_id)
    profile_values["completed_courses"] = {  # Ensure correct structure
        "math": "",
        "science": "",
        "english": "",
        "general_ed": "",
        "major_specific": "",
        "other": "",
    }
    result = personal_data_collection.insert_one(profile_values)
    return result.inserted_id, profile_values  # Return the profile data

def get_profile(_id):
    profile = personal_data_collection.find_one({"_id": {"$eq": _id}})
    return profile if profile else get_values(_id)  # Fall back to default

def get_notes(_id):
    notes = list(notes_collection.find({"user_id": {"$eq": _id}}))
    return [{"_id": str(note["_id"]), "text": note.get("text", "")} for note in notes]
