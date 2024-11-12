import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
large=('Helvetica',18)

# Fonction pour définir l'équation différentielle
def dU_dt(U, t, alpha, beta, F):
    return -alpha * U + beta * F


def logistic_growth(S, r, K):
    return r * S * (1 - S / K)

def runge_kutta(S0, r, K, dt, t_max):
    
    n_steps = int(t_max / dt)
    t_values = np.linspace(0, t_max, n_steps)
    S_values = np.zeros(n_steps)

    # condition initale
    S_values[0] = S0

    # Boucle sur chaque pas de temps 
    for i in range(1, n_steps):
        t = t_values[i-1]
        S = S_values[i-1]

        k1 = dt * logistic_growth(S, r, K)
        k2 = dt * logistic_growth(S + 0.5 * k1, r, K)
        k3 = dt * logistic_growth(S + 0.5 * k2, r, K)
        k4 = dt * logistic_growth(S + k3, r, K)

        # calcul de la nouvelle valeur de S
        S_values[i] = S + (k1 + 2*k2 + 2*k3 + k4) / 6.0


    return t_values, S_values


def submit():
    global r, k, SO, t_max, dt
    try:
        r = float(entry_r.get())
        k = float(entry_k.get())
        SO = float(entry_SO.get())
        t_max = float(entry_tmax.get())
        dt = float(entry_dt.get())

        result = f"r : {r} , k : {k}, dt : {dt}, so : {SO}, t_max : {t_max}"
        # messagebox.showinfo("Valeurs saisie", result)
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques")

        
def use_valus():
    global r, k, SO, t_max, dt
    try:
        result = f"r : {r} , k : {k}, dt : {dt}, so : {SO}, t_max : {t_max}"
        print(f"r : {r} , k : {k}, dt : {dt}, so : {SO}, t_max : {t_max}")
        messagebox.showinfo("utilisation des variagle globale", result)
    except NameError:
        messagebox.showerror("erreur", "Les variables ne sont pas encore definie")    

# Fonction pour afficher ou mettre à jour le graphique
def show_graph():


    
    # parametre de l'entreprise
    # r = 0.05 # Taux de croissance
    # K = 1000.0 # taille maximale de l'entreprise
    # SO = 50.0 # taille  initales de l'entreprise
    # dt = 0.1 # Pas de temps
    # t_max = 100 # temps total

    # parametre avec entrer Manuelle par l'utilisateur
    r = float(entry_r.get())
    k = float(entry_k.get())
    SO = float(entry_SO.get())
    t_max = float(entry_tmax.get())
    dt = float(entry_dt.get())

    t_values, S_values = runge_kutta(SO, r, k, dt, t_max)


    if 'canvas' not in globals():
        # Créer la figure et les axes pour le graphique
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
        ax.plot(t_values, S_values, label="État de l'unité (U(t))")
        # ax.axhline(y=U_crit, color='r', linestyle='--', label="Seuil critique U_crit")
        ax.set_xlabel('Temps t')
        ax.set_ylabel("Taille de l'entreprise")
        ax.set_title("Modele de croissance Logistique d'une entreprise")
        ax.legend()
        ax.grid(True)
        plt.show()

        global canvas
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    else:
        # Mettre à jour le graphique existant
        ax = canvas.figure.axes[0]  
        ax.clear()  
        ax.plot(t_values, S_values, label="État de l'unité (U(t))")
        ax.set_xlabel('Temps t')
        ax.set_ylabel("Taille de l'entreprise")
        ax.set_title("Modele de croissance Logistique d'une entreprise")
        ax.legend()
        ax.grid(True)
        canvas.draw()  # Redessiner le graphique

    
window = tk.Tk()
window.title("Parametre de la croissance Logistique d'une entreprise")
window.bind("<F11>", lambda event: window.attributes('-fullscreen', not window.attributes('-fullscreen')))


window.geometry("360x300")

tk.Label(window, text="Taux de croissance (r)").grid(row=0, column=0, padx=10, pady=5)
entry_r = tk.Entry(window)
entry_r.grid(row=0, column=1, padx=10, pady=5)


tk.Label(window, text="Capaciter de charge (k)").grid(row=1, column=0, padx=10, pady=5)
entry_k = tk.Entry(window)
entry_k.grid(row=1, column=1, padx=10, pady=5)


tk.Label(window, text="Population initiale (SO)").grid(row=2, column=0, padx=10, pady=5)
entry_SO = tk.Entry(window)
entry_SO.grid(row=2, column=1, padx=10, pady=5)


tk.Label(window, text="Temps maximal (t_max)").grid(row=3, column=0, padx=10, pady=5)
entry_tmax = tk.Entry(window)
entry_tmax.grid(row=3, column=1, padx=10, pady=5)



tk.Label(window, text="Intervalle de temps (dt)").grid(row=4, column=0, padx=10, pady=5)
entry_dt = tk.Entry(window)
entry_dt.grid(row=4, column=1, padx=10, pady=5)


submit_button = tk.Button(window, text="Valider", command=show_graph)
submit_button.grid(row=5, columnspan=2, pady=10)

def on_closing():
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
