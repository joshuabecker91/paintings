from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User





# -----------------------------------------------------------------------------

class Painting:
    db_name = 'paintings'

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.painted_by = User.get_by_id(data['user_id'])

    @classmethod
    def save(cls,data):
        query = "INSERT INTO paintings (title, description, price, quantity, user_id) VALUES (%(title)s,%(description)s,%(price)s,%(quantity)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_paintings = []
        if results:
            for row in results:
                # print(row['date_of_painting'])
                all_paintings.append( cls(row) )
        return all_paintings

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM paintings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s, quantity=%(quantity)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def owned_painting(cls):
        query = "SELECT * FROM purchased_paintings JOIN paintings WHERE id = painting_id;"
        return connectToMySQL(cls.db_name).query_db(query)
    
    @classmethod
    def buy_painting(cls,data):
        query = "INSERT INTO purchased_paintings (user_id, painting_id) VALUES (%(user_id)s,%(id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def update_inventory(cls,data):
        query = "UPDATE paintings SET quantity = quantity - 1 WHERE id = %(id)s"
        return connectToMySQL(cls.db_name).query_db(query,data)

# Validations-------------------------------------------------------------------

    @staticmethod
    def validate_painting(painting):
        is_valid = True
        if len(painting['title']) < 2:
            is_valid = False
            flash("Title must be at least 2 characters","painting")
        if len(painting['description']) < 10:
            is_valid = False
            flash("Description must be at least 10 characters","painting")
        if len(painting['price']) < 1:
            is_valid = False
            flash("Please enter the price - between 1 and one million dollars","painting")
        if len(painting['quantity']) < 1:
            is_valid = False
            flash("Please enter the quantity of paintings available - between 1 and 100","painting")
        return is_valid
