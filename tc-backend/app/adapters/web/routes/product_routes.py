from flask_restx import Namespace, Resource, fields

ns = Namespace("product", description="Product operations")

model = ns.model('Model', {
    'name': fields.String
})

@ns.route("")
class ProductResource(Resource):
    @ns.marshal_with(model, as_list=True, code=200)
    def get(self):
        return [{"name": "wine"}]
