[GET] /people Listar todos los registros de people en la base de datos.
[GET] /people/<int:people_id> Muestra la información de un solo personaje según su id.
[GET] /planets Listar todos los registros de planets en la base de datos.
[GET] /planets/<int:planet_id>

#Opcional: trabajar con starships

[GET] /users  Listar todos los usuarios del blog.
[GET] /users/<int:user_id>/favorites Listar people y planes favoritos de un usuario
[POST] /favorite/<int:user_id>/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el id = planet_id.
[POST] /favorite/<int:user_id>/people/<int:people_id> Añade un nuevo people favorito al usuario actual con el id = people_id.
[DELETE] /favorite/<int:user_id>/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id.
[DELETE] /favorite/<int:user_id>/people/<int:people_id> Elimina un people favorito con el id = people_id.