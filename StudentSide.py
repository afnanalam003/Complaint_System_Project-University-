import datetime
import os

# --- CLASS: FileManager ---
# This class follows the Single Responsibility Principle (SRP).
# Its ONLY job is to handle file operations (saving data).
class FileManager:
    def __init__(self, filename="complaints_data.txt"):
        self.filename = filename

    def save_complaint(self, name, roll_no, issue):
        """
        Saves a new complaint to the text file.
        Returns True if successful, False if an error occurs.
        """
        try:
            # 1. Calculate a new unique ID
            # We count the number of lines currently in the file to determine the ID.
            line_count = 0
            if os.path.exists(self.filename):
                with open(self.filename, "r") as r:
                    line_count = len(r.readlines())
            
            new_id = line_count + 1
            date = datetime.date.today()
            
            # 2. Format the data for storage
            # Format: ID | Name | RollNo | Date | Issue | Status
            data_line = f"{new_id}|{name}|{roll_no}|{date}|{issue}|Pending\n"
            
            # 3. Append the data to the file
            # 'a' mode opens the file for appending (adding to the end)
            with open(self.filename, "a") as f:
                f.write(data_line)
            return True
            
        except Exception as e:
            # If the file is open elsewhere or permission is denied, catch the error
            print(f"Error details: {e}")
            return False

# --- MAIN EXECUTION ---
# This block only runs if you run this file directly.
if __name__ == "__main__":
    manager = FileManager()
    
    print("=== STUDENT COMPLAINT FORM ===")
    print("Please fill out the details below:\n")
    
    # Get input from the student
    name = input("Enter Name: ")
    roll = input("Enter Roll No: ")
    issue = input("Enter Issue (e.g., Wi-Fi not working): ")
    
    print("\nSaving your complaint...")
    
    # Attempt to save using our FileManager class
    if manager.save_complaint(name, roll, issue):
        print("✅ Complaint Submitted Successfully!")
    else:
        print("❌ Error: Could not save file. Please check if the text file is open.")
        
    # Keep window open so student can see the success message
    input("\nPress Enter to exit...")
