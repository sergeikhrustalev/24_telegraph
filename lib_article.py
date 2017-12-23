import os
import json
import time


class Article:

    def __init__(self, header, signature, body):

            self.header = header
            self.signature = signature
            self.body = body

    @classmethod
    def from_json(cls, json_string):

        structure = json.loads(json_string)

        return cls(
            structure['header'],
            structure['signature'],
            structure['body'],
        )

    @property
    def jsonify(self):

        return json.dumps(

            dict(
                header=self.header,
                signature=self.signature,
                body=self.body,
            ),

            indent=2,

            ensure_ascii=False,
        )


class ArticleStorage:

    def __init__(self, article_dir):
        self._article_dir = article_dir
        os.makedirs(self._article_dir, exist_ok=True)

    def add(self, article):

        epoch_time = int(time.time())

        article_id = '{}-{}'.format(
            article.header,
            epoch_time,
        )

        filepath = os.path.join(
            self._article_dir,
            article_id,
        )

        with open(filepath, 'w') as file_handler:
            file_handler.write(article.jsonify)

    def get(self, article_id):

        filepath = os.path.join(
            self._article_dir,
            article_id,
        )

        if os.path.exists(filepath):

            with open(filepath) as file_handler:
                json_string = file_handler.read()

            return Article.from_json(json_string)
