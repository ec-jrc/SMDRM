import os
from flask import current_app, send_from_directory
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from api.core.triggers import AirflowJobsTrigger

ns = Namespace('uploads', description='File upload operations')

parser = ns.parser()
parser.add_argument('file', location='files', help="The zipfile to upload.",
                           type=FileStorage, required=True)
parser.add_argument('dag_id', location='args', default="twitter", help="The ID of the Airflow DAG workflow in charge to run the pipeline.", required=True)
parser.add_argument('collection_id', location='args', default="smdrm_uploads-volume", help="The ID of the collection from which the upload comes.", required=True)


@ns.route('/')
class Uploads(Resource):
    @ns.doc('list_uploads')
    def get(self):
        '''List uploads'''
        upload_dir = os.path.join(current_app.instance_path, 'uploads')
        return os.listdir(upload_dir)


@ns.route('/upload/')
@ns.expect(parser)
@ns.response(413, 'Upload exceeds the max size limit')
@ns.response(415, 'Upload content type is not "application/zip"')
class Upload(Resource):
    @ns.doc('upload_file')
    def post(self):
        '''Upload a zipfile.'''
        args = parser.parse_args()
        # FileStorage instance
        fs = args['file']

        # check if content is zip
        if fs.content_type != "application/zip":
            ns.abort(415)

        # ensure upload directory exists
        upload_dir = os.path.join(current_app.instance_path, 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # cache upload
        filename = secure_filename(fs.filename)
        filepath = os.path.join(upload_dir, filename)
        fs.save(filepath)
        current_app.logger.debug(filepath+" uploaded")

        # trigger Airflow DAG run on this file
        response = AirflowJobsTrigger.run_dag(filename=filename, dag_id=args["dag_id"], collection_id=args["collection_id"])
        current_app.logger.debug(response)

        return {'filename': filename, 'airflow_response': response}, 201


@ns.route('/download/<path:filename>')
@ns.param('filename', 'The name of the file to download')
@ns.response(404, 'File not found')
class Download(Resource):
    @ns.doc('download_file')
    def get(self, filename):
        '''Download a file from uploads directory.
        Raise a 404 NotFound error if file do not exist.'''
        upload_dir = os.path.join(current_app.instance_path, 'uploads')
        return send_from_directory(upload_dir, filename, as_attachment=True)
