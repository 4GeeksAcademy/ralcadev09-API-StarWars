import os
from flask_admin import Admin
from models import db, User, Characters, FavoriteCharacters, Planet, FavoritePlanet
from flask_admin.contrib.sqla import ModelView

class FavoriteCharactersModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'user_id', 'user', 'character_id', 'character']

class UserModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'email', 'password', 'is_active', 'favorite_characters', 'favorite_planets']

class CharacterModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'name', 'height', 'weight', 'favorite_by']

class PlanetModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'name', 'population', 'weather', 'favorite_by']

class FavoritePlanetModelView(ModelView):
    column_auto_selected_related = True
    column_list = ['id', 'user_id', 'user', 'planet_id', 'planet']


    
def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharacterModelView(Characters, db.session)) 
    admin.add_view(FavoriteCharactersModelView(FavoriteCharacters, db.session))
    admin.add_view(PlanetModelView(Planet, db.session))  
    admin.add_view(FavoritePlanetModelView(FavoritePlanet, db.session)) 
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))