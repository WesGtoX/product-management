import logging

from main import db, Product

logger = logging.getLogger(__name__)


class APIService:

    def __init__(self, data):
        self.data = data

    def create(self):
        product = Product(id=self.data.get('id'), title=self.data.get('title'), image=self.data.get('image'))
        db.session.add(product)
        db.session.commit()

        logger.info('product created')

    def update(self):
        product = Product.query.get(self.data.get('id'))
        product.title = self.data.get('title')
        product.image = self.data.get('image')
        db.session.commit()

        logger.info('product updated')

    def delete(self):
        product = Product.query.get(self.data.get('pk'))
        db.session.delete(product)
        db.session.commit()

        logger.info('product deleted')
