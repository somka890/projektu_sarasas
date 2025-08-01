from main import app, db, Projektas
from datetime import datetime

projektai = [
    Projektas(pavadinimas='Internetine parduotuve', kaina=1200.0, sukurimo_data=datetime(2023, 5, 1)),
    Projektas(pavadinimas='Mobilioji programele', kaina=1700.0, sukurimo_data=datetime(2022, 1, 16)),
    Projektas(pavadinimas='CRM sistema', kaina=2300.0, sukurimo_data=datetime(2020, 7, 19)),
]

with app.app_context():
    db.session.add_all(projektai)
    db.session.commit()
