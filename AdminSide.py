import os

class FileManager:
    def __init__(self, filename="complaints_data.txt"):
        self.filename = filename

    def read_all(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r") as f:
            return f.readlines()

    def update_status(self, complaint_id, new_status):
        lines = self.read_all()
        new_lines = []
        found = False
        for line in lines:
            parts = line.strip().split('|')
            if parts[0] == str(complaint_id):
                parts[5] = new_status
                found = True
                line = "|".join(parts) + "\n"
            new_lines.append(line)
        if found:
            with open(self.filename, "w") as f:
                f.writelines(new_lines)
            return True
        return False

    def delete_complaint(self, complaint_id):
        lines = self.read_all()
        new_lines = []
        found = False
        for line in lines:
            parts = line.strip().split('|')
            if parts[0] != str(complaint_id):
                new_lines.append(line)
            else:
                found = True
        if found:
            with open(self.filename, "w") as f:
                f.writelines(new_lines)
            return True
        return False