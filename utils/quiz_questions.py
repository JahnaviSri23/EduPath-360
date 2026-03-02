quiz = [
    {"question": "Do you enjoy solving logical problems?", "options":["Yes","No"]},
    {"question": "Do you like working with numbers?", "options":["Yes","No"]},
    {"question": "Are you interested in arts & creativity?", "options":["Yes","No"]},
]

def calculate_career(answers):
    score = 0
    if answers.get("Do you enjoy solving logical problems?") == "Yes":
        score += 1
    if answers.get("Do you like working with numbers?") == "Yes":
        score += 1
    if answers.get("Are you interested in arts & creativity?") == "Yes":
        score -= 1

    if score >= 2:
        return "Science/Engineering"
    elif score == 1:
        return "Commerce/Business"
    else:
        return "Arts/Humanities"