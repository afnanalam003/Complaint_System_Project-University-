import customtkinter as ctk
import colorsys

# --- IMPORT LOGIC ---
try:
    from StudentSide import FileManager as StudentManager
    from AdminSide import FileManager as TeacherManager
except ImportError:
    print("Error: Ensure StudentSide.py and AdminSide.py are in the folder.")

# --- THEME CONFIGURATION ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# --- CUSTOM POPUP CLASS ---
class CustomPopup(ctk.CTkToplevel):
    def __init__(self, parent, title, message, type="info", command=None):
        super().__init__(parent)
        self.command = command
        self.title(title)
        self.geometry("400x220")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        try:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
            y = parent.winfo_y() + (parent.winfo_height() // 2) - 110
            self.geometry(f"+{x}+{y}")
        except:
            self.geometry("400x220")
        
        self.configure(fg_color="#1a1a1a")
        color = "#4facfe" if type == "info" else "#ff416c" if type == "error" else "#00f260"
        
        self.lbl_title = ctk.CTkLabel(self, text=title, font=("Segoe UI", 18, "bold"), text_color=color)
        self.lbl_title.pack(pady=(20, 10))
        
        self.lbl_msg = ctk.CTkLabel(self, text=message, font=("Segoe UI", 14), text_color="#ddd", wraplength=350)
        self.lbl_msg.pack(pady=10, padx=20)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        if type == "confirm":
            ctk.CTkButton(btn_frame, text="Cancel", width=100, fg_color="#333", hover_color="#444", command=self.destroy).pack(side="left", padx=10)
            ctk.CTkButton(btn_frame, text="Confirm", width=100, fg_color="#ff416c", hover_color="#d43657", command=self.on_confirm).pack(side="left", padx=10)
        else:
            ctk.CTkButton(btn_frame, text="OK", width=100, fg_color=color, text_color="black" if type=="success" else "white", command=self.destroy).pack()

    def on_confirm(self):
        if self.command:
            self.command()
        self.destroy()

# --- MAIN APP CLASS ---
class ComplaintSystemApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.student_logic = StudentManager()
        self.teacher_logic = TeacherManager()
        self.admin_authenticated = False
        
        self.title("University Complaint Management System")
        self.geometry("1250x850") 
        
        self.hue = 0
        self.animate_background()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#111111")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="U-CMS", font=("Segoe UI", 32, "bold"), text_color="#4facfe")
        self.logo_label.pack(pady=(50, 10))
        
        self.subtitle_label = ctk.CTkLabel(self.sidebar, text="Student Service Portal", font=("Segoe UI", 12), text_color="#aaaaaa")
        self.subtitle_label.pack(pady=(0, 40))

        # NAVIGATION BUTTONS (Now stored as variables so we can change their color)
        self.btn_student = self.create_nav_button("Student Section", self.show_student_view)
        self.btn_admin = self.create_nav_button("Admin Panel", self.show_admin_login)
        
        self.status_label = ctk.CTkLabel(self.sidebar, text="● System Operational", text_color="#00f260", font=("Segoe UI", 10))
        self.status_label.pack(side="bottom", pady=20)

        # Main Area
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.show_student_view()

    # --- HELPERS ---
    def animate_background(self):
        self.hue += 0.001
        if self.hue > 1: self.hue = 0
        rgb = colorsys.hsv_to_rgb(0.66, 0.5, 0.2 + (0.1 * abs(self.hue - 0.5)))
        color_hex = "#%02x%02x%02x" % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        self.configure(fg_color=color_hex) 
        self.after(50, self.animate_background)

    def create_nav_button(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command, height=50, corner_radius=10, 
                            fg_color="transparent", text_color="gray", hover_color="#333333", font=("Segoe UI", 16), anchor="w")
        btn.pack(pady=10, padx=20, fill="x")
        return btn

    def update_sidebar_state(self, active_btn):
        """Highlights the active button and resets the other"""
        # Reset both to transparent/gray
        self.btn_student.configure(fg_color="transparent", text_color="gray", border_width=0)
        self.btn_admin.configure(fg_color="transparent", text_color="gray", border_width=0)
        
        # Highlight the active one
        if active_btn == "student":
            self.btn_student.configure(fg_color="#1a1a1a", text_color="white", border_width=1, border_color="#4facfe")
        elif active_btn == "admin":
            self.btn_admin.configure(fg_color="#1a1a1a", text_color="white", border_width=1, border_color="#4facfe")

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def on_textbox_focus_in(self, event):
        if self.issue_textbox.get("0.0", "end-1c") == "Describe your issue here...":
            self.issue_textbox.delete("0.0", "end")
            self.issue_textbox.configure(text_color="white")

    def on_textbox_focus_out(self, event):
        if not self.issue_textbox.get("0.0", "end-1c").strip():
            self.issue_textbox.insert("0.0", "Describe your issue here...")
            self.issue_textbox.configure(text_color="gray")

    # --- GRID TABLE BUILDER ---
    def create_table_row(self, parent, data, is_header=False):
        row_color = "#2b2b2b" if is_header else "transparent"
        text_color = "white" if is_header else "#ddd"
        font = ("Segoe UI", 13, "bold") if is_header else ("Segoe UI", 12)
        
        row_frame = ctk.CTkFrame(parent, fg_color=row_color, height=40 if is_header else 35, corner_radius=5 if is_header else 0)
        row_frame.pack(fill="x", pady=2)
        
        row_frame.grid_columnconfigure(0, minsize=50)   # ID
        row_frame.grid_columnconfigure(1, minsize=120)  # Roll No
        row_frame.grid_columnconfigure(2, minsize=200)  # Name
        row_frame.grid_columnconfigure(3, minsize=120)  # Status
        row_frame.grid_columnconfigure(4, weight=1)     # Issue 

        lbl_id = ctk.CTkLabel(row_frame, text=data[0], font=font, text_color=text_color, anchor="w")
        lbl_id.grid(row=0, column=0, padx=10, sticky="w")

        lbl_roll = ctk.CTkLabel(row_frame, text=data[1], font=font, text_color=text_color, anchor="w")
        lbl_roll.grid(row=0, column=1, padx=10, sticky="w")

        lbl_name = ctk.CTkLabel(row_frame, text=data[2], font=font, text_color=text_color, anchor="w")
        lbl_name.grid(row=0, column=2, padx=10, sticky="w")

        status_text = data[3]
        status_color = text_color
        if not is_header:
            if "Resolved" in status_text: status_color = "#00f260"
            elif "Pending" in status_text: status_color = "#f2c94c"
            elif "Rejected" in status_text: status_color = "#ff416c"
        
        lbl_status = ctk.CTkLabel(row_frame, text=status_text, font=font, text_color=status_color, anchor="w")
        lbl_status.grid(row=0, column=3, padx=10, sticky="w")

        lbl_issue = ctk.CTkLabel(row_frame, text=data[4], font=font, text_color=text_color, anchor="w")
        lbl_issue.grid(row=0, column=4, padx=10, sticky="w")

        if not is_header:
            sep = ctk.CTkFrame(parent, fg_color="#333", height=1)
            sep.pack(fill="x")

    # --- STUDENT VIEW ---
    def show_student_view(self):
        self.update_sidebar_state("student") # UPDATE NAV STATE
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Student Dashboard", font=("Segoe UI", 30, "bold")).pack(anchor="w", pady=(0, 20))

        container = ctk.CTkFrame(self.main_area, fg_color="transparent")
        container.pack(fill="both", expand=True)

        left_card = ctk.CTkFrame(container, fg_color="#1a1a1a", corner_radius=15, border_width=1, border_color="#333")
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(left_card, text="📝 New Complaint", font=("Segoe UI", 20, "bold"), text_color="#4facfe").pack(pady=20, padx=20, anchor="w")
        
        self.name_entry = ctk.CTkEntry(left_card, placeholder_text="Full Name", height=45, fg_color="#111", border_color="#444")
        self.name_entry.pack(pady=10, padx=20, fill="x")
        
        self.roll_entry = ctk.CTkEntry(left_card, placeholder_text="Roll Number (e.g. 23M-101)", height=45, fg_color="#111", border_color="#444")
        self.roll_entry.pack(pady=10, padx=20, fill="x")
        
        self.issue_textbox = ctk.CTkTextbox(left_card, height=150, fg_color="#111", border_color="#444", border_width=2, text_color="gray")
        self.issue_textbox.insert("0.0", "Describe your issue here...")
        self.issue_textbox.bind("<FocusIn>", self.on_textbox_focus_in)
        self.issue_textbox.bind("<FocusOut>", self.on_textbox_focus_out)
        self.issue_textbox.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(left_card, text="Submit Request", command=self.handle_student_submit, height=50, fg_color="#00f260", 
                      hover_color="#00c950", text_color="black", font=("Segoe UI", 16, "bold")).pack(pady=30, padx=20, fill="x")

        right_card = ctk.CTkFrame(container, fg_color="#1a1a1a", corner_radius=15, border_width=1, border_color="#333")
        right_card.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(right_card, text="🔍 Track Status", font=("Segoe UI", 20, "bold"), text_color="#a8edea").pack(pady=20, padx=20, anchor="w")
        
        search_frame = ctk.CTkFrame(right_card, fg_color="transparent")
        search_frame.pack(fill="x", padx=20)
        self.search_roll = ctk.CTkEntry(search_frame, placeholder_text="Enter Your Roll No.", height=40, fg_color="#111", border_color="#444")
        self.search_roll.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(search_frame, text="↻", width=40, height=40, fg_color="#333", hover_color="#444", command=self.refresh_track_data).pack(side="right", padx=(5, 0))
        ctk.CTkButton(search_frame, text="Search", width=80, height=40, fg_color="#4facfe", command=self.refresh_track_data).pack(side="right")

        self.results_frame = ctk.CTkFrame(right_card, fg_color="transparent")
        
        self.track_table_frame = ctk.CTkScrollableFrame(self.results_frame, fg_color="#111", height=300)
        self.track_table_frame.pack(fill="both", pady=20, expand=True)
        
        action_f = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        action_f.pack(fill="x")
        self.track_id_input = ctk.CTkEntry(action_f, placeholder_text="ID", width=60, fg_color="#111")
        self.track_id_input.pack(side="left", padx=(0, 10))
        ctk.CTkButton(action_f, text="Delete Complaint", fg_color="#ff416c", hover_color="#d43657", command=self.handle_student_delete).pack(side="left")

    def refresh_track_data(self):
        roll = self.search_roll.get()
        if not roll: return
        
        for widget in self.track_table_frame.winfo_children():
            widget.destroy()

        lines = self.teacher_logic.read_all()
        found_data = [l for l in lines if len(l.split('|')) >= 3 and l.split('|')[2].lower() == roll.lower()]

        if found_data:
            self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
            self.create_student_table_row(self.track_table_frame, ["ID", "Status", "Issue"], is_header=True)
            for line in found_data:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    self.create_student_table_row(self.track_table_frame, [parts[0], parts[5], parts[4]])
        else:
            self.results_frame.pack_forget()
            CustomPopup(self, "No Records", "No complaints found for this Roll Number.", "info")

    def create_student_table_row(self, parent, data, is_header=False):
        row_color = "#2b2b2b" if is_header else "transparent"
        text_color = "white" if is_header else "#ddd"
        font = ("Segoe UI", 13, "bold") if is_header else ("Segoe UI", 12)
        
        row_frame = ctk.CTkFrame(parent, fg_color=row_color, height=35)
        row_frame.pack(fill="x", pady=2)
        
        row_frame.grid_columnconfigure(0, minsize=50) # ID
        row_frame.grid_columnconfigure(1, minsize=100) # Status
        row_frame.grid_columnconfigure(2, weight=1)    # Issue

        ctk.CTkLabel(row_frame, text=data[0], font=font, text_color=text_color, anchor="w").grid(row=0, column=0, padx=10, sticky="w")
        
        status_color = text_color
        if not is_header:
            if "Resolved" in data[1]: status_color = "#00f260"
            elif "Pending" in data[1]: status_color = "#f2c94c"
            elif "Rejected" in data[1]: status_color = "#ff416c"
            
        ctk.CTkLabel(row_frame, text=data[1], font=font, text_color=status_color, anchor="w").grid(row=0, column=1, padx=10, sticky="w")
        ctk.CTkLabel(row_frame, text=data[2], font=font, text_color=text_color, anchor="w").grid(row=0, column=2, padx=10, sticky="w")

    def handle_student_submit(self):
        name = self.name_entry.get()
        roll = self.roll_entry.get()
        issue = self.issue_textbox.get("0.0", "end").strip()
        
        if not name or not roll or "Describe" in issue:
            CustomPopup(self, "Incomplete", "Please fill all fields.", "error")
            return
            
        if self.student_logic.save_complaint(name, roll, issue):
            CustomPopup(self, "Submitted", "Complaint logged successfully!", "success")
            self.name_entry.delete(0, "end")
            self.roll_entry.delete(0, "end")
            self.issue_textbox.delete("0.0", "end")
            self.issue_textbox.insert("0.0", "Describe your issue here...")
            self.issue_textbox.configure(text_color="gray")

    def handle_student_delete(self):
        c_id = self.track_id_input.get()
        if c_id:
            CustomPopup(self, "Confirm Delete", "Permanently remove this record?", "confirm", command=lambda: self.perform_delete(c_id))

    def perform_delete(self, c_id):
        if self.teacher_logic.delete_complaint(c_id):
            self.track_id_input.delete(0, "end")
            self.refresh_track_data()

    # --- ADMIN VIEW ---
    def show_admin_login(self):
        self.update_sidebar_state("admin") # UPDATE NAV STATE
        self.clear_main_area()
        if self.admin_authenticated:
            self.show_admin_dashboard()
            return

        login_card = ctk.CTkFrame(self.main_area, fg_color="#1a1a1a", width=400, corner_radius=20, border_width=1, border_color="#4facfe")
        login_card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(login_card, text="🔒 Admin Access", font=("Segoe UI", 24, "bold")).pack(pady=30)
        self.user_entry = ctk.CTkEntry(login_card, placeholder_text="Username", width=250, height=45)
        self.user_entry.pack(pady=10)
        self.pass_entry = ctk.CTkEntry(login_card, placeholder_text="Password", show="*", width=250, height=45)
        self.pass_entry.pack(pady=10)
        ctk.CTkButton(login_card, text="Login System", command=self.check_login, width=250, height=45, fg_color="#4facfe").pack(pady=30)

    def check_login(self):
        if self.user_entry.get() == "admin" and self.pass_entry.get() == "admin123":
            self.admin_authenticated = True
            self.show_admin_dashboard()
        else:
            CustomPopup(self, "Access Denied", "Invalid Credentials", "error")

    def show_admin_dashboard(self):
        self.clear_main_area()
        
        header = ctk.CTkFrame(self.main_area, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text="Admin Control Panel", font=("Segoe UI", 30, "bold")).pack(side="left")
        ctk.CTkButton(header, text="Logout", width=100, fg_color="#333", command=lambda: [setattr(self, 'admin_authenticated', False), self.show_admin_login()]).pack(side="right")

        stats_container = ctk.CTkFrame(self.main_area, fg_color="transparent")
        stats_container.pack(fill="x", pady=(0, 20))
        self.card_total = self.create_stat_card(stats_container, "Total Complaints", "0", "#4facfe")
        self.card_pending = self.create_stat_card(stats_container, "Pending", "0", "#ffb199")
        self.card_resolved = self.create_stat_card(stats_container, "Resolved", "0", "#00f260")

        table_container = ctk.CTkFrame(self.main_area, fg_color="#1a1a1a", corner_radius=15)
        table_container.pack(fill="both", expand=True)
        
        self.admin_table_frame = ctk.CTkScrollableFrame(table_container, fg_color="transparent")
        self.admin_table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        actions = ctk.CTkFrame(self.main_area, fg_color="#1a1a1a", height=80, corner_radius=15)
        actions.pack(fill="x", pady=(20, 0))
        
        ctk.CTkLabel(actions, text="Complaint ID:").pack(side="left", padx=(20, 5))
        self.admin_id_input = ctk.CTkEntry(actions, width=60)
        self.admin_id_input.pack(side="left", padx=5)
        
        self.status_menu = ctk.CTkOptionMenu(actions, values=["Resolved", "In Progress", "Rejected"])
        self.status_menu.pack(side="left", padx=10)
        
        ctk.CTkButton(actions, text="Update Status", fg_color="#00f260", text_color="black", command=self.handle_admin_update).pack(side="left", padx=5)
        ctk.CTkButton(actions, text="Delete", fg_color="#ff416c", command=self.handle_admin_delete).pack(side="left", padx=5)
        ctk.CTkButton(actions, text="Refresh", fg_color="#4facfe", command=self.refresh_admin_data).pack(side="right", padx=20)

        self.refresh_admin_data()

    def create_stat_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=15, border_width=1, border_color="#333")
        card.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 12), text_color="#aaa").pack(pady=(15, 0))
        lbl_value = ctk.CTkLabel(card, text=value, font=("Segoe UI", 28, "bold"), text_color=color)
        lbl_value.pack(pady=(0, 15))
        return lbl_value

    def refresh_admin_data(self):
        lines = self.teacher_logic.read_all()
        
        total = len(lines)
        pending = len([l for l in lines if "Pending" in l])
        resolved = len([l for l in lines if "Resolved" in l])
        
        self.card_total.configure(text=str(total))
        self.card_pending.configure(text=str(pending))
        self.card_resolved.configure(text=str(resolved))

        for widget in self.admin_table_frame.winfo_children():
            widget.destroy()

        self.create_table_row(self.admin_table_frame, ["ID", "ROLL NO", "NAME", "STATUS", "ISSUE"], is_header=True)
        
        for line in lines:
            parts = line.strip().split('|')
            if len(parts) >= 6:
                row_data = [parts[0], parts[2], parts[1], parts[5], parts[4]]
                self.create_table_row(self.admin_table_frame, row_data)

    def handle_admin_update(self):
        c_id = self.admin_id_input.get()
        status = self.status_menu.get()
        if c_id and self.teacher_logic.update_status(c_id, status):
            self.refresh_admin_data()
            self.admin_id_input.delete(0, "end")

    def handle_admin_delete(self):
        c_id = self.admin_id_input.get()
        if c_id:
            CustomPopup(self, "Confirm Delete", "Permanently remove this record?", "confirm", command=lambda: self.perform_admin_delete(c_id))

    def perform_admin_delete(self, c_id):
        if self.teacher_logic.delete_complaint(c_id):
            self.refresh_admin_data()
            self.admin_id_input.delete(0, "end")

if __name__ == "__main__":
    app = ComplaintSystemApp()
    app.mainloop()