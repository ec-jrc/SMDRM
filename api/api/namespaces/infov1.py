from flask_restx import Namespace, Resource

ns = Namespace('info', description='API status operations')

@ns.route('/health')
class InfoHealth(Resource):
    @ns.doc('get_health')
    def get(self):
        '''API health'''
        return ["OK"], 200
