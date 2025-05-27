import tkinter as tk
from tkinter import ttk, messagebox
from enum import Enum

class ReplacementPolicy(Enum):
    FIFO = "FIFO"
    LRU = "LRU"
    LFU = "LFU"

class MemoryManager:
    def __init__(self, num_frames, policy=ReplacementPolicy.FIFO):
        self.num_frames = num_frames
        self.policy = policy
        self.frames = [-1] * num_frames  # -1 represents empty frame
        self.frame_info = {}  # For LRU/LFU tracking
        self.page_table = {}  # Maps (pid, page) -> frame_number
        self.frame_to_page = {}  # Maps frame_number -> (pid, page)
        self.total_accesses = 0
        self.hits = 0
        self.misses = 0
        
    def check_page_in_memory(self, pid, page):
        key = (pid, page)
        return self.page_table.get(key, -1)
        
    def allocate_frame(self, pid, page):
        self.total_accesses += 1
        key = (pid, page)
        
        # Check if page is already in memory
        if key in self.page_table:
            self.hits += 1
            frame = self.page_table[key]
            self._update_access_info(frame)
            return frame
            
        # Page fault occurs
        self.misses += 1
        
        # Find empty frame or choose victim
        frame = self._find_empty_frame()
        if frame is None:
            frame = self._choose_victim()
            
        # Remove old page from mappings if frame was occupied
        if frame in self.frame_to_page:
            old_key = self.frame_to_page[frame]
            del self.page_table[old_key]
            
        # Update mappings
        self.page_table[key] = frame
        self.frame_to_page[frame] = key
        self.frames[frame] = page
        self._update_access_info(frame)
        
        return frame
        
    def deallocate_frames(self, pid):
        # Remove all pages belonging to the process
        pages_to_remove = [(p, f) for (p, page), f in self.page_table.items() if p == pid]
        for _, frame in pages_to_remove:
            self.frames[frame] = -1
            if frame in self.frame_info:
                del self.frame_info[frame]
                
        # Clean up mappings
        self.page_table = {k: v for k, v in self.page_table.items() if k[0] != pid}
        self.frame_to_page = {k: v for k, v in self.frame_to_page.items() if v[0] != pid}
        
    def _find_empty_frame(self):
        try:
            return self.frames.index(-1)
        except ValueError:
            return None
            
    def _choose_victim(self):
        if not self.frame_info:
            return 0
        if self.policy == ReplacementPolicy.FIFO:
            return min(self.frame_info.items(), key=lambda x: x[1])[0]
        elif self.policy == ReplacementPolicy.LRU:
            return min(self.frame_info.items(), key=lambda x: x[1])[0]
        elif self.policy == ReplacementPolicy.LFU:
            return min(self.frame_info.items(), key=lambda x: x[1])[0]
        return 0
            
    def _update_access_info(self, frame):
        current_time = self.total_accesses
        
        if self.policy == ReplacementPolicy.FIFO:
            if frame not in self.frame_info:
                self.frame_info[frame] = current_time
        elif self.policy == ReplacementPolicy.LRU:
            self.frame_info[frame] = current_time
        elif self.policy == ReplacementPolicy.LFU:
            self.frame_info[frame] = self.frame_info.get(frame, 0) + 1
            
    def get_stats(self):
        return {
            'total': self.total_accesses,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': (self.hits / self.total_accesses * 100) if self.total_accesses > 0 else 0,
            'miss_rate': (self.misses / self.total_accesses * 100) if self.total_accesses > 0 else 0
        }
        
    def get_frames(self):
        return self.frames.copy()
        
    def get_page_table(self, pid):
        return {page: frame for (p, page), frame in self.page_table.items() if p == pid}
        
    def get_frame_table(self):
        frame_table = []
        for frame in range(self.num_frames):
            if frame in self.frame_to_page:
                pid, page = self.frame_to_page[frame]
                frame_table.append((frame, pid, page))
            else:
                frame_table.append((frame, -1, -1))
        return frame_table
        
    def reset_stats(self):
        self.total_accesses = 0
        self.hits = 0
        self.misses = 0

class MemoryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Memory Manager Simulator")
        
        # Default frame size
        self.frame_size = 8
        
        # Initialize memory manager with default size and FIFO policy
        self.memory_manager = None  # Will be initialized after frame size is set
        self.processes = {}  # pid -> list of pages
        self.page_tables = {}  # pid -> {page_num -> frame_num}
        self.last_access_result = None  # To track the last page access result
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root, padding="5")
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Left side - Controls
        control_frame = ttk.LabelFrame(main_container, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        # Frame Size Configuration Section
        frame_config = ttk.LabelFrame(control_frame, text="Memory Configuration", padding="5")
        frame_config.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")
        
        ttk.Label(frame_config, text="Number of Frames:").grid(row=0, column=0, pady=5, padx=5)
        self.frame_size_entry = ttk.Entry(frame_config, width=10)
        self.frame_size_entry.insert(0, str(self.frame_size))
        self.frame_size_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Button(frame_config, text="Initialize Memory", 
                  command=self.initialize_memory).grid(row=0, column=2, pady=5, padx=5)
        
        # Create Process Section
        create_frame = ttk.LabelFrame(control_frame, text="Create Process", padding="5")
        create_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
        
        ttk.Label(create_frame, text="Process ID:").grid(row=0, column=0, pady=5, padx=5)
        self.create_pid_entry = ttk.Entry(create_frame, width=10)
        self.create_pid_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(create_frame, text="Number of Pages:").grid(row=1, column=0, pady=5, padx=5)
        self.pages_entry = ttk.Entry(create_frame, width=10)
        self.pages_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Button(create_frame, text="Create Process", 
                  command=self.create_process).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Access Page Section
        access_frame = ttk.LabelFrame(control_frame, text="Access Page", padding="5")
        access_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")
        
        ttk.Label(access_frame, text="Process ID:").grid(row=0, column=0, pady=5, padx=5)
        self.access_pid_entry = ttk.Entry(access_frame, width=10)
        self.access_pid_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(access_frame, text="Page Number:").grid(row=1, column=0, pady=5, padx=5)
        self.page_entry = ttk.Entry(access_frame, width=10)
        self.page_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Button(access_frame, text="Access Page", 
                  command=self.access_page).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Delete Process Section
        delete_frame = ttk.LabelFrame(control_frame, text="Delete Process", padding="5")
        delete_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        
        ttk.Label(delete_frame, text="Process ID:").grid(row=0, column=0, pady=5, padx=5)
        self.delete_pid_entry = ttk.Entry(delete_frame, width=10)
        self.delete_pid_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Button(delete_frame, text="Delete Process", 
                  command=self.delete_process).grid(row=1, column=0, columnspan=2, pady=5)
        
        # Policy selection
        policy_frame = ttk.LabelFrame(control_frame, text="Page Replacement Policy", padding="5")
        policy_frame.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")
        
        self.policy_var = tk.StringVar(value="FIFO")
        policy_combo = ttk.Combobox(policy_frame, textvariable=self.policy_var, 
                                  values=["FIFO", "LRU", "LFU"], state="readonly")
        policy_combo.pack(pady=5)
        policy_combo.bind('<<ComboboxSelected>>', self.change_policy)
        
        # Right side - Display
        display_frame = ttk.Frame(main_container)
        display_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        
        # Statistics Frame
        stats_frame = ttk.LabelFrame(display_frame, text="Memory Statistics", padding="5")
        stats_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Stats display
        self.stats_text = tk.Text(stats_frame, width=30, height=6, font=('TkDefaultFont', 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Last Access Result
        self.access_result_var = tk.StringVar(value="No pages accessed yet")
        access_result_label = ttk.Label(stats_frame, textvariable=self.access_result_var,
                                      font=('TkDefaultFont', 10, 'bold'))
        access_result_label.pack(pady=5)
        
        # Reset Stats Button
        ttk.Button(stats_frame, text="Reset Statistics", 
                  command=self.reset_stats).pack(pady=5)
        
        # Frame table
        frame_frame = ttk.LabelFrame(display_frame, text="Frame Table", padding="5")
        frame_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        self.frame_canvas = tk.Canvas(frame_frame, width=200, height=300)
        self.frame_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Page Tables
        page_tables_frame = ttk.LabelFrame(display_frame, text="Page Tables", padding="5")
        page_tables_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        
        # Create a canvas and scrollbar for page tables
        page_tables_canvas = tk.Canvas(page_tables_frame, width=200, height=200)
        scrollbar = ttk.Scrollbar(page_tables_frame, orient="vertical", command=page_tables_canvas.yview)
        self.page_tables_frame = ttk.Frame(page_tables_canvas)
        
        self.page_tables_frame.bind(
            "<Configure>",
            lambda e: page_tables_canvas.configure(scrollregion=page_tables_canvas.bbox("all"))
        )
        
        page_tables_canvas.create_window((0, 0), window=self.page_tables_frame, anchor="nw")
        page_tables_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        page_tables_canvas.pack(side="left", fill="both", expand=True)
        
        # Process list
        process_frame = ttk.LabelFrame(display_frame, text="Processes", padding="5")
        process_frame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        
        self.process_text = tk.Text(process_frame, width=30, height=10)
        self.process_text.pack(fill=tk.BOTH, expand=True)
        
    def initialize_memory(self):
        try:
            new_size = int(self.frame_size_entry.get())
            if new_size <= 0:
                messagebox.showerror("Error", "Frame size must be positive!")
                return
                
            self.frame_size = new_size
            self.memory_manager = MemoryManager(self.frame_size, ReplacementPolicy.FIFO)
            self.processes.clear()
            self.page_tables.clear()
            self.access_result_var.set("No pages accessed yet")
            self.update_displays()
            messagebox.showinfo("Success", f"Memory initialized with {self.frame_size} frames")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            
    def create_process(self):
        if not self.memory_manager:
            messagebox.showerror("Error", "Please initialize memory first!")
            return
            
        try:
            pid = int(self.create_pid_entry.get())
            num_pages = int(self.pages_entry.get())
            
            if pid in self.processes:
                messagebox.showerror("Error", f"Process {pid} already exists!")
                return
                
            self.processes[pid] = list(range(num_pages))
            self.page_tables[pid] = {}  # Initialize empty page table
            self.update_displays()
            messagebox.showinfo("Success", f"Created process {pid} with {num_pages} pages")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
            
    def access_page(self):
        if not self.memory_manager:
            messagebox.showerror("Error", "Please initialize memory first!")
            return
            
        try:
            pid = int(self.access_pid_entry.get())
            page = int(self.page_entry.get())
            
            if pid not in self.processes:
                messagebox.showerror("Error", f"Process {pid} does not exist!")
                return
                
            if page not in self.processes[pid]:
                messagebox.showerror("Error", f"Page {page} does not exist in process {pid}!")
                return
                
            # Check if page is already in memory
            existing_frame = self.memory_manager.check_page_in_memory(pid, page)
            was_hit = existing_frame != -1
            
            frame = self.memory_manager.allocate_frame(pid, page)
            if frame != -1:
                self.page_tables[pid][page] = frame
                self.update_displays()
                
                # Update access result display
                if was_hit:
                    self.access_result_var.set(f"HIT! Page {page} of PID {pid} found in frame {frame}")
                else:
                    self.access_result_var.set(f"MISS! Page {page} of PID {pid} loaded into frame {frame}")
                    
                # Don't show the messagebox for hits to reduce popup fatigue
                if not was_hit:
                    messagebox.showinfo("Success", f"Page {page} of process {pid} allocated to frame {frame}")
            else:
                messagebox.showerror("Error", "Failed to allocate frame!")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
            
    def delete_process(self):
        if not self.memory_manager:
            messagebox.showerror("Error", "Please initialize memory first!")
            return
            
        try:
            pid = int(self.delete_pid_entry.get())
            
            if pid not in self.processes:
                messagebox.showerror("Error", f"Process {pid} does not exist!")
                return
                
            self.memory_manager.deallocate_frames(pid)
            del self.processes[pid]
            del self.page_tables[pid]  # Remove page table
            self.update_displays()
            messagebox.showinfo("Success", f"Process {pid} deleted")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid process ID")
            
    def change_policy(self, event=None):
        if not self.memory_manager:
            messagebox.showerror("Error", "Please initialize memory first!")
            return
            
        policy_map = {
            "FIFO": ReplacementPolicy.FIFO,
            "LRU": ReplacementPolicy.LRU,
            "LFU": ReplacementPolicy.LFU
        }
        self.memory_manager = MemoryManager(self.frame_size, policy_map[self.policy_var.get()])
        self.update_displays()
        
    def reset_stats(self):
        if self.memory_manager:
            self.memory_manager.reset_stats()
            self.update_displays()
            self.access_result_var.set("Statistics reset")
            
    def update_displays(self):
        if not self.memory_manager:
            return
            
        # Update statistics
        stats = self.memory_manager.get_stats()
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"Total Accesses: {stats['total']}\n")
        self.stats_text.insert(tk.END, f"Hits: {stats['hits']}\n")
        self.stats_text.insert(tk.END, f"Misses: {stats['misses']}\n")
        self.stats_text.insert(tk.END, f"Hit Rate: {stats['hit_rate']:.2f}%\n")
        self.stats_text.insert(tk.END, f"Miss Rate: {stats['miss_rate']:.2f}%\n")
        
        # Update frame table visualization
        self.frame_canvas.delete("all")
        frame_table = self.memory_manager.get_frame_table()
        
        frame_height = 30
        for i, (frame, pid, page) in enumerate(frame_table):
            y = i * frame_height + 5
            # Draw frame rectangle
            self.frame_canvas.create_rectangle(10, y, 190, y + frame_height - 2,
                                            fill="white", outline="black")
            # Draw frame content
            if pid != -1:
                text = f"Frame {frame}: PID {pid}, Page {page}"
                color = f"#{(pid * 100 + 100) % 256:02x}{'ff':2s}{'ff':2s}"
                self.frame_canvas.create_rectangle(10, y, 190, y + frame_height - 2,
                                                fill=color, outline="black")
            else:
                text = f"Frame {frame}: Free"
                color = "white"
            self.frame_canvas.create_text(100, y + frame_height/2, text=text)
            
        # Clear existing page tables
        for widget in self.page_tables_frame.winfo_children():
            widget.destroy()
            
        # Update page tables
        row = 0
        for pid in sorted(self.page_tables.keys()):
            # Create a frame for this process's page table
            table_frame = ttk.LabelFrame(self.page_tables_frame, 
                                       text=f"Process {pid} Page Table", padding="5")
            table_frame.grid(row=row, column=0, pady=5, padx=5, sticky="ew")
            
            # Header
            ttk.Label(table_frame, text="Page").grid(row=0, column=0, padx=5)
            ttk.Label(table_frame, text="Frame").grid(row=0, column=1, padx=5)
            ttk.Label(table_frame, text="Valid").grid(row=0, column=2, padx=5)
            
            # Page table entries
            for i, page in enumerate(self.processes[pid]):
                ttk.Label(table_frame, text=str(page)).grid(row=i+1, column=0, padx=5)
                frame = self.page_tables[pid].get(page, -1)
                ttk.Label(table_frame, text=str(frame if frame != -1 else "")).grid(
                    row=i+1, column=1, padx=5)
                ttk.Label(table_frame, text="Yes" if frame != -1 else "No").grid(
                    row=i+1, column=2, padx=5)
            row += 1
            
        # Update process list
        self.process_text.delete(1.0, tk.END)
        for pid, pages in self.processes.items():
            self.process_text.insert(tk.END, f"Process {pid}: {len(pages)} pages\n")
            self.process_text.insert(tk.END, f"Pages: {pages}\n\n")

def main():
    root = tk.Tk()
    app = MemoryManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
