from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_characters: Mapped[list['FavoriteCharacters']] = relationship(back_populates='user')
    favorite_planets: Mapped[list['FavoritePlanet']] = relationship(back_populates='user')

    def __str__(self):
        return f'Usuario {self.email}'
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active
        }


class Characters(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[int] = mapped_column(Integer)
    favorite_by: Mapped[list['FavoriteCharacters']] = relationship(
        back_populates=('character')
    )
    

    def __str__(self):
        return f'Character {self.name}'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height, 
            'weight': self.weight
        }


class FavoriteCharacters(db.Model):
    __tablename__ = 'favorite_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favorite_characters')
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    character: Mapped['Characters'] = relationship(back_populates='favorite_by')

    def __str__(self):
        return f'{self.user} likes {self.character}'
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character_id': self.character_id 
          
        }
    
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    population: Mapped[int] =mapped_column(Integer, nullable=True)
    weather: Mapped[str] = mapped_column(String(25)) 
    favorite_by: Mapped[list['FavoritePlanet']] = relationship(back_populates='planet')

    def __str__(self):
        return f'Planet {self.name}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'population': self.population,
            'weather': self.weather
            }


class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favorite_planets')
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'))
    planet: Mapped['Planet'] = relationship(back_populates='favorite_by')

    def __str__(self):
        return f'{self.user} likes {self.planet}' 
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id 
          
        }



   
