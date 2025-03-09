# Password Strength Checker
# Written by Prashis (that's me!) :)

import re
import math
import tkinter as tk
from tkinter import messagebox

# List of common passwords (because people still use "password" as their password...)
COMMON_PASSWORDS = ["password", "123456", "qwerty", "admin", "letmein"]

# Function to check the length of the password
def check_length(password):
    if len(password) < 8:
        return "Weak"  # Too short, my dude!
    elif len(password) < 12:
        return "Medium"  # Not bad, but could be better
    else:
        return "Strong"  # Now we're talking!

# Function to check the complexity of the password
def check_complexity(password):
    score = 0
    if re.search(r'[A-Z]', password):  # Uppercase letters? Nice!
        score += 1
    if re.search(r'[a-z]', password):  # Lowercase letters? Cool!
        score += 1
    if re.search(r'[0-9]', password):  # Numbers? Smart move!
        score += 1
    if re.search(r'[^A-Za-z0-9]', password):  # Special characters? Awesome!
        score += 1
    return score

# Function to check if the password is too common
def check_common(password):
    return password.lower() in COMMON_PASSWORDS  # Please don't use "password123"...

# Function to calculate the entropy of the password (because math is fun!)
def calculate_entropy(password):
    # Determine the character set size
    char_set = 0
    if re.search(r'[a-z]', password):
        char_set += 26  # Lowercase letters
    if re.search(r'[A-Z]', password):
        char_set += 26  # Uppercase letters
    if re.search(r'[0-9]', password):
        char_set += 10  # Numbers
    if re.search(r'[^A-Za-z0-9]', password):
        char_set += 32  # Special characters (I assumed 32 common ones)
    
    # Calculate entropy (because randomness is cool)
    entropy = len(password) * math.log2(char_set) if char_set > 0 else 0
    return entropy

# Function to assess the overall strength of the password
def assess_password_strength(password):
    # Check length
    length_score = check_length(password)
    # Check complexity
    complexity_score = check_complexity(password)
    # Check if password is common
    is_common = check_common(password)
    # Calculate entropy
    entropy = calculate_entropy(password)
    
    # Determine overall strength
    if is_common or length_score == "Weak":
        return "Weak"  # Yikes, this password needs work!
    elif length_score == "Medium" and complexity_score >= 2:
        return "Medium"  # It's okay, but not great
    elif length_score == "Strong" and complexity_score >= 3 and entropy > 50:
        return "Strong"  # Now that's a solid password!
    else:
        return "Medium"  # Meh, it's alright

# Function to provide feedback on how to improve the password
def provide_feedback(password):
    strength = assess_password_strength(password)
    feedback = []
    
    if len(password) < 8:
        feedback.append("Password is too short. Use at least 8 characters.")
    if check_complexity(password) < 3:
        feedback.append("Add more character types (uppercase, lowercase, numbers, special characters).")
    if check_common(password):
        feedback.append("Avoid using common passwords.")
    if calculate_entropy(password) <= 50:
        feedback.append("Increase password randomness.")
    
    return strength, feedback

# UI Functionality
def check_password():
    password = password_entry.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")  # Don't leave it blank!
        return
    
    strength, feedback = provide_feedback(password)
    result_text = f"Password Strength: {strength}\n\n"
    if feedback:
        result_text += "Suggestions to improve:\n"
        for suggestion in feedback:
            result_text += f"- {suggestion}\n"
    
    result_label.config(text=result_text)

# Create the main window
root = tk.Tk()
root.title("Password Strength Checker - By Prashis")

# Create and place widgets
tk.Label(root, text="Enter your password:").pack(pady=10)
password_entry = tk.Entry(root, width=40)  # No 'show="*"' parameter (because I want to see what I type!)
password_entry.pack(pady=10)

tk.Button(root, text="Check Strength", command=check_password).pack(pady=10)

result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack(pady=10)

# Run the application
root.mainloop()