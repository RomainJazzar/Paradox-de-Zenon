#!/usr/bin/env python3
"""
Simulation du paradoxe de la flèche en vol de Zénon d'Élée
"""

import time
import math

def simulation_fleche():
    """
    Simule le vol de la flèche en analysant chaque instant.
    Paradoxe: à chaque instant, la flèche est immobile, donc le mouvement est impossible.
    """
    
    # Paramètres initiaux
    position_initiale = 0.0  # Position de départ de la flèche
    position_cible = 50.0    # Position de la cible (50 mètres)
    vitesse_fleche = 25.0    # Vitesse de la flèche (25 m/s)
    
    # Intervalles de temps de plus en plus petits
    intervalles = [1.0, 0.5, 0.1, 0.01, 0.001, 0.0001]
    
    print("=== PARADOXE DE LA FLÈCHE EN VOL ===")
    print(f"Distance jusqu'à la cible: {position_cible}m")
    print(f"Vitesse de la flèche: {vitesse_fleche} m/s")
    print("Analysons le mouvement avec des intervalles de temps décroissants\n")
    
    for dt in intervalles:
        print(f"\n--- ANALYSE AVEC Δt = {dt} seconde(s) ---")
        print(f"{'Instant':>8} | {'Position':>10} | {'Déplacement':>12} | {'Vitesse Moy':>12}")
        print("-" * 55)
        
        position = position_initiale
        temps = 0.0
        instant = 0
        
        while position < position_cible and instant < 20:
            # Calcul du déplacement pendant cet intervalle
            deplacement = vitesse_fleche * dt
            vitesse_moyenne = deplacement / dt if dt > 0 else 0
            
            print(f"{temps:8.4f} | {position:10.4f} | {deplacement:12.6f} | {vitesse_moyenne:12.2f}")
            
            # Mise à jour pour l'instant suivant
            position += deplacement
            temps += dt
            instant += 1
            
            if dt >= 0.1:
                time.sleep(0.1)  # Pause seulement pour les gros intervalles
        
        temps_theorique = position_cible / vitesse_fleche
        print(f"\nTemps théorique pour atteindre la cible: {temps_theorique:.4f}s")
        print(f"Temps simulé: {temps:.4f}s")

def analyse_paradoxe():
    """
    Analyse philosophique et mathématique du paradoxe
    """
    print("\n" + "="*60)
    print("=== ANALYSE DU PARADOXE ===")
    print("="*60)
    
    print("\n1. ARGUMENT DE ZÉNON:")
    print("   • À chaque instant t, la flèche occupe une position précise")
    print("   • Si l'instant est infiniment court, aucun mouvement n'est possible")
    print("   • Donc, à chaque instant, la flèche est au repos")
    print("   • Le temps étant une succession d'instants, la flèche est toujours au repos")
    
    print("\n2. RÉSOLUTION MODERNE:")
    print("   • Le mouvement est défini par une fonction position f(t)")
    print("   • La vitesse instantanée est la dérivée: v = df/dt")
    print("   • Même si la position est fixe à un instant donné,")
    print("     la dérivée peut être non-nulle")
    
    print("\n3. DÉMONSTRATION MATHÉMATIQUE:")
    print("   Position: x(t) = x₀ + v₀·t")
    print("   Vitesse:  v(t) = dx/dt = v₀")
    print("   La vitesse instantanée existe et est constante!")

def simulation_calcul_differentiel():
    """
    Démontre le concept de vitesse instantanée avec le calcul différentiel
    """
    print("\n=== VITESSE INSTANTANÉE PAR CALCUL DIFFÉRENTIEL ===")
    
    # Fonction position: x(t) = 25t (pour une vitesse de 25 m/s)
    def position(t):
        return 25 * t
    
    # Calcul de la vitesse instantanée en approximant la dérivée
    t_fixe = 1.0  # Instant où nous calculons la vitesse
    deltas = [1.0, 0.1, 0.01, 0.001, 0.0001, 0.00001]
    
    print(f"\nCalcul de la vitesse instantanée à t = {t_fixe}s:")
    print(f"{'Δt':>10} | {'Δx':>10} | {'Δx/Δt':>10} | {'Limite':>10}")
    print("-" * 45)
    
    for delta_t in deltas:
        x1 = position(t_fixe)
        x2 = position(t_fixe + delta_t)
        delta_x = x2 - x1
        vitesse_approx = delta_x / delta_t
        
        print(f"{delta_t:10.5f} | {delta_x:10.5f} | {vitesse_approx:10.3f} | {'→ 25.000':>10}")
    
    print("\nConclusion: Quand Δt → 0, Δx/Δt → 25 m/s")
    print("La vitesse instantanée existe et vaut 25 m/s!")

if __name__ == "__main__":
    simulation_fleche()
    analyse_paradoxe()
    simulation_calcul_differentiel()