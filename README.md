**Konstantin Gustafsson Docker-projekti**

Esittely Docker Compose -taidoistani.

**Käyttöohjeet**

- Mene projektin pääkansioon.
- Käynnistä sovellus:

```bash
docker compose up --build -d
```

- Mene selaimella osoitteeseen http://localhost:8080/ tai suoraan http://localhost:8080/page2.html.
- Tallenna viestejä sovelluksessa.
- Sammuta sovellus:

```bash
docker compose down
```

**Rakenne**

```text
kg_docker_project/
├── compose.yaml
├── README.md
├── kg-app/
│   ├── Dockerfile
│   └── server.py
└── nginx/
    ├── Dockerfile
    ├── default.conf
    └── html/
        ├── index.html
        └── page2.html
```

**Palvelut**

- **Nginx:** Näyttää webbisivut ja välittää pyynnöt Pythonille.
- **Python:** Käsittelee pyynnöt ja tallentaa sekä hakee viestejä tietokannasta.
- **PostgreSQL:** Tallentaa viestit tietokantaan.

Docker Compose käynnistää kaikki kolme palvelua ja yhdistää ne toisiinsa.