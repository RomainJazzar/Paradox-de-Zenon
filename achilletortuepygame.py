#!/usr/bin/env python3
"""
Version graphique avec Pygame du paradoxe d'Achille et la Tortue
Simulation interactive avec visualisation en temps réel
"""

import pygame
import sys
import math
import random

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 1400
HAUTEUR = 800
FPS = 60

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
GRIS = (128, 128, 128)
GRIS_CLAIR = (200, 200, 200)
JAUNE = (255, 255, 0)
ORANGE = (255, 165, 0)
VIOLET = (128, 0, 128)

class CourseAchilleTortue:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("🏃‍♂️ Paradoxe d'Achille et la Tortue - Zénon d'Élée")
        self.horloge = pygame.time.Clock()
        
        # Polices
        self.font_petit = pygame.font.Font(None, 20)
        self.font = pygame.font.Font(None, 24)
        self.font_titre = pygame.font.Font(None, 36)
        self.font_grand = pygame.font.Font(None, 48)
        
        # Paramètres de simulation
        self.reset_simulation()
        
        # Interface
        self.simulation_active = False
        self.vitesse_simulation = 1.0
        self.mode_affichage = "normal"  # "normal", "zenon", "mathematique"
        self.afficher_trajectoires = True
        self.afficher_graphique = True
        
        # Animation
        self.particules = []
        self.etape_zenon = 0
        self.temps_etape_zenon = 0.0
        
    def reset_simulation(self):
        """Remet à zéro la simulation"""
        self.position_achille = 0.0
        self.position_tortue = 300.0  # 300 pixels d'avance
        self.vitesse_achille = 100.0   # 100 pixels par seconde
        self.vitesse_tortue = 10.0     # 10 pixels par seconde
        self.temps = 0.0
        self.historique_achille = []
        self.historique_tortue = []
        self.historique_temps = []
        self.course_terminee = False
        self.particules = []
        self.etape_zenon = 0
        self.temps_etape_zenon = 0.0
        
    def ajouter_particule(self, x, y, couleur):
        """Ajoute une particule d'effet visuel"""
        for i in range(5):
            particule = {
                'x': x + random.uniform(-10, 10),
                'y': y + random.uniform(-10, 10),
                'vx': random.uniform(-50, 50),
                'vy': random.uniform(-50, 50),
                'vie': 1.0,
                'couleur': couleur
            }
            self.particules.append(particule)
    
    def mettre_a_jour_particules(self, dt):
        """Met à jour les particules d'effet"""
        for particule in self.particules[:]:
            particule['x'] += particule['vx'] * dt
            particule['y'] += particule['vy'] * dt
            particule['vie'] -= dt * 2
            if particule['vie'] <= 0:
                self.particules.remove(particule)
    
    def dessiner_particules(self):
        """Dessine les particules d'effet"""
        for particule in self.particules:
            alpha = int(particule['vie'] * 255)
            couleur = particule['couleur']
            rayon = int(particule['vie'] * 3)
            if rayon > 0:
                pygame.draw.circle(self.ecran, couleur, 
                                 (int(particule['x']), int(particule['y'])), rayon)
    
    def dessiner_piste(self):
        """Dessine la piste de course avec décorations"""
        y_piste = HAUTEUR // 2
        
        # Fond de piste
        pygame.draw.rect(self.ecran, GRIS_CLAIR, (50, y_piste - 30, LARGEUR - 100, 60))
        
        # Ligne centrale
        pygame.draw.line(self.ecran, NOIR, (50, y_piste), (LARGEUR - 50, y_piste), 3)
        
        # Lignes de délimitation
        pygame.draw.line(self.ecran, NOIR, (50, y_piste - 30), (LARGEUR - 50, y_piste - 30), 2)
        pygame.draw.line(self.ecran, NOIR, (50, y_piste + 30), (LARGEUR - 50, y_piste + 30), 2)
        
        # Marqueurs de distance tous les 100 pixels
        for i in range(0, LARGEUR - 100, 100):
            x = 50 + i
            pygame.draw.line(self.ecran, GRIS, (x, y_piste - 35), (x, y_piste + 35), 2)
            distance_m = i // 10  # Conversion pixels vers mètres (1m = 10px)
            texte = self.font_petit.render(f"{distance_m}m", True, GRIS)
            self.ecran.blit(texte, (x - 10, y_piste + 40))
        
        # Ligne d'arrivée (si Achille a rattrapé)
        if self.position_achille >= self.position_tortue:
            x_arrivee = 50 + self.position_achille
            pygame.draw.line(self.ecran, ROUGE, (x_arrivee, y_piste - 40), (x_arrivee, y_piste + 40), 3)
            texte_arrivee = self.font.render("ARRIVÉE!", True, ROUGE)
            self.ecran.blit(texte_arrivee, (x_arrivee - 30, y_piste - 60))
    
    def dessiner_coureurs(self):
        """Dessine Achille et la tortue avec animations"""
        y_piste = HAUTEUR // 2
        
        # Position d'Achille (héros grec stylisé)
        x_achille = 50 + self.position_achille
        if x_achille < LARGEUR - 50:
            # Corps d'Achille (rectangle rouge avec casque)
            pygame.draw.rect(self.ecran, ROUGE, (x_achille - 15, y_piste - 25, 30, 20))
            # Casque (cercle doré)
            pygame.draw.circle(self.ecran, JAUNE, (int(x_achille), y_piste - 30), 8)
            # Jambes en mouvement (simulation)
            jambe_offset = int(math.sin(self.temps * 10) * 3)
            pygame.draw.line(self.ecran, ROUGE, (x_achille - 5, y_piste - 5), 
                           (x_achille - 5 + jambe_offset, y_piste + 10), 3)
            pygame.draw.line(self.ecran, ROUGE, (x_achille + 5, y_piste - 5), 
                           (x_achille + 5 - jambe_offset, y_piste + 10), 3)
            
            # Nom et vitesse
            texte_achille = self.font.render(f"Achille", True, ROUGE)
            vitesse_achille = self.font_petit.render(f"{self.vitesse_achille:.1f} px/s", True, ROUGE)
            self.ecran.blit(texte_achille, (x_achille - 30, y_piste - 55))
            self.ecran.blit(vitesse_achille, (x_achille - 35, y_piste - 75))
        
        # Position de la tortue (tortue verte avec détails)
        x_tortue = 50 + self.position_tortue
        if x_tortue < LARGEUR - 50:
            # Corps de la tortue (ovale vert)
            pygame.draw.ellipse(self.ecran, VERT, (x_tortue - 12, y_piste - 15, 24, 18))
            # Tête (petit cercle)
            tete_x = x_tortue + 10 + int(math.sin(self.temps * 2) * 2)
            pygame.draw.circle(self.ecran, VERT, (tete_x, y_piste - 8), 4)
            # Pattes (petites lignes)
            for i, offset_x in enumerate([-8, -3, 3, 8]):
                patte_y = y_piste + 2 + int(math.sin(self.temps * 3 + i) * 1)
                pygame.draw.line(self.ecran, VERT, (x_tortue + offset_x, y_piste), 
                               (x_tortue + offset_x, patte_y), 2)
            
            # Nom et vitesse
            texte_tortue = self.font.render("Tortue", True, VERT)
            vitesse_tortue = self.font_petit.render(f"{self.vitesse_tortue:.1f} px/s", True, VERT)
            self.ecran.blit(texte_tortue, (x_tortue - 25, y_piste - 55))
            self.ecran.blit(vitesse_tortue, (x_tortue - 30, y_piste - 75))
    
    def dessiner_trajectoires(self):
        """Dessine les trajectoires historiques"""
        if not self.afficher_trajectoires or len(self.historique_achille) < 2:
            return
        
        y_traj_achille = 150
        y_traj_tortue = 200
        
        # Trajectoire d'Achille (rouge)
        points_achille = [(50 + pos, y_traj_achille) for pos in self.historique_achille]
        if len(points_achille) > 1:
            pygame.draw.lines(self.ecran, ROUGE, False, points_achille, 2)
        
        # Trajectoire de la tortue (verte)
        points_tortue = [(50 + pos, y_traj_tortue) for pos in self.historique_tortue]
        if len(points_tortue) > 1:
            pygame.draw.lines(self.ecran, VERT, False, points_tortue, 2)
        
        # Légendes
        pygame.draw.line(self.ecran, ROUGE, (60, y_traj_achille), (90, y_traj_achille), 3)
        texte = self.font_petit.render("Trajectoire Achille", True, ROUGE)
        self.ecran.blit(texte, (95, y_traj_achille - 8))
        
        pygame.draw.line(self.ecran, VERT, (60, y_traj_tortue), (90, y_traj_tortue), 3)
        texte = self.font_petit.render("Trajectoire Tortue", True, VERT)
        self.ecran.blit(texte, (95, y_traj_tortue - 8))
    
    def dessiner_graphique_distance(self):
        """Dessine un graphique de l'évolution de la distance"""
        if not self.afficher_graphique or len(self.historique_temps) < 2:
            return
        
        # Zone du graphique
        graph_x, graph_y = LARGEUR - 350, 100
        graph_w, graph_h = 300, 200
        
        pygame.draw.rect(self.ecran, BLANC, (graph_x, graph_y, graph_w, graph_h))
        pygame.draw.rect(self.ecran, NOIR, (graph_x, graph_y, graph_w, graph_h), 2)
        
        # Titre
        titre = self.font.render("Distance entre Achille et la Tortue", True, NOIR)
        self.ecran.blit(titre, (graph_x + 20, graph_y - 25))
        
        # Données
        if len(self.historique_achille) > 1:
            distances = [abs(self.historique_tortue[i] - self.historique_achille[i]) 
                        for i in range(len(self.historique_achille))]
            
            max_distance = max(distances) if distances else 1
            max_temps = max(self.historique_temps) if self.historique_temps else 1
            
            # Points du graphique
            points = []
            for i, (temps, distance) in enumerate(zip(self.historique_temps, distances)):
                x = graph_x + (temps / max_temps) * (graph_w - 20)
                y = graph_y + graph_h - 20 - (distance / max_distance) * (graph_h - 40)
                points.append((x, y))
            
            # Ligne du graphique
            if len(points) > 1:
                pygame.draw.lines(self.ecran, BLEU, False, points, 2)
            
            # Axes
            pygame.draw.line(self.ecran, NOIR, (graph_x + 10, graph_y + graph_h - 10), 
                           (graph_x + graph_w - 10, graph_y + graph_h - 10), 1)
            pygame.draw.line(self.ecran, NOIR, (graph_x + 10, graph_y + 10), 
                           (graph_x + 10, graph_y + graph_h - 10), 1)
            
            # Étiquettes
            texte_x = self.font_petit.render("Temps (s)", True, NOIR)
            self.ecran.blit(texte_x, (graph_x + graph_w//2 - 30, graph_y + graph_h + 5))
            
            texte_y = self.font_petit.render("Distance", True, NOIR)
            self.ecran.blit(texte_y, (graph_x - 50, graph_y + graph_h//2))
    
    def dessiner_analyse_zenon(self):
        """Dessine l'analyse selon l'approche de Zénon"""
        if self.mode_affichage != "zenon":
            return
        
        y_start = 500
        
        # Titre de l'analyse
        titre = self.font_titre.render("Analyse de Zénon : Étapes de Rattrapage", True, VIOLET)
        self.ecran.blit(titre, (50, y_start))
        
        # Calcul des étapes de Zénon
        avance_actuelle = self.position_tortue - self.position_achille if self.position_achille < self.position_tortue else 0
        
        if avance_actuelle > 0:
            temps_rattrapage = avance_actuelle / self.vitesse_achille
            nouvelle_avance = temps_rattrapage * self.vitesse_tortue
            
            infos_zenon = [
                f"Étape {self.etape_zenon + 1}:",
                f"Avance actuelle: {avance_actuelle:.2f} pixels",
                f"Temps pour rattraper: {temps_rattrapage:.4f}s",
                f"Nouvelle avance tortue: {nouvelle_avance:.2f} pixels",
                f"Ratio de réduction: {nouvelle_avance/avance_actuelle:.4f}" if avance_actuelle > 0 else ""
            ]
            
            for i, info in enumerate(infos_zenon):
                if info:
                    texte = self.font.render(info, True, VIOLET)
                    self.ecran.blit(texte, (50, y_start + 40 + i * 25))
    
    def dessiner_info(self):
        """Dessine les informations de la simulation"""
        y_info = 50
        
        # Titre principal
        titre = self.font_grand.render("🏃‍♂️ Paradoxe d'Achille et la Tortue", True, NOIR)
        self.ecran.blit(titre, (50, 10))
        
        # Informations actuelles
        infos_gauche = [
            f"⏱️  Temps: {self.temps:.3f}s",
            f"🏃 Position Achille: {self.position_achille:.1f}px ({self.position_achille/10:.1f}m)",
            f"🐢 Position Tortue: {self.position_tortue:.1f}px ({self.position_tortue/10:.1f}m)",
            f"📏 Distance entre eux: {abs(self.position_tortue - self.position_achille):.1f}px",
            f"🎯 Vitesse simulation: {self.vitesse_simulation:.1f}x"
        ]
        
        for i, info in enumerate(infos_gauche):
            texte = self.font.render(info, True, NOIR)
            self.ecran.blit(texte, (50, y_info + i * 25))
        
        # Calculs mathématiques
        infos_droite = [
            "📊 Calculs Théoriques:",
            f"Temps de rattrapage: {300/(self.vitesse_achille - self.vitesse_tortue):.3f}s",
            f"Position de croisement: {300 * self.vitesse_achille/(self.vitesse_achille - self.vitesse_tortue):.1f}px",
            f"Avance initiale: 300px (30m)",
            f"Différence de vitesse: {self.vitesse_achille - self.vitesse_tortue:.1f}px/s"
        ]
        
        for i, info in enumerate(infos_droite):
            couleur = BLEU if i == 0 else NOIR
            texte = self.font.render(info, True, couleur)
            self.ecran.blit(texte, (700, y_info + i * 25))
        
        # État de la course
        if self.position_achille >= self.position_tortue and not self.course_terminee:
            victoire = self.font_titre.render("🏆 Achille a dépassé la tortue !", True, ROUGE)
            self.ecran.blit(victoire, (50, y_info + len(infos_gauche) * 25 + 20))
            self.course_terminee = True
        
        # Contrôles
        y_controles = HAUTEUR - 180
        controles = [
            "🎮 CONTRÔLES:",
            "ESPACE: ▶️ Start/Pause    R: 🔄 Reset    M: 📊 Mode d'affichage",
            "↑/↓: ⚡ Vitesse simulation    T: 📈 Trajectoires    G: 📊 Graphique",
            "1,2,3: 🎛️ Paramètres prédéfinis    Q: ❌ Quitter"
        ]
        
        for i, controle in enumerate(controles):
            couleur = BLEU if i == 0 else GRIS
            font_utilise = self.font if i == 0 else self.font_petit
            texte = font_utilise.render(controle, True, couleur)
            self.ecran.blit(texte, (50, y_controles + i * 25))
        
        # Mode actuel
        mode_texte = f"Mode: {self.mode_affichage.title()}"
        texte_mode = self.font.render(mode_texte, True, VIOLET)
        self.ecran.blit(texte_mode, (LARGEUR - 200, y_controles))
    
    def mettre_a_jour_simulation(self):
        """Met à jour la simulation"""
        if not self.simulation_active:
            return
        
        dt = 1/60 * self.vitesse_simulation  # Delta temps
        
        if self.position_achille < self.position_tortue:
            # Mise à jour des positions
            self.position_achille += self.vitesse_achille * dt
            self.position_tortue += self.vitesse_tortue * dt
            self.temps += dt
            
            # Enregistrement de l'historique
            if len(self.historique_achille) == 0 or self.temps - self.historique_temps[-1] >= 0.1:
                self.historique_achille.append(self.position_achille)
                self.historique_tortue.append(self.position_tortue)
                self.historique_temps.append(self.temps)
            
            # Effets spéciaux quand Achille se rapproche
            if abs(self.position_tortue - self.position_achille) < 50:
                if random.random() < 0.1:  # 10% de chance
                    self.ajouter_particule(50 + self.position_achille, HAUTEUR//2, ROUGE)
                    self.ajouter_particule(50 + self.position_tortue, HAUTEUR//2, VERT)
        
        # Mise à jour des particules
        self.mettre_a_jour_particules(dt)
        
        # Mise à jour de l'analyse de Zénon
        if self.mode_affichage == "zenon":
            self.temps_etape_zenon += dt
            if self.temps_etape_zenon > 1.0:  # Nouvelle étape chaque seconde
                self.etape_zenon += 1
                self.temps_etape_zenon = 0.0
    
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
                
                elif evenement.key == pygame.K_m:
                    modes = ["normal", "zenon", "mathematique"]
                    current_index = modes.index(self.mode_affichage)
                    self.mode_affichage = modes[(current_index + 1) % len(modes)]
                
                elif evenement.key == pygame.K_t:
                    self.afficher_trajectoires = not self.afficher_trajectoires
                
                elif evenement.key == pygame.K_g:
                    self.afficher_graphique = not self.afficher_graphique
                
                elif evenement.key == pygame.K_1:
                    # Paramètres classiques
                    self.vitesse_achille = 100.0
                    self.vitesse_tortue = 10.0
                
                elif evenement.key == pygame.K_2:
                    # Course serrée
                    self.vitesse_achille = 50.0
                    self.vitesse_tortue = 45.0
                
                elif evenement.key == pygame.K_3:
                    # Achille très rapide
                    self.vitesse_achille = 200.0
                    self.vitesse_tortue = 5.0
                
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
            
            if self.afficher_trajectoires:
                self.dessiner_trajectoires()
            
            if self.afficher_graphique:
                self.dessiner_graphique_distance()
            
            self.dessiner_coureurs()
            self.dessiner_particules()
            self.dessiner_analyse_zenon()
            self.dessiner_info()
            
            pygame.display.flip()
            self.horloge.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jeu = CourseAchilleTortue()
    jeu.executer()