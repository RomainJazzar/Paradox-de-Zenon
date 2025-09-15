#!/usr/bin/env python3
"""
Simulation du paradoxe de la dichotomie de Zénon d'Élée
"""

import time
import math

def simulation_dichotomie():
    """
    Simule le lancement de la pierre vers l'arbre.
    La pierre doit parcourir la moitié de la distance restante à chaque étape.
    """
    
    # Paramètres initiaux
    distance_totale = 8.0  # Distance jusqu'à l'arbre (8 mètres)
    position_pierre = 0.0  # Position de départ de la pierre
    position_arbre = distance_totale
    
    print("=== PARADOXE DE LA DICHOTOMIE ===")
    print(f"Distance jusqu'à l'arbre: {distance_totale}m")
    print("La pierre doit parcourir la moitié de la distance restante à chaque étape\n")
    
    print(f"{'Étape':>5} | {'Position':>10} | {'Distance':>10} | {'Moitié':>10}")
    print("-" * 50)
    
    etape = 0
    seuil_precision = 0.001  # Arrêt quand la distance devient très petite
    
    while True:
        distance_restante = position_arbre - position_pierre
        
        # Affichage de l'état actuel
        moitie_distance = distance_restante / 2
        print(f"{etape:5d} | {position_pierre:10.6f} | {distance_restante:10.6f} | {moitie_distance:10.6f}")
        
        # Condition d'arrêt (quand la distance devient négligeable)
        if distance_restante < seuil_precision:
            print(f"\nLa pierre est suffisamment proche de l'arbre (< {seuil_precision}m)")
            break
        
        if etape > 50:  # Limite de sécurité
            print("\nSimulation interrompue après 50 étapes")
            break
        
        # La pierre avance de la moitié de la distance restante
        position_pierre += moitie_distance
        etape += 1
        
        time.sleep(0.2)  # Pause pour la lisibilité
    
    print(f"\nPosition finale de la pierre: {position_pierre:.6f}m")
    print(f"Distance finale à l'arbre: {position_arbre - position_pierre:.6f}m")

def analyse_serie_geometrique():
    """
    Analyse mathématique de la série géométrique
    """
    print("\n=== ANALYSE MATHÉMATIQUE ===")
    print("Série géométrique: 4 + 2 + 1 + 0.5 + 0.25 + ...")
    print("Formule: S = a / (1 - r) où a = 4 et r = 1/2")
    print("S = 4 / (1 - 0.5) = 4 / 0.5 = 8")
    print("La série converge vers 8, donc la pierre atteint bien l'arbre!")
    
    # Démonstration numérique
    print("\n=== DÉMONSTRATION NUMÉRIQUE ===")
    somme_partielle = 0
    terme = 4.0  # Premier terme: moitié de 8
    
    for i in range(15):
        somme_partielle += terme
        print(f"Terme {i+1}: {terme:.6f}, Somme: {somme_partielle:.6f}, Reste: {8 - somme_partielle:.6f}")
        terme = terme / 2

def visualisation_convergence():
    """
    Visualise la convergence de la série
    """
    print("\n=== VISUALISATION DE LA CONVERGENCE ===")
    distances = []
    distance = 8.0
    
    for i in range(20):
        distances.append(distance)
        distance = distance / 2
    
    # Graphique ASCII simple
    for i, dist in enumerate(distances[:10]):
        barre_length = int(dist * 5)  # Échelle pour l'affichage
        barre = "█" * barre_length
        print(f"Étape {i:2d}: {dist:8.4f}m |{barre}")

if __name__ == "__main__":
    simulation_dichotomie()
    analyse_serie_geometrique()
    visualisation_convergence()