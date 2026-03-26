def interfere(t1, t2):

    r1 = set(t1.reads)
    w1 = set(t1.writes)

    r2 = set(t2.reads)
    w2 = set(t2.reads)

    cond_1 = bool(r1 & w2)
    cond_2 = bool(r2 & w1)
    cond_3 = bool(w1 & w2)

    return cond_1 or cond_2 or cond_3

class TaskSystem:
    def __init__(self, liste_taches, dict_precedence):

        self.precedence = dict_precedence

        self.tasks = {}
        for t in liste_taches:
            self.tasks[t.name] = t

def _get_tous_les_ancetres(self, nomTache):
    tous_les_ancetres = set()

    def fouiller_parents(tache_courante):
        parents_direct = self.precedence.get(tache_courante, [])

        for parent in parents_direct:
            if parent not in tous_les_ancetres:
                tous_les_ancetres.add(parent)
                fouiller_parents(parent)

    fouiller_parents(nomTache)

    return list(tous_les_ancetres)

def getDependencies(self, nomTache):
    if nomTache not in self.tasks:
        raise ValueError(f"Erreur : la tâche '{nomTache}' n'existe pas dans le système.")

    dependances_maximales = []
    tache_cible = self.tasks[nomTache]

    ancetres = self._get_tous_les_ancetres(nomTache)

    for nom_ancetre in ancetres:
        tache_ancetre = self.tasks[nom_ancetre]
        if interfere(tache_ancetre, tache_cible):
            dependances_maximales.append(nom_ancetre)

    return dependances_maximales