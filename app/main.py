from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI()

database.init_db()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    db = next(get_db())
    for term in terms_to_add:
        add_term(term[0], term[1], db)
        print(f"Добавлен термин: {term[0]}")


@app.get("/terms/", response_model=list[schemas.Term])
def get_terms(db: Session = Depends(get_db)):
    return db.query(models.Term).all()

@app.get("/terms/{keyword}", response_model=schemas.Term)
def get_term(keyword: str, db: Session = Depends(get_db)):
    term = db.query(models.Term).filter(models.Term.keyword == keyword).first()
    if term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return term

@app.post("/terms/", response_model=schemas.Term)
def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    db_term = models.Term(keyword=term.keyword, description=term.description)
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term

@app.put("/terms/{term_id}", response_model=schemas.Term)
def update_term(term_id: int, term: schemas.TermCreate, db: Session = Depends(get_db)):
    db_term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    db_term.keyword = term.keyword
    db_term.description = term.description
    db.commit()
    db.refresh(db_term)
    return db_term

@app.delete("/terms/{term_id}", response_model=schemas.Term)
def delete_term(term_id: int, db: Session = Depends(get_db)):
    db_term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    db.delete(db_term)
    db.commit()
    return db_term
