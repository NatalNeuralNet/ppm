import streamlit as st
import json
import requests
import os
from typing import Optional
from profiles import create_profile, get_notes, get_profile
from form_submit import update_personal_info, add_note, delete_note

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "5df6e6c4-2c67-4025-b1d0-b6b8c6004505"
ENDPOINT = "basic-prompting"  # The endpoint name of the flow
APPLICATION_TOKEN = os.environ.get("LANGFLOW_TOKEN")



TWEAKS = {
    "OpenAIModel-nRAJ5": {},
    "TextInput-GyuA6": {"input_value": ""},  # Placeholder for full prompt
    "AstraDB-fS6MU": {},
    "ParseData-gXwDN": {},
    "Prompt-iSdxN": {},
    "TextOutput-3q8AU": {},
}

def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level  # Indentation for nested levels
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")

    return ", ".join(strings)


def run_flow(profile_data: dict, question: str) -> str:
    """
    Run a flow with a given profile and question, and extract the AI-generated message.

    :param profile_data: The user profile data as input for context.
    :param question: The main question to send to the flow.
    :return: The AI-generated message as a string.
    """
    # Ensure completed_courses and notes are added to profile_data
    profile_data["completed_courses"] = profile_data.get("completed_courses", {})
    profile_data["notes"] = st.session_state.get("notes", [])

    # Construct the prompt with all data
    prompt = (
        f"Profile Data: {json.dumps(profile_data, indent=2)}\n"
        f"Question: {question}"
    )
    
    # API configuration
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": prompt,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    st.write("Profile Data Before Serialization:", profile_data)

    try:
        # Make API request
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        return json_response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")
    except (KeyError, IndexError) as e:
        raise ValueError(f"Could not extract AI message. Response format issue: {e}")



def ask_ai(profile_data: dict, question: str) -> str:
    """
    Prepare the input for LangFlow and use the run_flow function to get the AI's response.

    :param profile_data: The user profile data as input for context.
    :param question: The main question to send to the flow.
    :return: The AI-generated message as a string.
    """
    try:
        ai_response = run_flow(profile_data, question)
        return ai_response
    except RuntimeError as e:
        raise RuntimeError(f"Error during ask_ai execution: {e}")
    except ValueError as e:
        raise ValueError(f"Error in processing AI response: {e}")






