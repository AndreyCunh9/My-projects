from app import app, db, Document
from datetime import datetime
import pytz

with app.app_context():
    new_document = Document(
        title="Documento Teste",
        filename="teste.pdf",
        sector="FINANCEIRO",
        document_type="Notas Fiscais",
        username="usuario_teste",
        created_at=datetime.now(pytz.UTC)
    )
    db.session.add(new_document)
    db.session.commit()
