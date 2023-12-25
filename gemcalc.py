import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import re

# Initialize the main window
root = tk.Tk()
root.title("Gem Buff Calculator")
root.geometry("800x600")  # Set window size

# Gem 1 or T12 Emerald Dictionary
gem1_powers = {
    "T12 Emerald - Level 1": "34aj",
    "T12 Emerald - Level 2": "39.1aj",
    "T12 Emerald - Level 3": "44.2aj",
    "T12 Emerald - Level 4": "49.3aj",
    "T12 Emerald - Level 5": "54.4aj",
    "T12 Emerald - Level 6": "59.5aj",
    "T12 Emerald - Level 7": "64.6aj",
    "T12 Emerald - Level 8": "69.7aj",
    "T12 Emerald - Level 9": "74.8aj",
    "T12 Emerald - Level 10": "79.9aj"
}

# Gem 2 or T12 Ruby dictionary
gem2_powers = {
    "T12 Ruby - Level 1": 194,
    "T12 Ruby - Level 2": 223,
    "T12 Ruby - Level 3": 252,
    "T12 Ruby - Level 4": 281,
    "T12 Ruby - Level 5": 310,
    "T12 Ruby - Level 6": 339,
    "T12 Ruby - Level 7": 368,
    "T12 Ruby - Level 8": 397,
    "T12 Ruby - Level 9": 426,
    "T12 Ruby - Level 10": 455
}

gemstone_powder_investment = {
    1: 0,
    2: 0.4944,
    3: 0.4944 + 1.22,
    4: 0.4944 + 1.22 + 2.31,
    5: 0.4944 + 1.22 + 2.31 + 3.96,
    6: 0.4944 + 1.22 + 2.31 + 3.96 + 6.43,
    7: 0.4944 + 1.22 + 2.31 + 3.96 + 6.43 + 10.12,
    8: 0.4944 + 1.22 + 2.31 + 3.96 + 6.43 + 10.12 + 15.66,
    9: 0.4944 + 1.22 + 2.31 + 3.96 + 6.43 + 10.12 + 15.66 + 23.97,
    10: 0.4944 + 1.22 + 2.31 + 3.96 + 6.43 + 10.12 + 15.66 + 23.97 + 36.43,
}
# Convert all values to millions (M) for consistency
gemstone_powder_investment = {level: total * 1e6 for level, total in gemstone_powder_investment.items()}

# Function to update the label displaying the invested gemstone powder for the gem
def update_gemstone_powder_display(gem_label, selected_level_var):
    level = int(selected_level_var.get().split(' ')[-1])  # Extract the level number from the selected level string
    invested_powder = gemstone_powder_investment.get(level, 0)
    gem_label.config(text=f"Level {level} - Invested: {invested_powder:.1f} powder")

# Define the basic mapping
mapping = {
    'aa': 10**18, 'ab': 10**21, 'ac': 10**24, 'ad': 10**27, 'ae': 10**30,
    'af': 10**33, 'ag': 10**36, 'ah': 10**39, 'ai': 10**42, 'aj': 10**45,
    'ak': 10**48, 'al': 10**51, 'am': 10**54, 'an': 10**57, 'ao': 10**60
    # Add more mappings as needed
}
# Function to update the tool power with the custom input
def update_custom_tool_power():
    custom_power_str = custom_power_entry.get()
    if custom_power_str:
        try:
            # Validate and update the power of the selected tool
            custom_power_num = letter_to_number(custom_power_str)
            current_tool = selected_tool.get()
            tool_powers[current_tool] = custom_power_str  # Update the power for the selected tool

            # Update the label to show it's a custom version of the selected tool
            tool_label.config(text=f"Custom {current_tool}")

            update_tool_image()
        except ValueError:
            print("Invalid power format. Please input in the format 'x.xxaj'")
            
# Create an entry widget for custom power level input
custom_power_entry = tk.Entry(root)
custom_power_entry.grid(row=2, column=0, padx=10, pady=10)

# Create a button to submit the custom power level
submit_button = tk.Button(root, text="Submit Custom Power", command=update_custom_tool_power)
submit_button.grid(row=2, column=1, padx=10, pady=10)

# Function to convert letter notation to number
def letter_to_number(letter_str):
    # Split the numeric and alphabetic parts
    parts = re.split('(\d+\.\d+|\d+)', letter_str)
    parts = [p for p in parts if p]  # Remove empty strings
    if len(parts) == 2:
        numeric_part, alpha_part = parts
        numeric_value = float(numeric_part) * mapping.get(alpha_part, 1)
    else:
        print(f"Error in input string format: {letter_str}")
        return 0
    return numeric_value

# Function to convert number to letter notation
def number_to_letter(number):
    reverse_mapping = {v: k for k, v in mapping.items()}
    number_float = float(number)  # Convert number to float
    for power in sorted(reverse_mapping, reverse=True):
        if number_float >= power:  # Use number_float for comparison
            return f"{number_float / power:.2f}{reverse_mapping[power]}".rstrip('0').rstrip('.')
    return str(number_float)

