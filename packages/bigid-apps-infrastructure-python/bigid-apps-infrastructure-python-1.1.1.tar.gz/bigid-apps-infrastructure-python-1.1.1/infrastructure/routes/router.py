import falcon
import json

from infrastructure.dto.ExecutionContext import ExecutionContext
from infrastructure.services.manifest_service import ManifestService
from infrastructure.types.enums import IconType


class LogsRouter:
    def __init__(self, logs_service):
        self.logs_service = logs_service;

    def on_get(self, req, resp):
        resp.body = self.logs_service.logs()
        resp.status = falcon.HTTP_200


class ManifestRouter:
    def __init__(self, manifest_path):
        self.manifest_service = ManifestService(manifest_path)

    def on_get(self, req, resp):
        try:
            resp.body = self.manifest_service.manifest()
        except IOError:
            print("Could not read manifest")
            resp.status = falcon.HTTP_404
            return
        resp.status = falcon.HTTP_200


class ExecutionRouter:
    def __init__(self, execution_service):
        self.execution_service = execution_service

    def on_post(self, req, resp):
        if req.content_length:
            req = json.load(req.stream)
        try:
            execution_context = ExecutionContext(req)
            resp.body = self.execution_service.execute(execution_context)
            resp.status = falcon.HTTP_200
        except NameError:
            print("Can't execute action")
            resp.status = falcon.HTTP_400


class IconRouter:
    def __init__(self, logo_service):
        self.logo_service = logo_service

    def on_get(self, req, resp):
        icon_type = req.path.split('/')[-1]
        resp.body = self.logo_service.get_icon_stream(IconType[icon_type])
        resp.status = falcon.HTTP_200


def create_api(execution_service, logo_service, manifest_path):
    icon_router = IconRouter(logo_service)
    app = falcon.App()
    app.add_route('/execute', ExecutionRouter(execution_service))
    app.add_route('/logs', LogsRouter(execution_service.logger))
    app.add_route('/manifest', ManifestRouter(manifest_path))
    app.add_route('/assets/' + IconType.icon.name, icon_router)
    app.add_route('/assets/' + IconType.sideBarIcon.name, icon_router)

    return app
