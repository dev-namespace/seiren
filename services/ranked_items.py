#!/usr/bin/env python

from seiren.models.ranked_items import RankedVocabularyItem
from seiren.database import db
import uuid, datetime

# @TODO: type: grammar / type: vocabulary
# @TODO: language (so we can filter)
default_item = {
    'id': str(uuid.uuid4()),
    'repetitions': 0,
    'easiness': 2.5,
    'interval': 1,
    'next_review': datetime.date.today(),
    'last_review': datetime.date.today(),
}

def add_item(item):
    input_item = {**default_item, **item}
    new_item = RankedVocabularyItem(**input_item)
    db.session.add(new_item)
    db.session.commit()
    return new_item

def update_item(item):
    current_item = RankedVocabularyItem.query.filter_by(id=item_id).first()
    current_item.update(**item)

def update_item_rank(item_id, quality):
    item = RankedVocabularyItem.query.filter_by(id=item_id).first()
    if quality < 3:
        item.repetitions = 0
        item.interval = 1
    else:
        if item.repetitions == 0:
            item.interval = 1
        elif item.repetitions == 1:
            item.interval = 2 # 6 in the original algorithm
        else:
            item.interval = min(item.interval * item.easiness, 500)

    item.repetitions += 1
    item.easiness = max(1.3, item.easiness + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
    item.next_review = datetime.date.today() + datetime.timedelta(days=(item.interval - 1)) # original algorithm doesn't substract 1
    item.last_review = datetime.date.today()
    db.session.commit()
    return item

def find_item(item_id):
    print(f"finding {item_id}")
    return RankedVocabularyItem.query.filter_by(id=item_id).first()

def find_item_by_content(item_content):
    return RankedVocabularyItem.query.filter_by(content=item_content).first()

def find_items():
    return RankedVocabularyItem.query.all()

def find_due_items(limit):
    return RankedVocabularyItem.query.filter(RankedVocabularyItem.next_review <= datetime.datetime.now()).limit(limit).all()

def remove_item(item_id):
    item = RankedVocabularyItem.query.filter_by(id=item_id).first()
    print(item)
    db.session.delete(item)
    db.session.commit()
