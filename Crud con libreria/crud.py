import tkinter as tk
from tkinter import messagebox, ttk

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD con Tkinter - Validación de Números")
        
        self.database = []
        self.current_id = 0
        
        self.input_frame = ttk.LabelFrame(root, text="Datos del Usuario")
        self.input_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(self.input_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry = ttk.Entry(self.input_frame)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(self.input_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(self.input_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(self.input_frame, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
        
        def validate_numeric_input(P):
            if P == "" or P.isdigit():
                return True
            else:
                self.root.bell()  
                return False
        
        vcmd = (self.root.register(validate_numeric_input), '%P')
        
        self.telefono_entry = ttk.Entry(self.input_frame, validate="key", validatecommand=vcmd)
        self.telefono_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(padx=10, pady=5, fill="x")
        
        ttk.Button(self.button_frame, text="Agregar", command=self.agregar).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Mostrar", command=self.mostrar).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Actualizar", command=self.actualizar).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=5)
        
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Nombre", "Email", "Teléfono"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Teléfono", text="Teléfono")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Teléfono", width=100)
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_registro)
    
    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.current_id = 0
    
    def agregar(self):
        nombre = self.nombre_entry.get()
        email = self.email_entry.get()
        telefono = self.telefono_entry.get()
        
        if nombre and email and telefono:
            if not telefono.isdigit():
                messagebox.showerror("Error", "El teléfono debe contener solo números")
                return
                
            self.current_id += 1
            self.database.append({
                "id": self.current_id,
                "nombre": nombre,
                "email": email,
                "telefono": telefono
            })
            self.actualizar_treeview()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Registro agregado correctamente")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos")
    
    def mostrar(self):
        if not self.database:
            messagebox.showinfo("Información", "No hay registros para mostrar")
        self.actualizar_treeview()
    
    def actualizar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un registro para actualizar")
            return
            
        nombre = self.nombre_entry.get()
        email = self.email_entry.get()
        telefono = self.telefono_entry.get()
        
        if nombre and email and telefono:
            if not telefono.isdigit():
                messagebox.showerror("Error", "El teléfono debe contener solo números")
                return
                
            item_id = int(self.tree.item(selected_item)['values'][0])
            
            for registro in self.database:
                if registro["id"] == item_id:
                    registro["nombre"] = nombre
                    registro["email"] = email
                    registro["telefono"] = telefono
                    break
            
            self.actualizar_treeview()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Registro actualizado correctamente")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos")
    
    def eliminar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un registro para eliminar")
            return
            
        item_id = int(self.tree.item(selected_item)['values'][0])
        
        for i, registro in enumerate(self.database):
            if registro["id"] == item_id:
                del self.database[i]
                break
        
        self.actualizar_treeview()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Registro eliminado correctamente")
    
    def seleccionar_registro(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.current_id = values[0]
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, values[1])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[2])
            self.telefono_entry.delete(0, tk.END)
            self.telefono_entry.insert(0, values[3])
    
    def actualizar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for registro in self.database:
            self.tree.insert("", "end", values=(
                registro["id"],
                registro["nombre"],
                registro["email"],
                registro["telefono"]
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()