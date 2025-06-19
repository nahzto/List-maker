import json
import os
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox

class DarkToDoApp:
    def __init__(self, root):
        self.root = root
        ctk.set_appearance_mode("dark")  # Force dark mode
        ctk.set_default_color_theme("dark-blue")  # Dark theme
        
        self.root.title("Dark To-Do List")
        self.root.geometry("800x600")
        
        # Configure dark color palette
        self.colors = {
            "bg": "#1a1a1a",
            "fg": "#e6e6e6",
            "accent": "#2a8cff",
            "danger": "#ff4d4d",
            "success": "#2ecc71",
            "card_bg": "#2a2a2a",
            "entry_bg": "#333333"
        }
        
        self.lists = {}
        self.current_list = None
        self.save_path = Path.home() / "Documents" / "ModernToDo.json"
        
        # Create save directory if needed
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.load_data()
        self.create_main_screen()
    
    def load_data(self):
        """Load saved lists from file if it exists"""
        try:
            if self.save_path.exists():
                with open(self.save_path, 'r') as f:
                    self.lists = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data:\n{str(e)}")
    
    def save_data(self):
        """Save lists to a reliable location"""
        try:
            with open(self.save_path, 'w') as f:
                json.dump(self.lists, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save data:\n{str(e)}")
    
    def create_main_screen(self):
        """Main screen showing all lists"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color=self.colors["bg"])
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(
            main_frame, 
            text="Your To-Do Lists", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["fg"]
        ).pack(pady=(10, 20))
        
        # Scrollable lists
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame, 
            fg_color=self.colors["bg"]
        )
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add list buttons
        for list_name in self.lists.keys():
            list_frame = ctk.CTkFrame(
                scroll_frame, 
                fg_color=self.colors["card_bg"]
            )
            list_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                list_frame, 
                text=list_name,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.colors["fg"],
                width=200,
                anchor="w"
            ).pack(side="left", padx=10)
            
            ctk.CTkButton(
                list_frame, 
                text="Open", 
                width=80,
                fg_color=self.colors["accent"],
                hover_color="#1a6fc9",
                command=lambda name=list_name: self.open_list(name)
            ).pack(side="right", padx=5)
            
            ctk.CTkButton(
                list_frame, 
                text="Delete", 
                width=80,
                fg_color=self.colors["danger"],
                hover_color="#cc3d3d",
                command=lambda name=list_name: self.delete_list(name)
            ).pack(side="right", padx=5)
        
        # Bottom buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color=self.colors["bg"])
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame, 
            text="New List", 
            command=self.create_new_list,
            height=40,
            width=120,
            fg_color=self.colors["accent"],
            hover_color="#1a6fc9"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame, 
            text="Exit", 
            command=self.root.quit,
            height=40,
            width=120,
            fg_color=self.colors["danger"],
            hover_color="#cc3d3d"
        ).pack(side="left", padx=10)
    
    def create_new_list(self):
        """Create a new list with dialog"""
        dialog = ctk.CTkInputDialog(
            text="Enter new list name:", 
            title="New List",
            fg_color=self.colors["card_bg"],
            text_color=self.colors["fg"]
        )
        list_name = dialog.get_input()
        
        if list_name:
            if list_name not in self.lists:
                self.lists[list_name] = []
                self.save_data()
                self.create_main_screen()
            else:
                messagebox.showerror("Error", "List name already exists!")
    
    def delete_list(self, list_name):
        """Delete an existing list"""
        if messagebox.askyesno("Confirm", f"Delete list '{list_name}'?"):
            del self.lists[list_name]
            self.save_data()
            self.create_main_screen()
    
    def open_list(self, list_name):
        """Open a list for editing"""
        self.current_list = list_name
        self.show_list()
    
    def show_list(self):
        """Display list contents"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        list_frame = ctk.CTkFrame(self.root, fg_color=self.colors["bg"])
        list_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Header with back button
        header_frame = ctk.CTkFrame(list_frame, fg_color=self.colors["bg"])
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkButton(
            header_frame,
            text="← Back",
            width=80,
            fg_color=self.colors["accent"],
            hover_color="#1a6fc9",
            command=self.create_main_screen
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            header_frame, 
            text=self.current_list, 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["fg"]
        ).pack(side="left", padx=10, fill="x", expand=True)
        
        # Add item section
        add_frame = ctk.CTkFrame(list_frame, fg_color=self.colors["bg"])
        add_frame.pack(fill="x", pady=(0, 10))
        
        self.new_item_entry = ctk.CTkEntry(
            add_frame, 
            placeholder_text="New item...",
            width=400,
            fg_color=self.colors["entry_bg"],
            text_color=self.colors["fg"],
            border_color=self.colors["accent"]
        )
        self.new_item_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.new_item_entry.bind("<Return>", lambda e: self.add_item())
        
        ctk.CTkButton(
            add_frame, 
            text="Add", 
            width=80,
            fg_color=self.colors["accent"],
            hover_color="#1a6fc9",
            command=self.add_item
        ).pack(side="left", padx=5)
        
        # Items list
        scroll_frame = ctk.CTkScrollableFrame(
            list_frame,
            height=400,
            fg_color=self.colors["bg"]
        )
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Display all items
        for i, item in enumerate(self.lists[self.current_list]):
            item_frame = ctk.CTkFrame(
                scroll_frame, 
                fg_color=self.colors["card_bg"]
            )
            item_frame.pack(fill="x", pady=2)
            
            # Checkbox
            var = ctk.IntVar(value=1 if item['completed'] else 0)
            checkbox = ctk.CTkCheckBox(
                item_frame,
                text="",
                variable=var,
                width=20,
                fg_color=self.colors["accent"],
                hover_color="#1a6fc9",
                command=lambda i=i, v=var: self.toggle_complete(i, v)
            )
            checkbox.pack(side="left", padx=5)
            
            # Item text
            text = ctk.CTkLabel(
                item_frame,
                text=item['text'],
                font=ctk.CTkFont(size=14, overstrike=item['completed']),
                text_color=self.colors["fg"],
                anchor="w"
            )
            text.pack(side="left", padx=5, fill="x", expand=True)
            
            # Delete button
            ctk.CTkButton(
                item_frame,
                text="×",
                width=30,
                height=30,
                fg_color="transparent",
                text_color=self.colors["danger"],
                hover_color="#3a3a3a",
                command=lambda i=i: self.remove_item(i)
            ).pack(side="right", padx=5)
        
        # Clear completed button
        ctk.CTkButton(
            list_frame,
            text="Clear Completed",
            command=self.clear_completed,
            fg_color=self.colors["success"],
            hover_color="#25a25a"
        ).pack(pady=10)
    
    def add_item(self):
        """Add new item to current list"""
        text = self.new_item_entry.get().strip()
        if text:
            self.lists[self.current_list].append({
                'text': text,
                'completed': False
            })
            self.save_data()
            self.new_item_entry.delete(0, "end")
            self.show_list()
    
    def remove_item(self, index):
        """Remove item from current list"""
        del self.lists[self.current_list][index]
        self.save_data()
        self.show_list()
    
    def toggle_complete(self, index, var):
        """Toggle item completion status"""
        self.lists[self.current_list][index]['completed'] = var.get() == 1
        self.save_data()
        self.show_list()
    
    def clear_completed(self):
        """Remove all completed items"""
        self.lists[self.current_list] = [
            item for item in self.lists[self.current_list] 
            if not item['completed']
        ]
        self.save_data()
        self.show_list()

if __name__ == "__main__":
    root = ctk.CTk()
    app = DarkToDoApp(root)
    root.mainloop()