from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not (len(name) == 0) and name not in [a.name for a in Author.query.all()]:
            return name
        raise ValueError('Invalid name!')

    @validates('phone_number')
    def validate_phone_number(self, key, number):
        number_to_string = str(number)
        if number_to_string.isdigit() and len(number_to_string) == 10:
            return number
        raise ValueError('Invalid phone number!')


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, title):
        keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if any(keyword in title for keyword in keywords):
            return title
        raise ValueError('''title must contain one of the following:
                         * "Won't Believe"
                         * "Secret"
                         * "Top"
                         * "Guess"''')
    
    @validates('content')
    def validate_content(self, key, content):
        if len(content) >= 250:
            return content
        raise ValueError('content must be at least 250 characters!')
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) <= 250:
            return summary
        raise ValueError('summary must not be more than 250 characters!')
    
    @validates('category')
    def validate_category(self, key, category):
        if (category == 'Fiction') or  (category == 'Non-Fiction'):
            return category
        raise ValueError('category must be either Fiction or Non-Fiction.')
    


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
