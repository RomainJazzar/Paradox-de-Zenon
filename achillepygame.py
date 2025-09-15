#!/usr/bin/env python3
"""
Version graphique avec Pygame du paradoxe d'Achille et la Tortue
"""

import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 1200
HAUTEUR = 600
FPS = 60

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
GRIS = (128, 128, 128)
JAUNE = (255, 255, 0)

class CourseAchilleTortue:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Paradoxe d'Achille et la Tortue - Zénon d'Élée")
        self.horloge = pygame.time.Clock()
        
        # Police pour le texte
        self.font = pygame.font.Font(None, 24)
        self.font_titre = pygame.font.Font(None, 36)
        
        # Paramètres de simulation
        self.reset_simulation()
        
        # Interface
        self.simulation_active = False
        self.vitesse_simulation = 1.0
        
    def reset_simulation(self):
        """Remet à zéro la simulation"""
        self.position_achille = 0.0
        self.position_tortue = 700.0  # 200 pixels d'avance
        self.vitesse_achille = 2.5    # 5 pixels par frame
        self.vitesse_tortue = 0.5     # 0.5 pixels par frame
        self.temps = 0.0
        self.historique_achille = []
        self.historique_tortue = []
        
    def dessiner_piste(self):
        """Dessine la piste de course"""
        # Ligne de course
        y_piste = HAUTEUR // 2
        pygame.draw.line(self.ecran, NOIR, (50, y_piste), (LARGEUR - 50, y_piste), 3)
        
        # Marqueurs de distance
        for i in range(0, LARGEUR - 100, 100):
            x = 50 + i
            pygame.draw.line(self.ecran, GRIS, (x, y_piste - 10), (x, y_piste + 10), 1)
            texte = self.font.render(f"{i}m", True, GRIS)
            self.ecran.blit(texte, (x - 10, y_piste + 15))
    
    def dessiner_coureurs(self):
        """Dessine Achille et la tortue"""
        y_piste = HAUTEUR // 2
        
        # Position d'Achille (rectangle rouge)
        x_achille = 50 + self.position_achille
        if x_achille < LARGEUR - 50:
            pygame.draw.rect(self.ecran, ROUGE, (x_achille - 10, y_piste - 20, 20, 15))
            texte_achille = self.font.render("Achille", True, ROUGE)
            self.ecran.blit(texte_achille, (x_achille - 25, y_piste - 45))
        
        # Position de la tortue (cercle vert)
        x_tortue = 50 + self.position_tortue
        if x_tortue < LARGEUR - 50:
            pygame.draw.circle(self.ecran, VERT, (int(x_tortue), y_piste - 10), 8)
            texte_tortue = self.font.render("Tortue", True, VERT)
            self.ecran.blit(texte_tortue, (x_tortue - 20, y_piste - 45))
    
    def dessiner_trajectoires(self):
        """Dessine les trajectoires historiques"""
        y_trajectoire_achille = 100
        y_trajectoire_tortue = 150
        
        # Trajectoire d'Achille
        if len(self.historique_achille) > 1:
            points_achille = [(50 + pos, y_trajectoire_achille) for pos in self.historique_achille]
            if len(points_achille) > 1:
                pygame.draw.lines(self.ecran, ROUGE, False, points_achille, 2)
        
        # Trajectoire de la tortue
        if len(self.historique_tortue) > 1:
            points_tortue = [(50 + pos, y_trajectoire_tortue) for pos in self.historique_tortue]
            if len(points_tortue) > 1:
                pygame.draw.lines(self.ecran, VERT, False, points_tortue, 2)
    
    def dessiner_info(self):
        """Dessine les informations de la simulation"""
        y_info = 2500
        
        # Titre
        titre = self.font_titre.render("Paradoxe d'Achille et la Tortue", True, NOIR)
        self.ecran.blit(titre, (10, 10))
        
        # Informations actuelles
        infos = [
            f"Temps: {self.temps:.2f}s",
            f"Position Achille: {self.position_achille:.2f}m",
            f"Position Tortue: {self.position_tortue:.2f}m",
            f"Distance entre eux: {abs(self.position_tortue - self.position_achille):.2f}m",
            f"Vitesse Achille: {self.vitesse_achille:.1f} m/s",
            f"Vitesse Tortue: {self.vitesse_tortue:.1f} m/s",
        ]
        
        for i, info in enumerate(infos):
            texte = self.font.render(info, True, NOIR)
            self.ecran.blit(texte, (10, y_info + i * 25))
        
        # État de la simulation
        if self.position_achille >= self.position_tortue:
            victoire = self.font.render("🏃‍♂️ Achille a dépassé la tortue!", True, ROUGE)
            self.ecran.blit(victoire, (10, y_info + len(infos) * 25 + 10))
        
        # Contrôles
        controles = [
            "CONTRÔLES:",
            "ESPACE: Start/Pause",
            "R: Reset",
            "↑/↓: Vitesse simulation",
            "Q: Quitter"
        ]
        
        for i, controle in enumerate(controles):
            couleur = BLEU if i == 0 else GRIS
            texte = self.font.render(controle, True, couleur)
            self.ecran.blit(texte, (10, HAUTEUR - 130 + i * 20))
    
    def mettre_a_jour_simulation(self):
        """Met à jour la simulation"""
        if self.simulation_active and self.position_achille < self.position_tortue:
            # Mise à jour des positions
            self.position_achille += self.vitesse_achille * self.vitesse_simulation
            self.position_tortue += self.vitesse_tortue * self.vitesse_simulation
            self.temps += 0.016 * self.vitesse_simulation  # ~60 FPS
            
            # Enregistrement de l'historique
            if len(self.historique_achille) == 0 or len(self.historique_achille) % 5 == 0:
                self.historique_achille.append(self.position_achille)
                self.historique_tortue.append(self.position_tortue)
    
    def gerer_evenements(self):
        """Gère les événements utilisateur"""
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return False
            
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_SPACE:
                    self.simulation_active = not self.simulation_active
                
                elif evenement.key == pygame.K_r:
                    self.reset_simulation()
                    self.simulation_active = False
                
                elif evenement.key == pygame.K_UP:
                    self.vitesse_simulation = min(5.0, self.vitesse_simulation + 0.5)
                
                elif evenement.key == pygame.K_DOWN:
                    self.vitesse_simulation = max(0.1, self.vitesse_simulation - 0.5)
                
                elif evenement.key == pygame.K_q:
                    return False
        
        return True
    
    def executer(self):
        """Boucle principale du programme"""
        en_cours = True
        
        while en_cours:
            en_cours = self.gerer_evenements()
            
            # Mise à jour
            self.mettre_a_jour_simulation()
            
            # Rendu
            self.ecran.fill(BLANC)
            self.dessiner_piste()
            self.dessiner_trajectoires()
            self.dessiner_coureurs()
            self.dessiner_info()
            
            pygame.display.flip()
            self.horloge.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jeu = CourseAchilleTortue()
    jeu.executer()