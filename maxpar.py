import time
import random

class Task:
    def __init__(self):
        self.name = ""
        self.reads = []
        self.writes = []
        self.run = None

class TaskSystem:
    def __init__(self, tasks, precedence):
        self.tasks = tasks
        self.precedence = precedence

        # --- Partie_Yassine ---

        def draw(self):
            """affiche le graphe de précédence de manière lisible"""
            print("\n=== GRAPHE DE PRÉCÉDENCE ===")
            if not self.precedence:
                print("Aucune contrainte de précédence.")
            for tache, parents in self.precedence.items():
                if not parents:
                    print(f"[Début] -> {tache}")
                for p in parents:
                    print(f"{p} ---> {tache}")
            print("============================\n")

        def detTestRnd(self, dic_globals):
            """vérifie si le résultat change avec des valeurs aléatoires"""
            print("=== TEST DE DÉTERMINISME ALÉATOIRE ===")
            all_reads = set()
            for t in self.tasks:
                all_reads.update(t.reads)

            # génère des valeurs au hasard pour ces variables
            test_values = {var: random.randint(1, 100) for var in all_reads}

            # 1. test séquentiel
            for var, val in test_values.items(): dic_globals[var] = val
            self.runSeq()
            res_seq = {t.name: {v: dic_globals.get(v) for v in t.writes} for t in self.tasks}

            # 2. test parallèle
            for var, val in test_values.items(): dic_globals[var] = val
            self.run()
            res_par = {t.name: {v: dic_globals.get(v) for v in t.writes} for t in self.tasks}

            if res_seq == res_par:
                print("✅ SUCCÈS : Les résultats sont identiques.")
            else:
                print("❌ ÉCHEC : Différence détectée entre séquentiel et parallèle !")

        def parCost(self):
            """compare le temps d'exécution moyen"""
            print("=== ANALYSE DES PERFORMANCES (Coût) ===")
            nb_essais = 5

            # mesure séquentielle
            start_seq = time.time()
            for _ in range(nb_essais): self.runSeq()
            avg_seq = (time.time() - start_seq) / nb_essais

            # mesure parallèle
            start_par = time.time()
            for _ in range(nb_essais): self.run()
            avg_par = (time.time() - start_par) / nb_essais

            print(f"Moyenne Séquentielle : {avg_seq:.5f}s")
            print(f"Moyenne Parallèle   : {avg_par:.5f}s")

            if avg_par < avg_seq:
                gain = ((avg_seq - avg_par) / avg_seq) * 100
                print(f"🚀 Gain de performance : {gain:.1f}%")
            else:
                print("ℹ️ Le mode parallèle n'est pas plus rapide sur ce petit exemple.")