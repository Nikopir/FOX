from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Boolean, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from hashlib import sha256

Base = declarative_base()

DB_NAME = 'fox.db'
engine = create_engine(f"sqlite:///{DB_NAME}")
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    progress = relationship("Progress", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("Settings", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Progress(Base):
    __tablename__ = 'progress'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    score = Column(Integer, nullable=False)
    completed = Column(Boolean, nullable=False)
    time_spent = Column(Integer, nullable=False)

    user = relationship("User", back_populates="progress")


class Words(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)


class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sound_volume = Column(Float, nullable=False, default=1.0)
    music_volume = Column(Float, nullable=False, default=1.0)
    language = Column(String, nullable=False, default="en")

    user = relationship("User", back_populates="settings")


Base.metadata.create_all(engine)


class DatabaseManager:

    def __init__(self):
        self.session = Session()
        self.current_user = None

    @staticmethod
    def hash_password(password):
        return sha256(password.encode()).hexdigest()

    def add_user(self, login, password):
        if self.get_user(login):
            return False

        new_user = User(
            login=login,
            password=self.hash_password(password)
        )
        self.session.add(new_user)
        self.session.commit()
        return True

    def get_user(self, login):
        return self.session.query(User).filter_by(login=login).first()

    def check_password(self, login, password):
        user = self.get_user(login)
        if user and user.password == self.hash_password(password):
            self.current_user = login
            return True
        return False

    def add_word(self, word):
        try:
            new_word = Words(word=word.upper())
            self.session.add(new_word)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False

    def get_all_words(self):
        return [word.word for word in self.session.query(Words).all()]

    def add_progress(self, user_id, score, completed):
        progress = self.session.query(Progress).filter_by(user_id=user_id).first()

        if progress:
            progress.score = max(progress.score, score)
            progress.completed = completed
        else:
            progress = Progress(user_id=user_id, score=score, completed=completed, time_spent=0)
            self.session.add(progress)

        self.session.commit()
        return True

    def get_user_progress(self, user_id):
        return self.session.query(Progress).filter_by(user_id=user_id).first()
