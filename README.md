# hw05_final

Social network of bloggers

A community for publishing. A blog with an emphasis on publishing posts, subscribing to groups and authors, and commenting on posts.

### **Stack**
![python version](https://img.shields.io/badge/Python-3.7-green)
![django version](https://img.shields.io/badge/Django-2.2-green)
![pillow version](https://img.shields.io/badge/Pillow-8.3-green)
![pytest version](https://img.shields.io/badge/pytest-6.2-green)
![requests version](https://img.shields.io/badge/requests-2.26-green)
![sorl-thumbnail version](https://img.shields.io/badge/thumbnail-12.7-green)

### **Launching a project in dev mode**
The instructions are oriented towards the windows operating system and the git bash utility.<br/>
For other tools, use the command analogs for your environment.

1. Clone the repository and go to it in the command line:

```
git clone https://github.com/Hlompy/hw05_final.git
```

```
cd hw05_final
```

2. Install and activate the virtual environment
```
python -m venv venv
``` 
```
source venv/Scripts/activate
```

3. Install dependencies from requirements.txt file
```
pip install -r requirements.txt
```

4. In the folder with the manage.py file, run migrations:
```
python manage.py migrate
```

5. In the folder with the manage.py file, start the server by running the command:
```
python manage.py runserver
```

### *What users can do*:

**Logged in** users can:
1. View, post, delete, and edit their posts;
2. View community information;
3. View and post comments on their behalf to other users' posts *(including themselves)*, delete and edit **their** comments;
4. Subscribe to other users and view **their** subscriptions.<br/>
***Note***: Access to all write, update, and delete operations is only available after authentication and receiving a token.

**Anonymous :alien:** users can:
1. View posts;
2. View community information;
3. View comments;

### **Set of available endpoints** :point_down:_:
* ```posts/``` - Displaying posts and publications (_GET, POST_);
* ```posts/{id}``` - Getting, editing, deleting a post with the corresponding **id** (_GET, PUT, PATCH, DELETE_);
* ```posts/{post_id}/comments/``` - Getting comments to a post with the corresponding **post_id** and publishing new comments (_GET, POST_);
* ```posts/{post_id}/comments/{id}``` - Getting, editing, deleting a comment with the corresponding **id** to a post with the corresponding **post_id** (_GET, PUT, PATCH, DELETE_);
* ```posts/groups/``` - Getting descriptions of registered communities (_GET_);
* ```posts/groups/{id}/``` - Get a description of a community with the corresponding **id** (_GET_);
* ```posts/follow/``` - Get information about the current user's subscriptions, create a new subscription to the user (_GET, POST_).<br/>
