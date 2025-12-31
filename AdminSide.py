import os

# --- CLASS: FileManager ---
# Handles reading and updating the complaints file.
# This separates data logic from the user interface (Separation of Concerns).
class FileManager:
    def __init__(self, filename="complaints_data.txt"):
        self.filename = filename

    def read_all(self):
        """
        Reads all lines from the text file.
        Returns a list of strings (one for each complaint).
        """
        if not os.path.exists(self.filename):
            return [] # Return empty list if file doesn't exist yet
        
        with open(self.filename, "r") as f:
            return f.readlines()

    def update_status(self, complaint_id, new_status):
        """
        Finds a complaint by ID and updates its status.
        Overwrites the file with the new data.
        """
        lines = self.read_all()
        new_lines = []
        found = False
        
        for line in lines:
            parts = line.strip().split('|')
            # The ID is the first item (index 0)
            if parts[0] == str(complaint_id):
                parts[5] = new_status  # Update the status column (index 5)
                found = True
                # Reassemble the line with the new status
                line = "|".join(parts) + "\n"
            
            new_lines.append(line)
            
        # Only rewrite the file if we actually found and changed something
        if found:
            with open(self.filename, "w") as f:
                f.writelines(new_lines)
            return True
        return False

# --- TEACHER DASHBOARD (Main Interface) ---
if __name__ == "__main__":
    manager = FileManager()
    
    while True:
        print("\n=== TEACHER DASHBOARD ===")
        
        # 1. Fetch and Display Data
        lines = manager.read_all()
        
        if not lines:
            print("(No complaints found in the system)")
        else:
            # Print table headers with spacing
            print(f"{'ID':<4} | {'Name':<15} | {'Status':<12} | {'Issue'}")
            print("-" * 60)
            
            for line in lines:
                parts = line.strip().split('|')
                # Ensure the line has all 6 parts before trying to print
                if len(parts) >= 6:
                    c_id, name, roll, date, issue, status = parts
                    # Format nicely using string padding (e.g., :<15 means 15 chars wide)
                    print(f"{c_id:<4} | {name:<15} | {status:<12} | {issue}")

        # 2. Show Menu Options
        print("\n[1] Update Status")
        print("[2] Refresh List")
        print("[3] Exit")
        
        choice = input("Enter Choice: ")

        if choice == '1':
            # Logic to resolve a complaint
            c_id = input("Enter Complaint ID to update: ")
            print("Select Status: [R]esolved, [P]rogress, [X]Rejected")
            code = input("Enter Code: ").upper()
            
            # Map single letters to full status words
            status_map = {'R': "Resolved", 'P': "In Progress", 'X': "Rejected"}
            
            if code in status_map:
                if manager.update_status(c_id, status_map[code]):
                    print(f"✅ Complaint {c_id} updated to '{status_map[code]}'.")
                else:
                    print("❌ Error: ID not found.")
            else:
                print("❌ Invalid status code.")
        
        elif choice == '2':
            continue # Restarts the loop to refresh the screen
            
        elif choice == '3':
            print("Exiting Dashboard...")
            break
