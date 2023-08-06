from client.v2.fiddler.schema.base import BaseDataSchema


class Project(BaseDataSchema):
    name: str
    organization_name: str