# Function to load an image and resize it to fit a specific size
def load_image(path, size=(150, 150)):
    image = Image.open(path)
    image = image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

# Function to return the correct image path based on the tool name
def get_image_path(tool_name):
    paths = {
        "Gem 1": "images/t12Emerald.png",
        "Gem 2": "images/t12Ruby.png",
        "Christmas Hammer II": "images/Christmas_HammerII.png",
        "Christmas Pickaxe III": "images/Christmas_PickaxeIII.png",
        "Tool": "images/default.png",
    }
    return paths.get(tool_name, "images/default.png")


# Options for the Tools and their power levels
tool_options = ["Christmas Hammer II", "Christmas Pickaxe III", "Custom Tool"]
tool_powers = {
    "Christmas Hammer II": "597ai",
    "Christmas Pickaxe III": "1.79aj",
    "Custom Tool": ""
}

# Define the StringVar for the dropdown selections
selected_tool = tk.StringVar(value=tool_options[0])
selected_level_gem1 = tk.StringVar(value=list(gem1_powers.keys())[0])
selected_level_gem2 = tk.StringVar(value=list(gem2_powers.keys())[0])

# Update the tool image and power display
def update_tool_image(*args):
    tool_name = selected_tool.get()
    new_image_path = get_image_path(tool_name)
    new_tool_image = load_image(new_image_path)
    tool_image_label.configure(image=new_tool_image)
    tool_image_label.image = new_tool_image  # Keep a reference!


    # Retrieve and convert the powers of the selected tool and gems to numerical values
    tool_power_str = tool_powers.get(tool_name, "0")
    tool_power_num = letter_to_number(tool_power_str)

    gem1_level = f"T12 Emerald - Level {selected_level_gem1.get().split(' ')[-1]}"
    gem1_power_str = gem1_powers.get(gem1_level, "0")
    gem1_power_num = letter_to_number(gem1_power_str)

    gem2_level = f"T12 Ruby - Level {selected_level_gem2.get().split(' ')[-1]}"
    gem2_power_increase_percentage = gem2_powers.get(gem2_level, 0)

    # Ruby's percentage increase applied to the tool's base power
    tool_power_with_ruby = tool_power_num * (1 + gem2_power_increase_percentage / 100.0)

    # Total power is the tool's power after Ruby's increase plus Emerald's power
    total_combined_power = tool_power_with_ruby + gem1_power_num

    # Update the tool power label with the total combined power in letter notation
    total_combined_power_str = number_to_letter(total_combined_power)
    tool_power_label.config(text=f"Power: {total_combined_power_str}")

    # Debugging: Output each step of the calculation
    print(f"Tool Base Power: {tool_power_num} ({number_to_letter(tool_power_num)})")
    print(f"Ruby Gem % Increase: {gem2_power_increase_percentage}%")
    print(f"Tool Power with Ruby: {tool_power_with_ruby} ({number_to_letter(tool_power_with_ruby)})")
    print(f"Emerald Gem Power: {gem1_power_num} ({number_to_letter(gem1_power_num)})")
    print(f"Total Combined Power: {total_combined_power} ({total_combined_power_str})")

# Function to calculate power increase for Gem 1 (Emerald)
def calculate_power_increase_emerald(gem_power_dict, level):
    if level > 1:
        prev_power = letter_to_number(gem_power_dict[f"T12 Emerald - Level {level - 1}"])
        new_power = letter_to_number(gem_power_dict[f"T12 Emerald - Level {level}"])
        return new_power - prev_power
    return letter_to_number(gem_power_dict["T12 Emerald - Level 1"])

# Function to calculate power increase for Gem 2 (Ruby)
def calculate_power_increase_ruby(gem_power_dict, level, base_power):
    if level > 1:
        prev_percentage = gem_power_dict[f"T12 Ruby - Level {level - 1}"]
        new_percentage = gem_power_dict[f"T12 Ruby - Level {level}"]
        return base_power * (new_percentage - prev_percentage) / 100.0
    return base_power * gem_power_dict["T12 Ruby - Level 1"] / 100.0

def calculate_upgrade_cost(gemstone_powder_dict, level):
    return gemstone_powder_dict[level]

