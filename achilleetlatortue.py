#!/usr/bin/env python3
"""
Simulation du paradoxe d'Achille et la Tortue de Zénon d'Élée
"""

import time

def simulation_achille_tortue():
    """
    Simule la course entre Achille et la tortue.
    Achille court 10 fois plus vite que la tortue, mais la tortue a 100m d'avance.
    """
    
    # Paramètres initiaux
    position_achille = 0.0  # Position de départ d'Achille (en mètres)
    position_tortue = 100.0  # La tortue a 100m d'avance
    vitesse_achille = 10.0   # Achille court à 10 m/s
    vitesse_tortue = 1.0     # La tortue avance à 1 m/s
    
    temps = 0.0
    dt = 1.0  # Intervalle de temps (1 seconde)
    iteration = 0
    
    print("=== PARADOXE D'ACHILLE ET LA TORTUE ===")
    print(f"Achille (vitesse: {vitesse_achille} m/s) vs Tortue (vitesse: {vitesse_tortue} m/s)")
    print(f"La tortue a {position_tortue}m d'avance\n")
    
    print(f"{'Temps':>6} | {'Achille':>8} | {'Tortue':>8} | {'Distance':>9}")
    print("-" * 45)
    
    # Simulation jusqu'à ce qu'Achille dépasse la tortue
    while position_achille < position_tortue and iteration < 200:
        # Affichage des positions actuelles
        distance_entre_eux = position_tortue - position_achille
        print(f"{temps:6.1f} | {position_achille:8.2f} | {position_tortue:8.2f} | {distance_entre_eux:9.2f}")
        
        # Mise à jour des positions
        position_achille += vitesse_achille * dt
        position_tortue += vitesse_tortue * dt
        temps += dt
        iteration += 1
        
        # Petite pause pour la lisibilité
        time.sleep(0.1)
    
    print("-" * 45)
    if position_achille >= position_tortue:
        print(f"🏃‍♂️ Achille dépasse la tortue après {temps:.1f} secondes!")
        print(f"Position finale d'Achille: {position_achille:.2f}m")
        print(f"Position finale de la tortue: {position_tortue:.2f}m")
    else:
        print("Simulation interrompue après 200 itérations")

def analyse_mathematique():
    """
    Analyse mathématique théorique du paradoxe
    """
    print("\n=== ANALYSE MATHÉMATIQUE ===")
    print("Résolution par équation:")
    print("Achille rattrape la tortue quand: 10t = 100 + 1t")
    print("Donc: 9t = 100")
    print("t = 100/9 ≈ 11.11 secondes")
    print("Position de rencontre: 10 × 11.11 ≈ 111.11 mètres")
    
    # Vérification par série infinie (approche de Zénon)
    print("\n=== APPROCHE DE ZÉNON (SÉRIE INFINIE) ===")
    temps_total = 0
    distance_parcourue = 0
    
    for i in range(10):  # Première dizaine de termes
        if i == 0:
            # Temps pour qu'Achille atteigne la position initiale de la tortue
            temps_etape = 100 / 10  # 100m à 10 m/s
            distance_tortue = temps_etape * 1  # distance parcourue par la tortue
        else:
            # Temps pour rattraper la nouvelle avance
            temps_etape = distance_tortue / 10
            distance_tortue = temps_etape * 1
        
        temps_total += temps_etape
        distance_parcourue += temps_etape * 10
        
        print(f"Étape {i+1}: +{temps_etape:.3f}s, total: {temps_total:.3f}s, position: {distance_parcourue:.3f}m")

if __name__ == "__main__":
    simulation_achille_tortue()
    analyse_mathematique()