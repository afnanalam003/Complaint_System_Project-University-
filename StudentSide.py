import datetime
import os

class FileManager:
    def __init__(self, filename="complaints_data.txt"):
        self.filename = filename

    def save_complaint(self, name, roll_no, issue):
        try:
            last_id = 0
            if os.path.exists(self.filename):
                with open(self.filename, "r") as r:
                    content = r.readlines()
                    if content:
                        last_line = content[-1]
                        last_id = int(last_line.split('|')[0])
            
            new_id = last_id + 1
            date = datetime.date.today()
            issue = issue.replace("|", "-")
            data_line = f"{new_id}|{name}|{roll_no}|{date}|{issue}|Pending\n"
            
            with open(self.filename, "a") as f:
                f.write(data_line)
            return True
        except Exception as e:
            print(f"File Error: {e}")
            return False