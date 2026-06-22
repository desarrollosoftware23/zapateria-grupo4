{
    'name': 'Zapatos - Devoluciones y Cambios',
    'version': '1.0',
    'summary': 'Gestión de devoluciones y cambios de zapatos',
    'description': 'Módulo para registrar devoluciones y cambios de zapatos.',
    'author': 'Franchesco',
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': ['zapatos'],
    'data': [
        'security/ir.model.access.csv',
        'views/devolucion_views.xml',
    ],
    'installable': True,
    'application': True,
}
