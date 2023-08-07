#!/usr/bin/env python

from seiren.database import db
import uuid, json, datetime

class RankedVocabularyItem(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=True)
    repetitions = db.Column(db.Integer, nullable=False)
    interval = db.Column(db.Integer, nullable=False)
    easiness = db.Column(db.Float, nullable=False)
    next_review = db.Column(db.DateTime, nullable=False)
    last_review = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<RankedItem id:{self.id} content:{self.content} reps: {self.repetitions} interval: {self.interval} due: {self.next_review.date() <= datetime.date.today()}>'

    def object_as_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'language': self.language,
            'content': self.content,
            'repetitions': self.repetitions,
            'interval': self.interval,
            'easiness': self.easiness,
            'next_review': str(self.next_review),
            'last_review': str(self.last_review)
        }

    def serialize(self):
        return json.loads(json.dumps(self.object_as_dict()))
