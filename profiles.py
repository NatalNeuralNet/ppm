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
            "math" : "",
            "science" : "",
            "english" : "",
            "general_ed": "",
            "major_specfic": "",
            "other" : ""
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
    return result.inserted_id, result

def get_profile(_id):
    return personal_data_collection.find_one({"_id": {"$eq": _id}})

def get_notes(_id):
    return list(notes_collection.find({"user_id": {"$eq": _id}}))