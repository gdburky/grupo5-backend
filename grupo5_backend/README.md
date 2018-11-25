# Endpoints Backend G5

**URL** base:

      http://charette14.ing.puc.cl/

Para utilizar distintas API solo se debe cambiar el prefijo:

API grupo 5:

      /api

API grupo 3:

      /api/g3

## People

### Registro

[POST] /people

Permite crear un nuevo usuario.

### Login

[POST] /people/login

Permite iniciar sesión en la aplicación.

### Logout

[POST] /people/logout

Permite cerrar sesión.

### Change password

[POST] /people/change-password

Permite cambiar la contraseña.

### Person

[GET] /people/{id}

Entrega un usuario determinado.

[PUT] /people/{id}

Modifica los datos del usuario.

[DELETE] /people/{id}

Elimina el usuario correspondiente (Cerrar cuenta).

### Person collection

[GET] /people

Obtiene todos los usuarios.

###  Subscriptions collection

[GET] /people/{id}/subscriptions

Obtiene todos los posts suscritos por el usuario.

[POST] /people/{id}/subscriptions

Crea una nueva suscripción para el usuario

### Subscriptions

[DELETE] /people/{id}/subscriptions/{sub_id}

Elimina la suscripción.

## Posts

### Post collection

[GET] /posts

Obtiene todos los posts.

[POST] /posts

Crea un nuevo post.

### Post

[GET] /posts/{id}

Obtiene un post específico.

### Messages by post

[GET] /posts/{id}/messages

Obtiene los mensajes de un post.

[POST] /posts/{id}/messages

Crea un nuevo mensaje asociado al post.

### Filter post

[GET] /posts/filter/{hashtag}

Entrega todos los posts filtrados por *hashtag*.

## Mensajes

### Message

[GET] /messages/{id}

Entrega un mensaje determinado.

[DELETE] /messages/{id}

Elimina un determinado mensaje.

### Responses by message

[GET] /messages/{id}/responses

Entrega todas las respuestas a un mensaje.

[POST] /messages/{id}/responses

Crea una nueva respuesta a un mensaje.

### Filter message

[GET] /messages/filter/{hashtag}

Filtra los mensajes por *hashtag*.
