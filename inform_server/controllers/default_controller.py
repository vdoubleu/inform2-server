import connexion
import six

from inform_server.models.article import Article  # noqa: E501
from inform_server.models.opinion import Opinion  # noqa: E501
from inform_server import util

import mysql.connector
import time

from .score import score_post

db = mysql.connector.connect(
    host="mgs0iaapcj3p9srz.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    user="zh9ql9bzpkim7foo",
    passwd="j1gwa06g7l7jcked",
    database="mt0kqyyfyc0jaz07"
)

cursor = db.cursor()

def get_articles(start=None, max_amount=None, author=None):  # noqa: E501
    """gets articles

    By passing in the appropriate options, you can search for  the desired articles in the system  # noqa: E501

    :param start: start at the nth position in terms of articles to return
    :type start: int
    :param max_amount: the max amount of articles to return
    :type max_amount: int
    :param author: returns only articles by the specified author
    :type author: str

    :rtype: List[Article]
    """
   
    m = max_amount if max_amount is not None else 100
    s = start if start is not None else 1

    if author is not None:
        cursor.execute("SELECT * FROM articles WHERE author='" + author + "' ORDER BY score LIMIT " + str(m) + " OFFSET " + str(s - 1)) 
    else:
        cursor.execute("SELECT * FROM articles ORDER BY score LIMIT " + str(m) + " OFFSET " + str(s - 1))

    out = cursor.fetchall()

    res = map(lambda a: {"id": a[0], "title": a[1], "body": a[2], "author": a[3], "category": a[4], "time": a[5]}, out)

    return list(res)

def get_opinion(article_id=None, user=None):  # noqa: E501
    """gets opinion

    gets a users opinion on an article # noqa: E501

    :param article_id: article id
    :type article_id: int
    :param user: user name
    :type user: str

    :rtype: int
    """

    if article_id is None or user is None:
        return "one or more arguments were null"

    cursor.execute("SHOW TABLES LIKE 'opinion" + str(article_id) + "'")
    res = cursor.fetchone()

    if res:
        cursor.execute("SELECT value FROM opinion" + str(article_id))
        op = (cursor.fetchall())

        if len(op) == 0:
            out = 0
        else:
            out = op[0][0]

        cursor.execute("SELECT totalLikes, totalDislikes FROM articles where id=" + str(article_id))

        likes = cursor.fetchall()

        return {"opinion": out, "totalLikes": likes[0][0], "totalDislikes": likes[0][1]}
    else:
        return {"opinion": 0}

def post_articles(body=None):  # noqa: E501
    """post article

    Adds an article to the system # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    res = {}

    if connexion.request.is_json:
        body = Article.from_dict(connexion.request.get_json())  # noqa: E501

        #score = score_post(body.post_time, 0, 0)

        newArticle = (body.title, body.body, body.category, body.author, body.post_time, 0, 0, 10)
        addArticle = "INSERT INTO articles(title, body, category, author, time, totalLikes, totalDislikes, score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(addArticle, newArticle)
        db.commit()

        cursor.execute("SELECT id FROM articles WHERE title='" + body.title + "' AND author='" + body.author + "' AND category='" + body.category +"' AND time=" + str(body.post_time))
        articleID = cursor.fetchall()

        cursor.execute("CREATE TABLE opinion" + str(articleID[0][0]) + " (user VARCHAR(255), value smallint)")

        res = {"id": articleID[0][0], "title": body.title, "body": body.body, "category": body.category, "author": body.author, "postTime": body.post_time}

    return res 


def post_opinion(body=None):  # noqa: E501
    """send opinion

    Adds an opinion # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Opinion.from_dict(connexion.request.get_json())  # noqa: E501

        cursor.execute("SELECT * FROM opinion" + str(body.id) + " WHERE user='" + body.user + "'")
        
        #checks if value already exists in the opinion table to determine whether to add or modify value
        if len(cursor.fetchall()) == 0:
            insertOpinion = "INSERT INTO opinion" + str(body.id) + " (user, value) VALUES (%s, %s)"
            newOpinion = (body.user, body.value)
            cursor.execute(insertOpinion, newOpinion)
        else:
            cursor.execute("SELECT value FROM opinion" + str(body.id) + " WHERE user='" + body.user + "'")
            oldVal = (cursor.fetchall())[0][0]

            #decrease like/dislike count if necessary
            if oldVal == 1:
                cursor.execute("UPDATE articles SET totalLikes = totalLikes - 1 WHERE id=" + str(body.id))
            elif oldVal == -1:
                cursor.execute("UPDATE articles SET totalDislikes = totalDislikes - 1 WHERE id=" + str(body.id))

            #update user value in the opinion table
            cursor.execute("UPDATE opinion" + str(body.id) + " SET value=" + str(body.value) + " WHERE user='" + body.user + "'")

        #increase like/dislike count
        if body.value == 1:
            cursor.execute("UPDATE articles SET totalLikes = totalLikes + 1 WHERE id=" + str(body.id))
        elif body.value == -1:
            cursor.execute("UPDATE articles SET totalDislikes = totalDislikes + 1 WHERE id=" + str(body.id))


        db.commit()

    return 'success'
