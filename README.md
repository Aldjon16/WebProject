# GjejMjeshtrin

Platformë web për të lidhur klientët me profesionistë lokalë në Shqipëri — hidraulikë, elektricistë, mekanikë, piktorë, fotografë, programues, dhe shërbyes të tjerë.

---

## Funksionalitete

- Regjistrim & Autentikim (Klient / Profesionist / Admin)
- Profil profesional me foto, përshkrim, eksperiencë
- Kërkim sipas emrit, profesionit, qytetit
- Vlerësime dhe komente (1–5 yje)
- Paneli i profesionistit (ndrysho profilin, shiko vlerësimet)
- Paneli administrativ (menaxho përdorues, aprovo profile, menaxho kategori)

---

## Teknologjitë

- **Backend:** Python, Flask
- **Databaza:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Imazhe:** Pillow

---

## Instalimi

```bash
# Klono projektin
git clone https://github.com/Aldjon16/WebProject.git
cd WebProject

# Krijo virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalo varësitë
pip install -r requirements.txt

# Nis serverin
python app.py
```

Hape në browser: http://127.0.0.1:5000/

---

## Llogaritë Default

| Roli  | Emri | Fjalëkalimi |
|-------|------|-------------|
| Admin | admin | admin123   |

---

## Struktura e Projektit

```
WebProject/
├── app.py              # Flask app factory
├── config.py           # Konfigurimet
├── models.py           # Modelet e databazës
├── requirements.txt    # Varësitë Python
├── routes/
│   ├── auth.py         # Autentikim (login, register, logout)
│   ├── main.py         # Kryefaqja, kërkim
│   ├── professional.py # Profili profesional (CRUD)
│   ├── review.py       # Vlerësimet
│   └── admin.py        # Paneli administrativ
├── templates/
│   ├── base.html
│   ├── auth/
│   ├── main/
│   ├── professional/
│   └── admin/
└── static/
    ├── css/style.css
    ├── js/main.js
    └── images/profiles/
```

---

## Kategoritë

| Kodi | Emri |
|------|------|
| hidraulik | Hidraulik |
| elektricist | Elektricist |
| mekanik | Mekanik |
| piktor | Piktor |
| fotograf | Fotograf |
| programues | Programues |
| kondicionim | Teknik Kondicionimi |
| pastrim | Shërbime Pastrimi |
| mobileri | Specialist Mobiliesh |

---

## Autorë

- Aldjon Kacollja
- Eneriko Troka
- Zenel Rrugeja
- Alek Ahmeti
- Daniel Basha

---

## Licenca

Projekt edukativ — të gjitha të drejtat e rezervuara.
