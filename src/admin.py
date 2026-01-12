import os
from flask_admin import Admin
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    class UserModelView(ModelView):
        column_auto_select_related = True
        colum_list = ['id', 'email', 'password', 'is active', 'favorites']
    
    class CharacterModelView(ModelView):
        column_auto_select_related = True
        colum_list = ['id', 'name', 'height', 'favorite_by']

    class PlanetModelView(ModelView):
        column_auto_select_related = True
        colum_list = ['id', 'name', 'climate', 'favorite_by']
    
    class FavoriteCharacterModelView(ModelView):
        column_auto_select_related = True
        colum_list = ['id', 'user_id', 'character_id']
    
    class FavoritePlanetModelView(ModelView):
        column_auto_select_related = True
        colum_list = ['id', 'user_id', 'planet_id']
    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharacterModelView(Character, db.session))
    admin.add_view(PlanetModelView(Planet, db.session))
    admin.add_view(FavoriteCharacterModelView(FavoriteCharacter, db.session))
    admin.add_view(FavoritePlanetModelView(FavoritePlanet, db.session))


    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))