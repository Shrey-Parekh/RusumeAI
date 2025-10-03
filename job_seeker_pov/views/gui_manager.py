"""
GUI Manager - Handles all Tkinter interface components and user interactions
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from typing import Dict, List, Any, Optional, Callable
import json
from models.profile_manager import ProfileManager
from models.job_analyzer import JobAnalyzer
from models.resume_generator import ResumeGenerator


class GUIManager:
    """Manages all GUI components and user interactions for the Resume Tailoring App"""
    
    def __init__(self):
        """Initialize GUI Manager"""
        self.root = None
        self.current_frame = None
        self.controller = None  # Will be set by the controller
        
        # Legacy model instances (for backward compatibility)
        self.profile_manager = ProfileManager()
        self.job_analyzer = JobAnalyzer()
        self.resume_generator = ResumeGenerator()
        
        # Current data (will be managed by controller)
        self.current_profile = None
        self.current_job_analysis = None
        self.current_resume = None
        
        # GUI components
        self.profile_form_vars = {}
        self.job_text_widget = None
        self.resume_preview_widget = None
    
    def set_controller(self, controller) -> None:
        """Set the application controller reference"""
        self.controller = controller
        
    def create_main_window(self) -> None:
        """Create and configure the main application window"""
        self.root = tk.Tk()
        self.root.title("Resume Tailoring App")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main menu
        self._create_menu()
        
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create navigation frame
        nav_frame = ttk.Frame(main_container)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Navigation buttons
        ttk.Button(nav_frame, text="Profile Management", 
                  command=self.show_profile_form).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="Job Analysis", 
                  command=self.show_job_input_form).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="Resume Preview", 
                  command=self.show_resume_preview).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="History", 
                  command=self.show_history_view).pack(side=tk.LEFT, padx=(0, 5))
        
        # Create content frame
        self.content_frame = ttk.Frame(main_container)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Load existing profile
        self._load_existing_profile()
        
        # Show initial view
        self.show_profile_form()
    
    def _create_menu(self) -> None:
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Profile", command=self._new_profile)
        file_menu.add_command(label="Load Profile", command=self._load_profile)
        file_menu.add_command(label="Save Profile", command=self._save_profile)
        file_menu.add_separator()
        file_menu.add_command(label="Export Resume", command=self._export_resume)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def show_profile_form(self) -> None:
        """Display the profile creation and editing form"""
        self._clear_content_frame()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.content_frame)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = ttk.Label(scrollable_frame, text="Profile Management", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create form sections
        self._create_personal_info_section(scrollable_frame)
        self._create_summary_section(scrollable_frame)
        self._create_work_experience_section(scrollable_frame)
        self._create_education_section(scrollable_frame)
        self._create_skills_section(scrollable_frame)
        self._create_projects_section(scrollable_frame)
        
        # Action buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Save Profile", 
                  command=self._save_profile_form).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Validate Profile", 
                  command=self._validate_profile_form).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Clear Form", 
                  command=self._clear_profile_form).pack(side=tk.LEFT)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate form with existing data
        if self.current_profile:
            self._populate_profile_form(self.current_profile)
    
    def show_job_input_form(self) -> None:
        """Display the job description input interface"""
        self._clear_content_frame()
        
        # Title
        title_label = ttk.Label(self.content_frame, text="Job Description Analysis", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Instructions
        instructions = ttk.Label(self.content_frame, 
                                text="Paste the job description below and click 'Analyze' to extract requirements:",
                                wraplength=600)
        instructions.pack(pady=(0, 10))
        
        # Job description input
        input_frame = ttk.LabelFrame(self.content_frame, text="Job Description", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.job_text_widget = scrolledtext.ScrolledText(input_frame, height=15, wrap=tk.WORD)
        self.job_text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Analyze Job", 
                  command=self._analyze_job_description).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Clear", 
                  command=self._clear_job_input).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Generate Resume", 
                  command=self._generate_resume).pack(side=tk.LEFT)
        
        # Analysis results frame
        self.analysis_frame = ttk.LabelFrame(self.content_frame, text="Analysis Results", padding=10)
        self.analysis_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Initially hide analysis frame
        self.analysis_frame.pack_forget()
    
    def show_resume_preview(self, resume_content: Optional[str] = None) -> None:
        """Display the resume preview window"""
        self._clear_content_frame()
        
        # Title
        title_label = ttk.Label(self.content_frame, text="Resume Preview", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        if not self.current_resume and not resume_content:
            # No resume to display
            no_resume_label = ttk.Label(self.content_frame, 
                                       text="No resume generated yet. Please analyze a job description first.",
                                       font=('Arial', 12))
            no_resume_label.pack(pady=50)
            
            ttk.Button(self.content_frame, text="Go to Job Analysis", 
                      command=self.show_job_input_form).pack(pady=10)
            return
        
        # Resume preview area
        preview_frame = ttk.LabelFrame(self.content_frame, text="Generated Resume", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.resume_preview_widget = scrolledtext.ScrolledText(preview_frame, height=20, wrap=tk.WORD)
        self.resume_preview_widget.pack(fill=tk.BOTH, expand=True)
        
        # Display resume content
        content_to_show = resume_content or self._format_current_resume()
        self.resume_preview_widget.delete(1.0, tk.END)
        self.resume_preview_widget.insert(1.0, content_to_show)
        self.resume_preview_widget.config(state=tk.DISABLED)
        
        # Action buttons
        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Export as PDF", 
                  command=lambda: self._export_resume("pdf")).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Export as Word", 
                  command=lambda: self._export_resume("docx")).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Export as Text", 
                  command=lambda: self._export_resume("txt")).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Regenerate", 
                  command=self._regenerate_resume).pack(side=tk.LEFT)
    
    def show_export_dialog(self) -> None:
        """Show export options dialog"""
        if not self.current_resume:
            messagebox.showwarning("No Resume", "Please generate a resume first.")
            return
        
        # Create export dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Export Resume")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        ttk.Label(dialog, text="Choose export format:", font=('Arial', 12)).pack(pady=20)
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="PDF", 
                  command=lambda: self._export_and_close(dialog, "pdf")).pack(pady=5, fill=tk.X)
        ttk.Button(button_frame, text="Word Document", 
                  command=lambda: self._export_and_close(dialog, "docx")).pack(pady=5, fill=tk.X)
        ttk.Button(button_frame, text="Text File", 
                  command=lambda: self._export_and_close(dialog, "txt")).pack(pady=5, fill=tk.X)
        
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(pady=(20, 5), fill=tk.X)
    
    def show_history_view(self) -> None:
        """Display the resume export history"""
        self._clear_content_frame()
        
        # Title
        title_label = ttk.Label(self.content_frame, text="Resume Export History", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Get history from controller
        history = []
        if self.controller:
            history = self.controller.get_resume_history()
        
        if not history:
            # No history to display
            no_history_label = ttk.Label(self.content_frame, 
                                        text="No resume export history found.",
                                        font=('Arial', 12))
            no_history_label.pack(pady=50)
            return
        
        # History controls
        controls_frame = ttk.Frame(self.content_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(controls_frame, text="Refresh", 
                  command=self.show_history_view).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls_frame, text="Clear All History", 
                  command=self._clear_all_history).pack(side=tk.LEFT)
        
        # History list
        history_frame = ttk.LabelFrame(self.content_frame, text="Export History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for history
        columns = ("timestamp", "filename", "format", "profile", "job_title", "exists")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.history_tree.heading("timestamp", text="Date/Time")
        self.history_tree.heading("filename", text="Filename")
        self.history_tree.heading("format", text="Format")
        self.history_tree.heading("profile", text="Profile")
        self.history_tree.heading("job_title", text="Job Title")
        self.history_tree.heading("exists", text="File Exists")
        
        # Configure column widths
        self.history_tree.column("timestamp", width=150)
        self.history_tree.column("filename", width=200)
        self.history_tree.column("format", width=80)
        self.history_tree.column("profile", width=150)
        self.history_tree.column("job_title", width=200)
        self.history_tree.column("exists", width=80)
        
        # Add scrollbar
        history_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        # Populate history
        for entry in reversed(history):  # Show newest first
            timestamp = entry.get("timestamp", "")
            if timestamp:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    timestamp = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            
            filename = entry.get("filename", "")
            # Show only filename, not full path
            if filename:
                filename = filename.split('/')[-1].split('\\')[-1]
            
            self.history_tree.insert("", "end", values=(
                timestamp,
                filename,
                entry.get("format", "").upper(),
                entry.get("profile_name", "")[:30],  # Truncate long names
                entry.get("job_title", "")[:40],     # Truncate long titles
                "Yes" if entry.get("file_exists", False) else "No"
            ), tags=(entry.get("id", ""),))
        
        # Pack treeview and scrollbar
        self.history_tree.pack(side="left", fill="both", expand=True)
        history_scrollbar.pack(side="right", fill="y")
        
        # Context menu for history items
        self.history_tree.bind("<Button-3>", self._show_history_context_menu)
        
        # Action buttons
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(action_frame, text="Delete Selected", 
                  command=self._delete_selected_history).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Open File Location", 
                  command=self._open_file_location).pack(side=tk.LEFT)
    
    def run(self) -> None:
        """Start the GUI application"""
        if self.root:
            self.root.mainloop()
    
    def _clear_content_frame(self) -> None:
        """Clear all widgets from the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def _load_existing_profile(self) -> None:
        """Load existing profile data if available"""
        try:
            if self.controller:
                self.current_profile = self.controller.load_profile()
            else:
                self.current_profile = self.profile_manager.load_profile()
        except Exception as e:
            print(f"Error loading profile: {e}")
            self.current_profile = None   
 
    def _create_personal_info_section(self, parent: ttk.Widget) -> None:
        """Create personal information form section"""
        section_frame = ttk.LabelFrame(parent, text="Personal Information", padding=10)
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create form variables
        self.profile_form_vars["personal_info"] = {}
        
        # Name
        name_frame = ttk.Frame(section_frame)
        name_frame.pack(fill=tk.X, pady=2)
        ttk.Label(name_frame, text="Full Name*:", width=15).pack(side=tk.LEFT)
        self.profile_form_vars["personal_info"]["name"] = tk.StringVar()
        ttk.Entry(name_frame, textvariable=self.profile_form_vars["personal_info"]["name"], 
                 width=40).pack(side=tk.LEFT, padx=(10, 0))
        
        # Email
        email_frame = ttk.Frame(section_frame)
        email_frame.pack(fill=tk.X, pady=2)
        ttk.Label(email_frame, text="Email*:", width=15).pack(side=tk.LEFT)
        self.profile_form_vars["personal_info"]["email"] = tk.StringVar()
        ttk.Entry(email_frame, textvariable=self.profile_form_vars["personal_info"]["email"], 
                 width=40).pack(side=tk.LEFT, padx=(10, 0))
        
        # Phone
        phone_frame = ttk.Frame(section_frame)
        phone_frame.pack(fill=tk.X, pady=2)
        ttk.Label(phone_frame, text="Phone:", width=15).pack(side=tk.LEFT)
        self.profile_form_vars["personal_info"]["phone"] = tk.StringVar()
        ttk.Entry(phone_frame, textvariable=self.profile_form_vars["personal_info"]["phone"], 
                 width=40).pack(side=tk.LEFT, padx=(10, 0))
        
        # Address
        address_frame = ttk.Frame(section_frame)
        address_frame.pack(fill=tk.X, pady=2)
        ttk.Label(address_frame, text="Address:", width=15).pack(side=tk.LEFT)
        self.profile_form_vars["personal_info"]["address"] = tk.StringVar()
        ttk.Entry(address_frame, textvariable=self.profile_form_vars["personal_info"]["address"], 
                 width=40).pack(side=tk.LEFT, padx=(10, 0))
        
        # LinkedIn
        linkedin_frame = ttk.Frame(section_frame)
        linkedin_frame.pack(fill=tk.X, pady=2)
        ttk.Label(linkedin_frame, text="LinkedIn:", width=15).pack(side=tk.LEFT)
        self.profile_form_vars["personal_info"]["linkedin"] = tk.StringVar()
        ttk.Entry(linkedin_frame, textvariable=self.profile_form_vars["personal_info"]["linkedin"], 
                 width=40).pack(side=tk.LEFT, padx=(10, 0))
    
    def _create_summary_section(self, parent: ttk.Widget) -> None:
        """Create professional summary form section"""
        section_frame = ttk.LabelFrame(parent, text="Professional Summary", padding=10)
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(section_frame, text="Professional Summary:").pack(anchor=tk.W)
        self.profile_form_vars["summary"] = tk.Text(section_frame, height=4, wrap=tk.WORD)
        self.profile_form_vars["summary"].pack(fill=tk.X, pady=(5, 0))
    
    def _create_work_experience_section(self, parent: ttk.Widget) -> None:
        """Create work experience form section"""
        section_frame = ttk.LabelFrame(parent, text="Work Experience", padding=10)
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Work experience list
        self.work_exp_frame = ttk.Frame(section_frame)
        self.work_exp_frame.pack(fill=tk.X)
        
        self.profile_form_vars["work_experience"] = []
        
        # Add work experience button
        ttk.Button(section_frame, text="Add Work Experience", 
                  command=self._add_work_experience).pack(pady=(10, 0))
        
        # Add initial work experience entry
        self._add_work_experience()
    
    def _create_education_section(self, parent: ttk.Widget) -> None:
        """Create education form section"""
        section_frame = ttk.LabelFrame(parent, text="Education", padding=10)
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Education list
        self.education_frame = ttk.Frame(section_frame)
        self.education_frame.pack(fill=tk.X)
        
        self.profile_form_vars["education"] = []
        
        # Add education button
        ttk.Button(section_frame, text="Add Education", 
                  command=self._add_education).pack(pady=(10, 0))
        
        # Add initial education entry
        self._add_education()
    
    def _create_skills_section(self, parent: ttk.Widget) -> None:
        """Create skills form section"""
        section_frame = ttk.LabelFrame(parent, text="Skills", padding=10)
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.profile_form_vars["skills"] = {}
        
        # Technical skills
        tech_frame = ttk.Frame(section_frame)
        tech_frame.pack(fill=tk.X, pady=2)
        ttk.Label(tech_frame, text="Technical Skills:", width=20).pack(side=tk.LEFT)
        self.profile_form_vars["skills"]["technical"] = tk.Text(tech_frame, height=2, wrap=tk.WORD)
        self.profile_form_vars["skills"]["technical"].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Soft skills
        soft_frame = ttk.Frame(section_frame)
        soft_frame.pack(fill=tk.X, pady=2)
        ttk.Label(soft_frame, text="Soft Skills:", width=20).pack(side=tk.LEFT)
        self.profile_form_vars["skills"]["soft"] = tk.Text(soft_frame, height=2, wrap=tk.WORD)
        self.profile_form_vars["skills"]["soft"].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Languages
        lang_frame = ttk.Frame(section_frame)
        lang_frame.pack(fill=tk.X, pady=2)
        ttk.Label(lang_frame, text="Languages:", width=20).pack(side=tk.LEFT)
        self.profile_form_vars["skills"]["languages"] = tk.Text(lang_frame, height=2, wrap=tk.WORD)
        self.profile_form_vars["skills"]["languages"].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Certifications
        cert_frame = ttk.Frame(section_frame)
        cert_frame.pack(fill=tk.X, pady=2)
        ttk.Label(cert_frame, text="Certifications:", width=20).pack(side=tk.LEFT)
        self.profile_form_vars["skills"]["certifications"] = tk.Text(cert_frame, height=2, wrap=tk.WORD)
        self.profile_form_vars["skills"]["certifications"].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Instructions
        ttk.Label(section_frame, text="Enter skills separated by commas", 
                 font=('Arial', 8), foreground='gray').pack(pady=(5, 0))
    
    def _create_projects_section(self, parent: ttk.Widget) -> None:
        """Create projects form section"""
        section_frame = ttk.LabelFrame(parent, text="Projects", padding=10)
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Projects list
        self.projects_frame = ttk.Frame(section_frame)
        self.projects_frame.pack(fill=tk.X)
        
        self.profile_form_vars["projects"] = []
        
        # Add project button
        ttk.Button(section_frame, text="Add Project", 
                  command=self._add_project).pack(pady=(10, 0))
    
    def _add_work_experience(self) -> None:
        """Add a new work experience entry"""
        exp_frame = ttk.LabelFrame(self.work_exp_frame, text=f"Experience {len(self.profile_form_vars['work_experience']) + 1}", 
                                  padding=5)
        exp_frame.pack(fill=tk.X, pady=(0, 5))
        
        exp_vars = {}
        
        # Company and Position row
        row1 = ttk.Frame(exp_frame)
        row1.pack(fill=tk.X, pady=2)
        
        ttk.Label(row1, text="Company*:", width=12).pack(side=tk.LEFT)
        exp_vars["company"] = tk.StringVar()
        ttk.Entry(row1, textvariable=exp_vars["company"], width=25).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(row1, text="Position*:", width=12).pack(side=tk.LEFT)
        exp_vars["position"] = tk.StringVar()
        ttk.Entry(row1, textvariable=exp_vars["position"], width=25).pack(side=tk.LEFT, padx=(5, 0))
        
        # Dates row
        row2 = ttk.Frame(exp_frame)
        row2.pack(fill=tk.X, pady=2)
        
        ttk.Label(row2, text="Start Date*:", width=12).pack(side=tk.LEFT)
        exp_vars["start_date"] = tk.StringVar()
        ttk.Entry(row2, textvariable=exp_vars["start_date"], width=25).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(row2, text="End Date:", width=12).pack(side=tk.LEFT)
        exp_vars["end_date"] = tk.StringVar()
        ttk.Entry(row2, textvariable=exp_vars["end_date"], width=25).pack(side=tk.LEFT, padx=(5, 0))
        
        # Description
        ttk.Label(exp_frame, text="Description:").pack(anchor=tk.W, pady=(5, 0))
        exp_vars["description"] = tk.Text(exp_frame, height=3, wrap=tk.WORD)
        exp_vars["description"].pack(fill=tk.X, pady=(2, 5))
        
        # Achievements
        ttk.Label(exp_frame, text="Achievements (one per line):").pack(anchor=tk.W)
        exp_vars["achievements"] = tk.Text(exp_frame, height=3, wrap=tk.WORD)
        exp_vars["achievements"].pack(fill=tk.X, pady=(2, 5))
        
        # Remove button
        ttk.Button(exp_frame, text="Remove", 
                  command=lambda: self._remove_work_experience(exp_frame, exp_vars)).pack(anchor=tk.E)
        
        self.profile_form_vars["work_experience"].append(exp_vars)
    
    def _add_education(self) -> None:
        """Add a new education entry"""
        edu_frame = ttk.LabelFrame(self.education_frame, text=f"Education {len(self.profile_form_vars['education']) + 1}", 
                                  padding=5)
        edu_frame.pack(fill=tk.X, pady=(0, 5))
        
        edu_vars = {}
        
        # Institution and Degree row
        row1 = ttk.Frame(edu_frame)
        row1.pack(fill=tk.X, pady=2)
        
        ttk.Label(row1, text="Institution*:", width=12).pack(side=tk.LEFT)
        edu_vars["institution"] = tk.StringVar()
        ttk.Entry(row1, textvariable=edu_vars["institution"], width=25).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(row1, text="Degree*:", width=12).pack(side=tk.LEFT)
        edu_vars["degree"] = tk.StringVar()
        ttk.Entry(row1, textvariable=edu_vars["degree"], width=25).pack(side=tk.LEFT, padx=(5, 0))
        
        # Field and Date row
        row2 = ttk.Frame(edu_frame)
        row2.pack(fill=tk.X, pady=2)
        
        ttk.Label(row2, text="Field:", width=12).pack(side=tk.LEFT)
        edu_vars["field"] = tk.StringVar()
        ttk.Entry(row2, textvariable=edu_vars["field"], width=25).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(row2, text="Graduation:", width=12).pack(side=tk.LEFT)
        edu_vars["graduation_date"] = tk.StringVar()
        ttk.Entry(row2, textvariable=edu_vars["graduation_date"], width=25).pack(side=tk.LEFT, padx=(5, 0))
        
        # GPA
        row3 = ttk.Frame(edu_frame)
        row3.pack(fill=tk.X, pady=2)
        
        ttk.Label(row3, text="GPA:", width=12).pack(side=tk.LEFT)
        edu_vars["gpa"] = tk.StringVar()
        ttk.Entry(row3, textvariable=edu_vars["gpa"], width=10).pack(side=tk.LEFT, padx=(5, 0))
        
        # Remove button
        ttk.Button(edu_frame, text="Remove", 
                  command=lambda: self._remove_education(edu_frame, edu_vars)).pack(anchor=tk.E, pady=(5, 0))
        
        self.profile_form_vars["education"].append(edu_vars)
    
    def _add_project(self) -> None:
        """Add a new project entry"""
        proj_frame = ttk.LabelFrame(self.projects_frame, text=f"Project {len(self.profile_form_vars['projects']) + 1}", 
                                   padding=5)
        proj_frame.pack(fill=tk.X, pady=(0, 5))
        
        proj_vars = {}
        
        # Name and URL row
        row1 = ttk.Frame(proj_frame)
        row1.pack(fill=tk.X, pady=2)
        
        ttk.Label(row1, text="Project Name:", width=15).pack(side=tk.LEFT)
        proj_vars["name"] = tk.StringVar()
        ttk.Entry(row1, textvariable=proj_vars["name"], width=30).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(row1, text="URL:", width=8).pack(side=tk.LEFT)
        proj_vars["url"] = tk.StringVar()
        ttk.Entry(row1, textvariable=proj_vars["url"], width=30).pack(side=tk.LEFT, padx=(5, 0))
        
        # Description
        ttk.Label(proj_frame, text="Description:").pack(anchor=tk.W, pady=(5, 0))
        proj_vars["description"] = tk.Text(proj_frame, height=3, wrap=tk.WORD)
        proj_vars["description"].pack(fill=tk.X, pady=(2, 5))
        
        # Technologies
        ttk.Label(proj_frame, text="Technologies (comma-separated):").pack(anchor=tk.W)
        proj_vars["technologies"] = tk.Text(proj_frame, height=2, wrap=tk.WORD)
        proj_vars["technologies"].pack(fill=tk.X, pady=(2, 5))
        
        # Remove button
        ttk.Button(proj_frame, text="Remove", 
                  command=lambda: self._remove_project(proj_frame, proj_vars)).pack(anchor=tk.E)
        
        self.profile_form_vars["projects"].append(proj_vars)
    
    def _remove_work_experience(self, frame: ttk.Widget, exp_vars: Dict) -> None:
        """Remove a work experience entry"""
        frame.destroy()
        if exp_vars in self.profile_form_vars["work_experience"]:
            self.profile_form_vars["work_experience"].remove(exp_vars)
    
    def _remove_education(self, frame: ttk.Widget, edu_vars: Dict) -> None:
        """Remove an education entry"""
        frame.destroy()
        if edu_vars in self.profile_form_vars["education"]:
            self.profile_form_vars["education"].remove(edu_vars)
    
    def _remove_project(self, frame: ttk.Widget, proj_vars: Dict) -> None:
        """Remove a project entry"""
        frame.destroy()
        if proj_vars in self.profile_form_vars["projects"]:
            self.profile_form_vars["projects"].remove(proj_vars)  
  
    def _populate_profile_form(self, profile_data: Dict[str, Any]) -> None:
        """Populate form fields with existing profile data"""
        try:
            # Personal info
            if "personal_info" in profile_data:
                personal_info = profile_data["personal_info"]
                for field, var in self.profile_form_vars["personal_info"].items():
                    if field in personal_info:
                        var.set(personal_info[field])
            
            # Summary
            if "summary" in profile_data and profile_data["summary"]:
                self.profile_form_vars["summary"].delete(1.0, tk.END)
                self.profile_form_vars["summary"].insert(1.0, profile_data["summary"])
            
            # Work experience
            if "work_experience" in profile_data:
                # Clear existing entries
                for exp_vars in self.profile_form_vars["work_experience"]:
                    for widget in self.work_exp_frame.winfo_children():
                        widget.destroy()
                self.profile_form_vars["work_experience"] = []
                
                # Add entries for each work experience
                for exp_data in profile_data["work_experience"]:
                    self._add_work_experience()
                    exp_vars = self.profile_form_vars["work_experience"][-1]
                    
                    for field, var in exp_vars.items():
                        if field in exp_data:
                            if isinstance(var, tk.StringVar):
                                var.set(exp_data[field])
                            elif isinstance(var, tk.Text):
                                var.delete(1.0, tk.END)
                                if field == "achievements" and isinstance(exp_data[field], list):
                                    var.insert(1.0, "\n".join(exp_data[field]))
                                else:
                                    var.insert(1.0, str(exp_data[field]))
            
            # Education
            if "education" in profile_data:
                # Clear existing entries
                for edu_vars in self.profile_form_vars["education"]:
                    for widget in self.education_frame.winfo_children():
                        widget.destroy()
                self.profile_form_vars["education"] = []
                
                # Add entries for each education
                for edu_data in profile_data["education"]:
                    self._add_education()
                    edu_vars = self.profile_form_vars["education"][-1]
                    
                    for field, var in edu_vars.items():
                        if field in edu_data:
                            var.set(str(edu_data[field]))
            
            # Skills
            if "skills" in profile_data:
                skills_data = profile_data["skills"]
                for skill_type, widget in self.profile_form_vars["skills"].items():
                    if skill_type in skills_data and isinstance(skills_data[skill_type], list):
                        widget.delete(1.0, tk.END)
                        widget.insert(1.0, ", ".join(skills_data[skill_type]))
            
            # Projects
            if "projects" in profile_data:
                # Clear existing entries
                for proj_vars in self.profile_form_vars["projects"]:
                    for widget in self.projects_frame.winfo_children():
                        widget.destroy()
                self.profile_form_vars["projects"] = []
                
                # Add entries for each project
                for proj_data in profile_data["projects"]:
                    self._add_project()
                    proj_vars = self.profile_form_vars["projects"][-1]
                    
                    for field, var in proj_vars.items():
                        if field in proj_data:
                            if isinstance(var, tk.StringVar):
                                var.set(proj_data[field])
                            elif isinstance(var, tk.Text):
                                var.delete(1.0, tk.END)
                                if field == "technologies" and isinstance(proj_data[field], list):
                                    var.insert(1.0, ", ".join(proj_data[field]))
                                else:
                                    var.insert(1.0, str(proj_data[field]))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error populating form: {str(e)}")
    
    def _collect_profile_data(self) -> Dict[str, Any]:
        """Collect data from form fields"""
        try:
            profile_data = {}
            
            # Personal info
            profile_data["personal_info"] = {}
            for field, var in self.profile_form_vars["personal_info"].items():
                profile_data["personal_info"][field] = var.get().strip()
            
            # Summary
            profile_data["summary"] = self.profile_form_vars["summary"].get(1.0, tk.END).strip()
            
            # Work experience
            profile_data["work_experience"] = []
            for exp_vars in self.profile_form_vars["work_experience"]:
                exp_data = {}
                for field, var in exp_vars.items():
                    if isinstance(var, tk.StringVar):
                        exp_data[field] = var.get().strip()
                    elif isinstance(var, tk.Text):
                        content = var.get(1.0, tk.END).strip()
                        if field == "achievements":
                            exp_data[field] = [line.strip() for line in content.split('\n') if line.strip()]
                        else:
                            exp_data[field] = content
                
                # Only add if has required fields
                if exp_data.get("company") and exp_data.get("position"):
                    profile_data["work_experience"].append(exp_data)
            
            # Education
            profile_data["education"] = []
            for edu_vars in self.profile_form_vars["education"]:
                edu_data = {}
                for field, var in edu_vars.items():
                    value = var.get().strip()
                    if field == "gpa" and value:
                        try:
                            edu_data[field] = float(value)
                        except ValueError:
                            edu_data[field] = 0.0
                    else:
                        edu_data[field] = value
                
                # Only add if has required fields
                if edu_data.get("institution") and edu_data.get("degree"):
                    profile_data["education"].append(edu_data)
            
            # Skills
            profile_data["skills"] = {}
            for skill_type, widget in self.profile_form_vars["skills"].items():
                content = widget.get(1.0, tk.END).strip()
                if content:
                    profile_data["skills"][skill_type] = [skill.strip() for skill in content.split(',') if skill.strip()]
                else:
                    profile_data["skills"][skill_type] = []
            
            # Projects
            profile_data["projects"] = []
            for proj_vars in self.profile_form_vars["projects"]:
                proj_data = {}
                for field, var in proj_vars.items():
                    if isinstance(var, tk.StringVar):
                        proj_data[field] = var.get().strip()
                    elif isinstance(var, tk.Text):
                        content = var.get(1.0, tk.END).strip()
                        if field == "technologies":
                            proj_data[field] = [tech.strip() for tech in content.split(',') if tech.strip()]
                        else:
                            proj_data[field] = content
                
                # Only add if has name
                if proj_data.get("name"):
                    profile_data["projects"].append(proj_data)
            
            return profile_data
            
        except Exception as e:
            messagebox.showerror("Error", f"Error collecting form data: {str(e)}")
            return {}
    
    def _save_profile_form(self) -> None:
        """Save profile data from form"""
        try:
            profile_data = self._collect_profile_data()
            if not profile_data:
                return
            
            if self.controller:
                # Use controller
                validation_errors = self.controller.validate_profile(profile_data)
                if validation_errors:
                    error_msg = "Profile validation failed:\n\n" + "\n".join(f"• {error}" for error in validation_errors)
                    messagebox.showerror("Validation Error", error_msg)
                    return
                
                # Save profile
                if self.controller.update_profile(profile_data):
                    self.current_profile = profile_data
                    messagebox.showinfo("Success", "Profile saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save profile. Please check the console for details.")
            else:
                # Fallback to direct model access
                validation_errors = self.profile_manager.validate_profile(profile_data)
                if validation_errors:
                    error_msg = "Profile validation failed:\n\n" + "\n".join(f"• {error}" for error in validation_errors)
                    messagebox.showerror("Validation Error", error_msg)
                    return
                
                if self.profile_manager.update_profile(profile_data):
                    self.current_profile = profile_data
                    messagebox.showinfo("Success", "Profile saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save profile. Please check the console for details.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving profile: {str(e)}")
    
    def _validate_profile_form(self) -> None:
        """Validate profile data without saving"""
        try:
            profile_data = self._collect_profile_data()
            if not profile_data:
                return
            
            validation_errors = self.profile_manager.validate_profile(profile_data)
            if validation_errors:
                error_msg = "Profile validation failed:\n\n" + "\n".join(f"• {error}" for error in validation_errors)
                messagebox.showerror("Validation Error", error_msg)
            else:
                messagebox.showinfo("Validation Success", "Profile data is valid!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error validating profile: {str(e)}")
    
    def _clear_profile_form(self) -> None:
        """Clear all form fields"""
        try:
            # Confirm action
            if messagebox.askyesno("Confirm", "Are you sure you want to clear all form data?"):
                # Clear personal info
                for var in self.profile_form_vars["personal_info"].values():
                    var.set("")
                
                # Clear summary
                self.profile_form_vars["summary"].delete(1.0, tk.END)
                
                # Clear skills
                for widget in self.profile_form_vars["skills"].values():
                    widget.delete(1.0, tk.END)
                
                # Clear work experience
                for widget in self.work_exp_frame.winfo_children():
                    widget.destroy()
                self.profile_form_vars["work_experience"] = []
                self._add_work_experience()
                
                # Clear education
                for widget in self.education_frame.winfo_children():
                    widget.destroy()
                self.profile_form_vars["education"] = []
                self._add_education()
                
                # Clear projects
                for widget in self.projects_frame.winfo_children():
                    widget.destroy()
                self.profile_form_vars["projects"] = []
                
        except Exception as e:
            messagebox.showerror("Error", f"Error clearing form: {str(e)}")
    
    def _analyze_job_description(self) -> None:
        """Analyze the job description and display results"""
        try:
            job_text = self.job_text_widget.get(1.0, tk.END).strip()
            if not job_text:
                messagebox.showwarning("No Input", "Please enter a job description to analyze.")
                return
            
            if self.controller:
                # Use controller
                analysis = self.controller.analyze_job_description(job_text)
                if analysis:
                    self.current_job_analysis = analysis
                    self._display_job_analysis(analysis)
                else:
                    messagebox.showerror("Error", "Failed to analyze job description.")
            else:
                # Fallback to direct model access
                keywords = self.job_analyzer.extract_keywords(job_text)
                requirements = self.job_analyzer.identify_requirements(job_text)
                
                # Calculate relevance score if profile exists
                relevance_score = 0.0
                if self.current_profile:
                    relevance_score = self.job_analyzer.calculate_relevance_score(self.current_profile, requirements)
                
                # Store analysis results
                self.current_job_analysis = {
                    "keywords": keywords,
                    **requirements,
                    "relevance_score": relevance_score
                }
                
                # Display results
                self._display_job_analysis(self.current_job_analysis)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error analyzing job description: {str(e)}")
    
    def _display_job_analysis(self, analysis: Dict[str, Any]) -> None:
        """Display job analysis results"""
        # Clear previous results
        for widget in self.analysis_frame.winfo_children():
            widget.destroy()
        
        # Show analysis frame
        self.analysis_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create notebook for tabbed results
        notebook = ttk.Notebook(self.analysis_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Keywords tab
        keywords_frame = ttk.Frame(notebook)
        notebook.add(keywords_frame, text="Keywords")
        
        keywords_text = scrolledtext.ScrolledText(keywords_frame, height=8, wrap=tk.WORD)
        keywords_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        keywords_content = "Top Keywords Found:\n\n" + "\n".join(f"• {keyword}" for keyword in analysis.get("keywords", []))
        keywords_text.insert(1.0, keywords_content)
        keywords_text.config(state=tk.DISABLED)
        
        # Requirements tab
        req_frame = ttk.Frame(notebook)
        notebook.add(req_frame, text="Requirements")
        
        req_text = scrolledtext.ScrolledText(req_frame, height=8, wrap=tk.WORD)
        req_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        req_content = self._format_requirements(analysis)
        req_text.insert(1.0, req_content)
        req_text.config(state=tk.DISABLED)
        
        # Match score tab (if profile exists)
        if self.current_profile:
            score_frame = ttk.Frame(notebook)
            notebook.add(score_frame, text="Match Score")
            
            score_text = scrolledtext.ScrolledText(score_frame, height=8, wrap=tk.WORD)
            score_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            score_content = f"Profile Match Score: {analysis.get('relevance_score', 0.0):.1%}\n\n"
            score_content += self._generate_match_feedback(analysis.get('relevance_score', 0.0))
            score_text.insert(1.0, score_content)
            score_text.config(state=tk.DISABLED)
    
    def _format_requirements(self, analysis: Dict[str, Any]) -> str:
        """Format requirements for display"""
        content = "Job Requirements Analysis:\n\n"
        
        if analysis.get("required_skills"):
            content += "Required Skills:\n"
            content += "\n".join(f"• {skill}" for skill in analysis["required_skills"])
            content += "\n\n"
        
        if analysis.get("preferred_skills"):
            content += "Preferred Skills:\n"
            content += "\n".join(f"• {skill}" for skill in analysis["preferred_skills"])
            content += "\n\n"
        
        if analysis.get("experience_level"):
            content += f"Experience Level: {analysis['experience_level']}\n\n"
        
        if analysis.get("education_requirements"):
            content += f"Education: {analysis['education_requirements']}\n\n"
        
        if analysis.get("key_responsibilities"):
            content += "Key Responsibilities:\n"
            content += "\n".join(f"• {resp}" for resp in analysis["key_responsibilities"])
            content += "\n\n"
        
        if analysis.get("company_info"):
            content += f"Company Info:\n{analysis['company_info']}"
        
        return content
    
    def _generate_match_feedback(self, score: float) -> str:
        """Generate feedback based on match score"""
        if score >= 0.8:
            return "Excellent match! Your profile aligns very well with this job."
        elif score >= 0.6:
            return "Good match! You meet most of the requirements for this position."
        elif score >= 0.4:
            return "Moderate match. Consider highlighting relevant skills and experience."
        else:
            return "Limited match. You may want to develop additional skills for this role."
    
    def _clear_job_input(self) -> None:
        """Clear job description input"""
        self.job_text_widget.delete(1.0, tk.END)
        self.analysis_frame.pack_forget()
        self.current_job_analysis = None
    
    def _generate_resume(self) -> None:
        """Generate tailored resume"""
        try:
            if self.controller:
                # Use controller
                resume_data = self.controller.generate_resume()
                if resume_data:
                    self.current_resume = resume_data
                    self.show_resume_preview()
                    messagebox.showinfo("Success", "Resume generated successfully!")
                else:
                    messagebox.showerror("Error", "Failed to generate resume. Please ensure you have a profile and job analysis.")
            else:
                # Fallback to direct model access
                if not self.current_profile:
                    messagebox.showwarning("No Profile", "Please create a profile first.")
                    return
                
                if not self.current_job_analysis:
                    messagebox.showwarning("No Job Analysis", "Please analyze a job description first.")
                    return
                
                # Generate resume
                resume_data = self.resume_generator.generate_resume(self.current_profile, self.current_job_analysis)
                self.current_resume = resume_data
                
                # Show resume preview
                self.show_resume_preview()
                
                messagebox.showinfo("Success", "Resume generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating resume: {str(e)}")
    
    def _format_current_resume(self) -> str:
        """Format current resume for display"""
        if not self.current_resume:
            return "No resume generated."
        
        return self.resume_generator.format_resume(self.current_resume)
    
    def _regenerate_resume(self) -> None:
        """Regenerate resume with current data"""
        if not self.current_profile or not self.current_job_analysis:
            messagebox.showwarning("Missing Data", "Please ensure you have both a profile and job analysis.")
            return
        
        self._generate_resume()
    
    def _export_resume(self, format_type: str = None) -> None:
        """Export resume using the controller"""
        try:
            if self.controller:
                # Use controller's export functionality
                exported_file = self.controller.export_resume("dialog")
                if exported_file:
                    # Success message is shown by the export manager
                    pass
            else:
                # Fallback to legacy export
                if not self.current_resume:
                    messagebox.showwarning("No Resume", "Please generate a resume first.")
                    return
                
                resume_content = self._format_current_resume()
                
                # File type mappings
                file_types = {
                    "pdf": [("PDF files", "*.pdf")],
                    "docx": [("Word documents", "*.docx")],
                    "txt": [("Text files", "*.txt")]
                }
                
                if not format_type:
                    format_type = "txt"  # Default
                
                filename = filedialog.asksaveasfilename(
                    defaultextension=f".{format_type}",
                    filetypes=file_types.get(format_type, [("All files", "*.*")])
                )
                
                if filename:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(resume_content)
                    
                    messagebox.showinfo("Success", f"Resume exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting resume: {str(e)}")
    
    def _export_and_close(self, dialog: tk.Toplevel, format_type: str) -> None:
        """Export resume and close dialog"""
        dialog.destroy()
        self._export_resume(format_type)
    
    # Menu handlers
    def _new_profile(self) -> None:
        """Create new profile"""
        if messagebox.askyesno("New Profile", "This will clear the current profile. Continue?"):
            self.current_profile = None
            self._clear_profile_form()
    
    def _load_profile(self) -> None:
        """Load profile from file"""
        try:
            if self.controller:
                # Use controller
                profile = self.controller.load_profile()
                if profile:
                    self.current_profile = profile
                    self.show_profile_form()  # Refresh form with loaded data
                    messagebox.showinfo("Success", "Profile loaded successfully!")
                else:
                    messagebox.showinfo("No Profile", "No profile found to load.")
            else:
                # Fallback to direct model access
                self.current_profile = self.profile_manager.load_profile()
                if self.current_profile:
                    self.show_profile_form()  # Refresh form with loaded data
                    messagebox.showinfo("Success", "Profile loaded successfully!")
                else:
                    messagebox.showinfo("No Profile", "No profile found to load.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading profile: {str(e)}")
    
    def _save_profile(self) -> None:
        """Save current profile"""
        self._save_profile_form()
    
    def _show_about(self) -> None:
        """Show about dialog"""
        about_text = """Resume Tailoring App v1.0

A Python desktop application for creating tailored resumes based on job descriptions.

Features:
• Profile management
• Job description analysis
• Automated resume generation
• Multiple export formats

Built with Python and Tkinter"""
        
        messagebox.showinfo("About", about_text)
    
    def _clear_all_history(self) -> None:
        """Clear all resume export history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all export history?"):
            if self.controller and self.controller.clear_resume_history():
                messagebox.showinfo("Success", "History cleared successfully!")
                self.show_history_view()  # Refresh view
            else:
                messagebox.showerror("Error", "Failed to clear history.")
    
    def _delete_selected_history(self) -> None:
        """Delete selected history entry"""
        if not hasattr(self, 'history_tree'):
            return
        
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a history entry to delete.")
            return
        
        if messagebox.askyesno("Delete Entry", "Are you sure you want to delete the selected history entry?"):
            for item in selection:
                tags = self.history_tree.item(item, "tags")
                if tags and self.controller:
                    entry_id = tags[0]
                    if self.controller.delete_history_entry(entry_id):
                        self.history_tree.delete(item)
                    else:
                        messagebox.showerror("Error", "Failed to delete history entry.")
    
    def _open_file_location(self) -> None:
        """Open file location for selected history entry"""
        if not hasattr(self, 'history_tree'):
            return
        
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a history entry.")
            return
        
        # Get the filename from the selected item
        item = selection[0]
        values = self.history_tree.item(item, "values")
        if len(values) > 1:
            filename = values[1]  # filename column
            
            # Get full path from history
            if self.controller:
                history = self.controller.get_resume_history()
                for entry in history:
                    if entry.get("filename", "").endswith(filename):
                        full_path = entry.get("filename", "")
                        if full_path and os.path.exists(full_path):
                            # Open file location
                            import subprocess
                            import platform
                            
                            try:
                                if platform.system() == "Windows":
                                    subprocess.run(["explorer", "/select,", full_path])
                                elif platform.system() == "Darwin":  # macOS
                                    subprocess.run(["open", "-R", full_path])
                                else:  # Linux
                                    subprocess.run(["xdg-open", os.path.dirname(full_path)])
                            except Exception as e:
                                messagebox.showerror("Error", f"Could not open file location: {str(e)}")
                        else:
                            messagebox.showwarning("File Not Found", "The exported file no longer exists.")
                        break
    
    def _show_history_context_menu(self, event) -> None:
        """Show context menu for history items"""
        if not hasattr(self, 'history_tree'):
            return
        
        # Select item under cursor
        item = self.history_tree.identify_row(event.y)
        if item:
            self.history_tree.selection_set(item)
            
            # Create context menu
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Delete Entry", command=self._delete_selected_history)
            context_menu.add_command(label="Open File Location", command=self._open_file_location)
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()