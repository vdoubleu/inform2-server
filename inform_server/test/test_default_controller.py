# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from inform_server.models.article import Article  # noqa: E501
from inform_server.models.opinion import Opinion  # noqa: E501
from inform_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_articles(self):
        """Test case for get_articles

        gets articles
        """
        query_string = [('start', 1),
                        ('max_amount', 100),
                        ('author', 'author_example')]
        response = self.client.open(
            '/VictorW/InformAPI/1.0.0/article',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_opinion(self):
        """Test case for get_opinion

        gets opinion
        """
        query_string = [('article_id', 789),
                        ('user', 'user_example')]
        response = self.client.open(
            '/VictorW/InformAPI/1.0.0/opinion',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_articles(self):
        """Test case for post_articles

        post article
        """
        body = Article()
        response = self.client.open(
            '/VictorW/InformAPI/1.0.0/article',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_opinion(self):
        """Test case for post_opinion

        send opinion
        """
        body = Opinion()
        response = self.client.open(
            '/VictorW/InformAPI/1.0.0/opinion',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
