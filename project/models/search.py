from project import db

#tabulka ktora zaznamenava informacie o vyhladani - nazov knihy, meno autora a link na tu stranku
class FoundBookInfo(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    choice_num = db.Column(db.Integer, nullable=True)
    result_id = db.Column(db.Integer, db.ForeignKey("result.id"), nullable=False)


#tabulka v ktorej su zaznamenane vyhladavane slova (teda nazov knihy) a prve vysledky ktore naslo na danom linku
class Result(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    searched_words = db.Column(db.String, nullable=False)
    results = db.relationship("FoundBookInfo", backref=db.backref("the_result"), lazy=True)