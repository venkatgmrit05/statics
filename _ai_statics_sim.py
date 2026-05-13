import tkinter as tk
from tkinter import messagebox
import math

# Default material/section properties (Steel-like, arbitrary standard values)
# E: Young's Modulus (Pa), A: Cross-section Area (m^2), I: Moment of Inertia (m^4)
DEFAULT_E = 200e9 
DEFAULT_A = 0.01   
DEFAULT_I = 1e-5   

# Display scaling: 100 pixels = 1 meter
SCALE = 100.0      

def mat_mul(A, B):
    """Multiplies Matrix A by Matrix/Vector B."""
    if isinstance(B[0], (int, float)): # B is a 1D vector
        res = [0] * len(A)
        for i in range(len(A)):
            res[i] = sum(A[i][k] * B[k] for k in range(len(B)))
        return res
    else: # B is a 2D matrix
        res = [[0] * len(B[0]) for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                res[i][j] = sum(A[i][k] * B[k][j] for k in range(len(A[0])))
        return res

def transpose(A):
    """Returns the transpose of Matrix A."""
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def solve_linear_system(A, b):
    """Solves Ax = b using Gaussian elimination with partial pivoting."""
    n = len(A)
    # Augment matrix
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    for i in range(n):
        # Find pivot
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]

        if abs(M[i][i]) < 1e-12:
            return None # Singular matrix / unstable structure

        # Normalize pivot row
        pivot = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= pivot

        # Eliminate rows below
        for j in range(i + 1, n):
            factor = M[j][i]
            for k in range(i, n + 1):
                M[j][k] -= factor * M[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))
    return x

class Node:
    def __init__(self, node_id, x, y):
        self.id = node_id
        self.x = x # Canvas X
        self.y = y # Canvas Y
        
        # Boundary conditions (True means fixed)
        self.fix_x = False
        self.fix_y = False
        self.fix_t = False # Theta (rotation)
        
        # Applied loads
        self.Fx = 0.0
        self.Fy = 0.0
        self.Mz = 0.0

class Element:
    def __init__(self, elem_id, n1, n2):
        self.id = elem_id
        self.n1 = n1
        self.n2 = n2
        self.E = DEFAULT_E
        self.A = DEFAULT_A
        self.I = DEFAULT_I

class StaticsSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Statics & Structural Simulator")
        self.geometry("1100x700")
        
        self.nodes = []
        self.elements = []
        self.mode = tk.StringVar(value="NODE")
        
        self.selected_node = None # Used for connecting beams
        self.results_text = None
        
        self.setup_ui()

    def setup_ui(self):
        # Left Panel for Controls
        control_frame = tk.Frame(self, width=250, bg="#dad2d2", padx=10, pady=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(control_frame, text="Tools", font=("Arial", 14, "bold"), bg="#25dbb3").pack(pady=(0, 10))
        
        # Modes
        modes = [
            ("Add Node", "NODE"),
            ("Add Beam", "BEAM"),
            ("Support: Pin", "PIN"),
            ("Support: Roller", "ROLLER"),
            ("Support: Fixed", "FIXED"),
            ("Apply Load", "LOAD")
        ]
        
        for text, val in modes:
            tk.Radiobutton(control_frame, text=text, variable=self.mode, value=val, 
                           bg="#0e0e0e", font=("Arial", 11), command=self.on_mode_change).pack(anchor="w", pady=2)
            
        # Load Inputs
        load_frame = tk.LabelFrame(control_frame, text="Load Values", bg="#090606", padx=5, pady=5)
        load_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(load_frame, text="Fx (N):", bg="#080707").grid(row=0, column=0, sticky="w")
        self.entry_fx = tk.Entry(load_frame, width=10)
        self.entry_fx.insert(0, "0")
        self.entry_fx.grid(row=0, column=1)
        
        tk.Label(load_frame, text="Fy (N):", bg="#080101").grid(row=1, column=0, sticky="w")
        self.entry_fy = tk.Entry(load_frame, width=10)
        self.entry_fy.insert(0, "-1000")
        self.entry_fy.grid(row=1, column=1)
        
        tk.Label(load_frame, text="Mz (Nm):", bg="#0b0909").grid(row=2, column=0, sticky="w")
        self.entry_mz = tk.Entry(load_frame, width=10)
        self.entry_mz.insert(0, "0")
        self.entry_mz.grid(row=2, column=1)
        
        # Actions
        tk.Button(control_frame, text="Solve Equilibrium", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                  command=self.solve).pack(fill=tk.X, pady=(20, 5))
        tk.Button(control_frame, text="Clear All", command=self.clear_all).pack(fill=tk.X)
        
        # Output Log
        tk.Label(control_frame, text="Results Log:", bg="#0B0606", font=("Arial", 10, "bold")).pack(anchor="w", pady=(20, 0))
        self.log = tk.Text(control_frame, height=15, width=30, font=("Courier", 9))
        self.log.pack(fill=tk.BOTH, expand=True)
        
        # Canvas
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        self.log_msg("System ready. 100px = 1m.\nPositive Y is UP in math,\nDOWN on screen.")

    def on_mode_change(self):
        self.selected_node = None
        self.redraw()

    def get_nearest_node(self, x, y, threshold=20):
        for node in self.nodes:
            if math.hypot(node.x - x, node.y - y) < threshold:
                return node
        return None

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        mode = self.mode.get()
        
        if mode == "NODE":
            n = Node(len(self.nodes), x, y)
            self.nodes.append(n)
            
        elif mode == "BEAM":
            clicked_node = self.get_nearest_node(x, y)
            if clicked_node:
                if self.selected_node is None:
                    self.selected_node = clicked_node
                else:
                    if self.selected_node != clicked_node:
                        elem = Element(len(self.elements), self.selected_node, clicked_node)
                        self.elements.append(elem)
                    self.selected_node = None
            else:
                self.selected_node = None
                
        elif mode in ["PIN", "ROLLER", "FIXED"]:
            n = self.get_nearest_node(x, y)
            if n:
                if mode == "PIN":
                    n.fix_x, n.fix_y, n.fix_t = True, True, False
                elif mode == "ROLLER":
                    n.fix_x, n.fix_y, n.fix_t = False, True, False
                elif mode == "FIXED":
                    n.fix_x, n.fix_y, n.fix_t = True, True, True
                    
        elif mode == "LOAD":
            n = self.get_nearest_node(x, y)
            if n:
                try:
                    n.Fx = float(self.entry_fx.get())
                    # Convert math Y (up) to canvas Y (down)
                    # A positive input force (upwards) pulls the node visually UP (negative canvas Y)
                    n.Fy = float(self.entry_fy.get()) 
                    n.Mz = float(self.entry_mz.get())
                except ValueError:
                    messagebox.showerror("Input Error", "Forces must be valid numbers.")
                    
        self.redraw()

    def redraw(self):
        self.canvas.delete("all")
        
        # Draw Beams
        for elem in self.elements:
            self.canvas.create_line(elem.n1.x, elem.n1.y, elem.n2.x, elem.n2.y, width=4, fill="#333333")
            
        # Draw Supports and Loads
        for n in self.nodes:
            # Supports
            if n.fix_x and n.fix_y and n.fix_t: # Fixed
                self.canvas.create_rectangle(n.x-15, n.y-5, n.x+15, n.y+15, fill="gray")
            elif n.fix_x and n.fix_y and not n.fix_t: # Pin
                self.canvas.create_polygon(n.x, n.y, n.x-15, n.y+20, n.x+15, n.y+20, fill="white", outline="green", width=2)
            elif not n.fix_x and n.fix_y and not n.fix_t: # Roller
                self.canvas.create_polygon(n.x, n.y, n.x-15, n.y+20, n.x+15, n.y+20, fill="white", outline="green", width=2)
                self.canvas.create_line(n.x-20, n.y+25, n.x+20, n.y+25, fill="green", width=3)

            # Loads
            if abs(n.Fx) > 0 or abs(n.Fy) > 0:
                # Scale arrows purely for visualization
                ax = n.x + (50 if n.Fx > 0 else -50 if n.Fx < 0 else 0)
                ay = n.y - (50 if n.Fy > 0 else -50 if n.Fy < 0 else 0) # Flip Y for visual arrow
                self.canvas.create_line(ax, ay, n.x, n.y, arrow=tk.LAST, fill="red", width=3)
                
            # Nodes
            color = "orange" if n == self.selected_node else "blue"
            self.canvas.create_oval(n.x-6, n.y-6, n.x+6, n.y+6, fill=color, outline="black")

    def clear_all(self):
        self.nodes = []
        self.elements = []
        self.selected_node = None
        self.log.delete(1.0, tk.END)
        self.redraw()

    def log_msg(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def get_element_stiffness(self, E, A, I, L):
        """Generates 6x6 local stiffness matrix for a 2D frame element."""
        k = [[0]*6 for _ in range(6)]
        # Axial terms
        k[0][0] = k[3][3] = E*A/L
        k[0][3] = k[3][0] = -E*A/L
        # Bending/Shear terms
        k[1][1] = k[4][4] = 12*E*I/(L**3)
        k[1][4] = k[4][1] = -12*E*I/(L**3)
        k[1][2] = k[1][5] = k[2][1] = k[5][1] = 6*E*I/(L**2)
        k[4][2] = k[4][5] = k[2][4] = k[5][4] = -6*E*I/(L**2)
        k[2][2] = k[5][5] = 4*E*I/L
        k[2][5] = k[5][2] = 2*E*I/L
        return k

    def get_transformation_matrix(self, dx, dy, L):
        """Generates 6x6 transformation matrix from local to global coordinates."""
        c = dx / L
        s = dy / L
        T = [[0]*6 for _ in range(6)]
        T[0][0] = T[1][1] = T[3][3] = T[4][4] = c
        T[0][1] = T[3][4] = s
        T[1][0] = T[4][3] = -s
        T[2][2] = T[5][5] = 1
        return T

    def solve(self):
        if not self.nodes or not self.elements:
            messagebox.showwarning("Incomplete", "Please add nodes and beams first.")
            return

        N = len(self.nodes)
        total_dof = 3 * N
        
        # Initialize Global Stiffness Matrix (K) and Force Vector (F)
        K_global = [[0]*total_dof for _ in range(total_dof)]
        F_global = [0] * total_dof

        # Assemble Global Stiffness Matrix
        for elem in self.elements:
            n1, n2 = elem.n1, elem.n2
            
            # Convert screen coordinates to math distances
            dx = (n2.x - n1.x) / SCALE
            dy = -(n2.y - n1.y) / SCALE # Flip Y axis to standard math (Up = Positive)
            
            L = math.hypot(dx, dy)
            if L == 0: continue

            k_local = self.get_element_stiffness(elem.E, elem.A, elem.I, L)
            T = self.get_transformation_matrix(dx, dy, L)
            T_trans = transpose(T)
            
            # k_g = T^T * k_local * T
            k_g = mat_mul(T_trans, mat_mul(k_local, T))

            # Mapping indices
            idx = [n1.id*3, n1.id*3+1, n1.id*3+2, n2.id*3, n2.id*3+1, n2.id*3+2]
            
            for i in range(6):
                for j in range(6):
                    K_global[idx[i]][idx[j]] += k_g[i][j]

        # Assemble Force Vector
        for n in self.nodes:
            F_global[n.id*3] = n.Fx
            F_global[n.id*3+1] = n.Fy
            F_global[n.id*3+2] = n.Mz

        # Save a copy of K for reaction calculations
        import copy
        K_original = copy.deepcopy(K_global)

        # Apply Boundary Conditions via Penalty Method
        penalty = 1e15
        for n in self.nodes:
            if n.fix_x: K_global[n.id*3][n.id*3] += penalty
            if n.fix_y: K_global[n.id*3+1][n.id*3+1] += penalty
            if n.fix_t: K_global[n.id*3+2][n.id*3+2] += penalty

        # Solve KD = F
        self.log_msg("Solving matrix (size {}x{})...".format(total_dof, total_dof))
        displacements = solve_linear_system(K_global, F_global)

        if displacements is None:
            messagebox.showerror("Math Error", "Structure is mathematically unstable (Singular Matrix). Check your supports.")
            self.log_msg("ERROR: Singular Matrix.")
            return

        # Calculate Reactions: R = K_original * D - F_applied
        internal_forces = mat_mul(K_original, displacements)
        reactions = [internal_forces[i] - F_global[i] for i in range(total_dof)]

        # Print Results
        self.log.delete(1.0, tk.END)
        self.log_msg("--- REACTION FORCES ---")
        has_reactions = False
        
        for n in self.nodes:
            rx = reactions[n.id*3]
            ry = reactions[n.id*3+1]
            rm = reactions[n.id*3+2]
            
            # Print if node is a support and forces are non-negligible
            if n.fix_x or n.fix_y or n.fix_t:
                msg = f"Node {n.id}:\n"
                if n.fix_x: msg += f"  Rx: {rx:.2f} N\n"
                if n.fix_y: msg += f"  Ry: {ry:.2f} N\n"
                if n.fix_t: msg += f"  Mz: {rm:.2f} Nm\n"
                self.log_msg(msg)
                has_reactions = True
                
        if not has_reactions:
            self.log_msg("No reaction forces detected.\nCheck applied loads.")
            
        self.log_msg("Solution Complete.")

if __name__ == "__main__":
    app = StaticsSimulator()
    app.mainloop()