def recommend_next_upgrade():
    current_level_gem1 = int(selected_level_gem1.get().split(' ')[-1])
    current_level_gem2 = int(selected_level_gem2.get().split(' ')[-1])
    base_power_num = letter_to_number(tool_powers[selected_tool.get()])

    # Calculate power increase and upgrade cost for both gems
    power_increase_gem1 = calculate_power_increase_emerald(gem1_powers, current_level_gem1)
    upgrade_cost_gem1 = calculate_upgrade_cost(gemstone_powder_investment, current_level_gem1 + 1)
    
    power_increase_gem2 = calculate_power_increase_ruby(gem2_powers, current_level_gem2, base_power_num)
    upgrade_cost_gem2 = calculate_upgrade_cost(gemstone_powder_investment, current_level_gem2 + 1)

    # Calculate cost-effectiveness (power increase per powder invested)
    cost_effectiveness_gem1 = power_increase_gem1 / upgrade_cost_gem1
    cost_effectiveness_gem2 = power_increase_gem2 / upgrade_cost_gem2

    if cost_effectiveness_gem1 > cost_effectiveness_gem2:
        return f"Upgrade Gem 1 for better value: +{number_to_letter(power_increase_gem1)} power for {format_investment(upgrade_cost_gem1)} powder"
    else:
        return f"Upgrade Gem 2 for more power: +{number_to_letter(power_increase_gem2)} power for {format_investment(upgrade_cost_gem2)} powder"
    
# Function to update the recommendation label
def update_recommendation_label(*args):
    recommendation = recommend_next_upgrade()
    recommendation_label.config(text=recommendation)
    
# Function to format the invested gemstone powder into K or M
def format_investment(number):
    """
    Format the investment number into a string with K for thousand or M for million.
    """
    if number >= 1e6:
        return f"{number / 1e6:.2f}M"
    elif number >= 1e3:
        return f"{number / 1e3:.1f}K"
    else:
        return str(number)

# Modified function to update the label displaying the invested gemstone powder
def update_gemstone_powder_display(gem_label, selected_level_var):
    level = int(selected_level_var.get().split(' ')[-1])
    invested_powder = gemstone_powder_investment.get(level, 0)
    formatted_investment = format_investment(invested_powder)
    gem_label.config(text=f"Level {level} - Invested: {formatted_investment}")
# Set up the trace for the dropdown selections
selected_tool.trace("w", update_tool_image)
selected_level_gem1.trace("w", update_tool_image)
selected_level_gem2.trace("w", update_tool_image)

# Load and display images for Gem 1 and Gem 2
for i, gem_name in enumerate(["Gem 1", "Gem 2"], start=1):
    gem_frame = tk.Frame(root, borderwidth=2, relief="solid")
    gem_frame.grid(row=0, column=i, padx=10, pady=10)
    gem_image = load_image(get_image_path(gem_name))
    gem_image_label = tk.Label(gem_frame, image=gem_image)
    gem_image_label.image = gem_image  # Keep a reference!
    gem_image_label.pack()
    gem_label = tk.Label(gem_frame, text=gem_name)
    gem_label.pack()
    dropdown = tk.OptionMenu(gem_frame, selected_level_gem1 if gem_name == "Gem 1" else selected_level_gem2, *list(gem1_powers.keys()))
    dropdown.pack(side="bottom", anchor="se")

# Create a frame for the tool
tool_frame = tk.Frame(root, borderwidth=2, relief="solid")
tool_frame.grid(row=0, column=0, padx=10, pady=10)
tool_image = load_image(get_image_path("Tool"))
tool_image_label = tk.Label(tool_frame, image=tool_image)
tool_image_label.image = tool_image  # Keep a reference!
tool_image_label.pack()
tool_label = tk.Label(tool_frame, text="Tool")
tool_label.pack()
tool_dropdown = tk.OptionMenu(tool_frame, selected_tool, *tool_options)
tool_dropdown.pack(side="bottom", anchor="se")

# Create a label to display the power of the selected tool
tool_power_label = tk.Label(root, text="Power: ")
tool_power_label.grid(row=1, column=0, padx=10, pady=10)

# Load and display the gemstone powder information labels
gemstone_powder_label_gem1 = tk.Label(root, text="")
gemstone_powder_label_gem1.grid(row=1, column=1, padx=10, pady=0)

gemstone_powder_label_gem2 = tk.Label(root, text="")
gemstone_powder_label_gem2.grid(row=1, column=2, padx=10, pady=0)

# Create a label to display the recommendation
recommendation_label = tk.Label(root, text="")
recommendation_label.grid(row=4, column=0, columnspan=3, pady=10)

# Set up the trace for the gem level dropdowns to refresh the recommendation when a new level is selected
selected_level_gem1.trace("w", update_recommendation_label)
selected_level_gem2.trace("w", update_recommendation_label)

# Call the update function to set the initial recommendation
update_recommendation_label()

# Set up traces for the level dropdowns to refresh the gemstone powder display when a new level is selected
selected_level_gem1.trace("w", lambda *args: update_gemstone_powder_display(gemstone_powder_label_gem1, selected_level_gem1))
selected_level_gem2.trace("w", lambda *args: update_gemstone_powder_display(gemstone_powder_label_gem2, selected_level_gem2))

# After all widgets are created and traces are set up, call update_tool_image
update_tool_image()

# Run the main loop
root.mainloop()
