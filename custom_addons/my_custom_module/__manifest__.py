   {
       'name': 'My Custom Module',
       'version': '1.0',
       'category': 'Sales',
       'summary': 'Custom extensions for product search',
       'description': """
           This module adds custom search functionality to products.
       """,
       'author': 'Your Name',
       'website': 'https://www.yourwebsite.com',
       'depends': ['product'],
       'data': [
           'views/product_views.xml',
       ],
       'installable': True,
       'application': False,
   }
