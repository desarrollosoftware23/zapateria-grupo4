{
    'name': 'Zapatos Temporada',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Módulo para agregar temporada a los zapatos',
    'description': 'Extiende el modelo de zapatos para almacenar la temporada de cada modelo y mostrarla en las vistas.',
    'author': 'JZAdy',
    'depends': ['zapatos'],
    'data': [
        'views/temporada_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
} 