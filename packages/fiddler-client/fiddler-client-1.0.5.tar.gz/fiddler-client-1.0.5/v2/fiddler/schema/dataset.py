from client.v2.fiddler.schema.base import BaseDataSchema


class Dataset(BaseDataSchema):

    id: int
    name: str
    version: str
    file_list: dict
    info: dict
    organization_name: str
    project_name: str
