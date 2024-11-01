import os


def load_prompt(file_name):
    current_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(current_dir, '../prompts', file_name)
    with open(prompt_path, 'r') as file:
        return file.read()