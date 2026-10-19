# Atelier : introduction au CI/CD avec GitHub Actions

Dans cet atelier, vous allez automatiser le cycle de vie d'une petite application web Flask :
à chaque `git push`, GitHub va **tester** l'application, **construire** son image Docker,
puis **simuler sa mise en production**.

```
  git push
     │
     ▼
┌──────────┐      ┌──────────┐      ┌──────────────┐
│  Job 1   │ ───▶ │  Job 2   │ ───▶ │    Job 3     │
│  Tests   │      │  Docker  │      │  Production  │
└──────────┘      └──────────┘      └──────────────┘
  CI : on           CD : on           CD : on
  vérifie           emballe           déploie
```

Chaque job ne démarre **que si le précédent a réussi** : un test qui échoue bloque toute la suite.
C'est tout l'intérêt du CI/CD : on ne livre jamais une version cassée.

## Préparation

1. Faites un **fork** de ce dépôt sur votre compte GitHub.
2. Ouvrez votre fork dans un **Codespace** (bouton `Code` > `Codespaces`) ou clonez-le sur votre machine.
3. Allez dans l'onglet **Actions** de votre fork et activez les workflows si GitHub vous le demande.

Les fichiers que vous allez modifier :

| Fichier | Rôle |
|---|---|
| `.github/workflows/cicd.yml` | Le pipeline : les 3 jobs à compléter |
| `Dockerfile` | La recette de l'image Docker (Job 2) |
| `tests/test_app.py` | Les tests de l'application (fournis, à lire) |

Après chaque modification dans Codespace, pour pouvoir lancer vos Actions dans Github : `git add .`, `git commit` il faudra mettre un message, `git push`, puis observez le résultat dans l'onglet **Actions** dans GitHub.

## Job 1 : tester l'application

Complétez le job `Tests` du fichier `.github/workflows/cicd.yml` : il doit récupérer le code,
installer Python, installer les dépendances et lancer `pytest`.

Vous pouvez d'abord lancer les tests sur votre poste :

    pip install -r requirements.txt pytest
    pytest -v tests/

✅ **Validé quand** : le job `Tests` est vert et affiche la liste des tests passés.

🧪 **Expérience** : modifiez un test pour le faire échouer (par exemple, remplacez `"Hello Alice!"`
par `"Hello Alice!"`) et poussez. Que se passe-t-il pour les jobs 2 et 3 ? Remettez le test en état ensuite.

## Job 2 : construire l'image Docker

1. Complétez le `Dockerfile` en suivant les indications qu'il contient. Testez-le localement :

       docker build -t atelier-flask .
       docker run -p 4000:4000 atelier-flask

   puis ouvrez http://localhost:4000.

2. Complétez le job `Docker` du pipeline : construire l'image, l'exporter en fichier
   (`docker save`) et la transmettre au job suivant (`actions/upload-artifact`).

✅ **Validé quand** : le job `Docker` est vert et un artefact `image-docker` apparaît en bas de la page du pipeline.

## Job 3 : simuler la mise en production

Complétez le job `Production` : récupérer l'image du job 2, la charger, démarrer le conteneur
et vérifier avec `curl` que l'application répond. Terminez par un message de succès dans le
résumé du pipeline (`$GITHUB_STEP_SUMMARY`).

✅ **Validé quand** : les 3 jobs sont verts et le résumé du pipeline annonce la mise en production.

🔒 **Bonus : validation humaine avant la production.** Le job 3 utilise l'environnement `production`.
Dans `Settings` > `Environments` > `production`, cochez **Required reviewers** et ajoutez-vous.
Au prochain push, le pipeline s'arrête avant le job 3 et attend votre accord : c'est ainsi que
beaucoup d'équipes protègent leur production.

## Pour aller plus loin

- Ajouter un **linter** (`flake8`) dans le job 1.
- Publier l'image sur le **GitHub Container Registry** (`ghcr.io`) au lieu d'un artefact.
- Ne déclencher la mise en production que sur la branche `main` (`if: github.ref == 'refs/heads/main'`).
- Scanner l'image avec **Trivy** pour y chercher des vulnérabilités.

## À propos de l'application

⚠️ **L'application est volontairement vulnérable** (injections de code, de commandes, SQL…, voir
`vulnerability_index.md`) : ne la déployez jamais sur un serveur réellement accessible. Ici, la
« production » est simulée sur la machine jetable de GitHub Actions, qui est détruite à la fin du pipeline.

Pour lancer l'application sans Docker :

    pip install -r requirements.txt
    python main.py

Elle est alors accessible sur http://127.0.0.1:4000. Les options pour utiliser une autre base de données que
SQLite sont décrites par `python main.py --help` et dans `docker_database_setup.md`.
