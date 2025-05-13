import os
import sys
import matplotlib.pyplot as plt
from graph import Graph
from algorithms import BestFirstSearch
from visualization import GraphVisualizer
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class BestFirstSearchApp:
    """
    Application principale pour exécuter et visualiser l'algorithme Best-First Search.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Best-First Search Visualizer")
        self.root.geometry("1200x800")
        
        # Variables
        self.graph = None
        self.visualizer = None
        self.results = None
        
        # Création du répertoire pour les exemples s'il n'existe pas
        os.makedirs("example_graphs", exist_ok=True)
        
        # Créer l'interface utilisateur
        self._create_widgets()
        
    def _create_widgets(self):
        """Crée les widgets de l'interface utilisateur."""
        # Frame principale
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame pour les boutons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        # Boutons
        tk.Button(button_frame, text="Charger un graphe", command=self.load_graph).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Créer un exemple 1", command=self.create_example_1).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Créer un exemple 2", command=self.create_example_2).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Exécuter Best-First Search", command=self.run_bfs).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sauvegarder résultats", command=self.save_results).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Créer Animation", command=self.create_animation).pack(side=tk.LEFT, padx=5)
        
        # Frame pour le graphe
        self.graph_frame = tk.Frame(main_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Zone de texte pour les informations
        self.info_text = tk.Text(main_frame, height=8)
        self.info_text.pack(fill=tk.X, pady=5)
        
        # Message initial
        self.update_info("Bienvenue dans le visualiseur de Best-First Search!\n"
                        "Chargez un graphe ou créez un exemple pour commencer.")
        
    def update_info(self, message):
        """Met à jour la zone d'information avec un message."""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, message)
    
    def load_graph(self):
        """Charge un graphe depuis un fichier JSON."""
        try:
            filename = filedialog.askopenfilename(
                title="Sélectionner un fichier de graphe",
                filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
            )
            
            if not filename:  # L'utilisateur a annulé
                return
            
            self.graph = Graph.load_from_file(filename)
            self.visualizer = GraphVisualizer(self.graph)
            
            self.display_graph()
            self.update_info(f"Graphe chargé depuis {filename}\n"
                           f"Nœud de départ: {self.graph.start_node}\n"
                           f"Nœud d'arrivée: {self.graph.goal_node}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le graphe: {str(e)}")
    
    def create_example_1(self):
        """Crée le premier exemple de graphe."""
        self.graph = Graph()
        self.graph.create_example_graph_1()
        self.visualizer = GraphVisualizer(self.graph)
        
        # Sauvegarder l'exemple
        self.graph.save_to_file("example_graphs/graph1.json")
        
        self.display_graph()
        self.update_info("Exemple 1 créé: graphe simple pour Best-First Search.\n"
                       "Sauvegarder dans example_graphs/graph1.json")
    
    def create_example_2(self):
        """Crée le deuxième exemple de graphe."""
        self.graph = Graph()
        self.graph.create_example_graph_2()
        self.visualizer = GraphVisualizer(self.graph)
        
        # Sauvegarder l'exemple
        self.graph.save_to_file("example_graphs/graph2.json")
        
        self.display_graph()
        self.update_info("Exemple 2 créé: graphe plus complexe pour Best-First Search.\n"
                       "Sauvegarder dans example_graphs/graph2.json")
    
    def display_graph(self):
        """Affiche le graphe dans l'interface."""
        # Effacer les widgets existants dans le frame du graphe
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        if self.graph and self.visualizer:
            fig, ax = self.visualizer.draw_graph("Graphe initial")
            
            # Intégrer la figure matplotlib dans tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Ajouter une barre d'outils pour naviguer dans le graphique
            toolbar = NavigationToolbar2Tk(canvas, self.graph_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def run_bfs(self):
        """Exécute l'algorithme Best-First Search et affiche les résultats."""
        if not self.graph:
            messagebox.showerror("Erreur", "Veuillez d'abord charger ou créer un graphe.")
            return
        
        try:
            # Exécuter l'algorithme
            bfs = BestFirstSearch(self.graph)
            path, expanded_nodes, steps = bfs.search()
            self.results = (path, expanded_nodes, steps)
            
            # Afficher le chemin trouvé
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            if path:
                fig, ax = self.visualizer.visualize_path(path, "Chemin trouvé par Best-First Search")
                
                # Intégrer la figure matplotlib dans tkinter
                canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # Ajouter une barre d'outils pour naviguer dans le graphique
                toolbar = NavigationToolbar2Tk(canvas, self.graph_frame)
                toolbar.update()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # Mise à jour des informations
                path_str = " -> ".join(path)
                expanded_str = " -> ".join(expanded_nodes)
                
                self.update_info(f"Chemin trouvé: {path_str}\n"
                              f"Nœuds explorés: {expanded_str}\n"
                              f"Longueur du chemin: {len(path)-1} arêtes")
            else:
                self.update_info("Aucun chemin trouvé de {} à {}".format(
                    self.graph.start_node, self.graph.goal_node))
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exécution de Best-First Search: {str(e)}")
    
    def save_results(self):
        """Sauvegarde les résultats dans un fichier."""
        if not self.results or not self.graph:
            messagebox.showerror("Erreur", "Aucun résultat à sauvegarder.")
            return
        
        try:
            path, expanded_nodes, steps = self.results
            
            # Demander le nom du fichier
            filename = filedialog.asksaveasfilename(
                title="Sauvegarder les résultats",
                defaultextension=".json",
                filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
            )
            
            if not filename:  # L'utilisateur a annulé
                return
            
            # Préparer les données à sauvegarder
            results_data = {
                "algorithm": "Best-First Search",
                "start_node": self.graph.start_node,
                "goal_node": self.graph.goal_node,
                "path": path if path else [],
                "expanded_nodes": expanded_nodes,
                "steps_count": len(steps)
            }
            
            # Sauvegarder au format JSON
            with open(filename, 'w') as file:
                json.dump(results_data, file, indent=4)
            
            # Sauvegarder aussi une image du graphe avec le chemin
            if path:
                image_filename = os.path.splitext(filename)[0] + ".png"
                fig, ax = self.visualizer.visualize_path(path)
                plt.savefig(image_filename, bbox_inches='tight')
                plt.close(fig)
                
                self.update_info(f"Résultats sauvegardés dans {filename}\n"
                              f"Image sauvegardée dans {image_filename}")
            else:
                self.update_info(f"Résultats sauvegardés dans {filename}")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde des résultats: {str(e)}")
    
    def create_animation(self):
        """Crée une animation de l'algorithme et la sauvegarde."""
        if not self.results or not self.graph:
            messagebox.showerror("Erreur", "Exécutez d'abord l'algorithme.")
            return
        
        try:
            path, expanded_nodes, steps = self.results
            
            # Demander le nom du fichier
            filename = filedialog.asksaveasfilename(
                title="Sauvegarder l'animation",
                defaultextension=".mp4",
                filetypes=[("Fichiers MP4", "*.mp4"), ("Tous les fichiers", "*.*")]
            )
            
            if not filename:  # L'utilisateur a annulé
                return
            
            # Demander l'intervalle entre les images
            interval = simpledialog.askinteger(
                "Intervalle", "Intervalle entre les images (ms):",
                initialvalue=1000, minvalue=100, maxvalue=5000
            )
            
            if not interval:  # L'utilisateur a annulé
                interval = 1000
            
            # Mettre à jour les informations
            self.update_info("Création de l'animation en cours...\nCela peut prendre un moment.")
            self.root.update()
            
            # Créer l'animation
            self.visualizer.animate_search(steps, path, interval=interval, 
                                         save_animation=True, filename=filename)
            
            self.update_info(f"Animation sauvegardée dans {filename}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création de l'animation: {str(e)}")


def main():
    root = tk.Tk()
    app = BestFirstSearchApp(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()