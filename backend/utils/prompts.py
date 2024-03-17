def find_others_system_prompt():
    return f"""
    You will be given the summary what a certain employee has been doing today. Your job is to rank the most similar employees based on the summaries of their workdays, 
    which will be provided later in a JSON list.
    OUTPUT ONLY THE UUIDs THAT ARE ASSOCIATED WITH THE SELECTED EMPLOYEES. NOTHING ELSE.
    """

def find_others_user_prompt(target, neighbors):
    return f"""
    Here, deliminated by `, is a summary of what an employee has been doing all day:
    `{target}`

    You will also be given the day summary of all other employees at that company. Your goal is to rank the employees in the order of those having the most similar days.
    Here is a list of employees deliminated by `. In the list are summaries of their days in JSON format and entry is separated by a comma:
    `{neighbors}`

    OUTPUT ONLY THE ASSOCIATED UUIDs OF THE SELECTED EMPLOYEES. DO NOT GIVE ANY EXPLANATION OR REASONING

    Below is an example output:
    7, 9, 10
    """

