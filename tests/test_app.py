"""Tests de l'application Flask (utilisés par le Job 1 du pipeline CI/CD)."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import main  # noqa: E402


@pytest.fixture
def client():
    main.app.config["TESTING"] = True
    with main.app.test_client() as client:
        yield client


def test_page_accueil_repond(client):
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert b"Functions" in reponse.data


def test_page_accueil_liste_les_fonctions(client):
    reponse = client.get("/")
    for lien in [b"/cookie", b"/lookup", b"/evaluate", b"/xml", b"/config", b"/sayhi", b"/listservices"]:
        assert lien in reponse.data


def test_salutation_personnalisee(client):
    reponse = client.post("/sayhi", data={"name": "Alice"})
    assert reponse.status_code == 200
    assert b"Bonjour Alice!" in reponse.data


def test_cookie_est_enregistre(client):
    reponse = client.post("/cookie", data={"value": "atelier"})
    assert reponse.status_code == 200
    assert "value=" in reponse.headers.get("Set-Cookie", "")


def test_page_config_masque_les_secrets(client):
    reponse = client.get("/config")
    assert reponse.status_code == 200
    assert b"secret_admin_value - Not Viewable" in reponse.data


def test_padding_aller_retour():
    message = b"bonjour"
    assert main.unpad(main.pad(message)) == message


def test_chiffrement_aller_retour():
    message = b"Integration continue"
    chiffre = main.encrypt(message, main.KEY)
    assert chiffre != message
    assert main.decrypt(chiffre, main.KEY) == message
