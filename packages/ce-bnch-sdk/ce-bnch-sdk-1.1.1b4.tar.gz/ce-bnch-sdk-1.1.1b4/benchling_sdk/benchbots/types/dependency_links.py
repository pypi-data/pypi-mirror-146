from __future__ import annotations

from dataclasses import dataclass
from typing import List, Type, TypeVar, Union

from dataclasses_json import dataclass_json, DataClassJsonMixin
from dataclasses_json.core import Json
from dataclasses_jsonschema import JsonSchemaMixin


@dataclass_json
@dataclass
class NamedApiIdentifiedSublink(JsonSchemaMixin):
    # Sublinks like schema fields and dropdown options don't have a type
    name: str
    resourceId: str
    resourceName: str


@dataclass_json
@dataclass
class ApiIdentifiedLink(JsonSchemaMixin):
    name: str
    resourceId: str
    type: str


@dataclass_json
@dataclass
class NamedApiIdentifiedLink(ApiIdentifiedLink):
    resourceName: str


@dataclass_json
@dataclass
class SchemaFieldLink(NamedApiIdentifiedSublink):
    pass


@dataclass_json
@dataclass
class SchemaLink(NamedApiIdentifiedLink):
    fieldDefinitions: List[SchemaFieldLink]


@dataclass_json
@dataclass
class DropdownOptionLink(NamedApiIdentifiedSublink):
    pass


@dataclass_json
@dataclass
class WorkflowTaskOutputSchemaLink:
    fieldDefinitions: List[SchemaFieldLink]


@dataclass_json
@dataclass
class WorkflowTaskSchemaLink(SchemaLink):
    fieldDefinitions: List[SchemaFieldLink]
    output: WorkflowTaskOutputSchemaLink
    # "type" is a reserved word
    resourceType: str = "workflow_task_schema"


@dataclass_json
@dataclass
class WorkflowTaskStatusLink(NamedApiIdentifiedLink):
    # "type" is a reserved word
    resourceType: str = "workflow_task_status"


@dataclass_json
@dataclass
class DropdownLink(NamedApiIdentifiedLink):
    options: List[DropdownOptionLink]


@dataclass_json
@dataclass
class NamedResourceLink(NamedApiIdentifiedLink):
    pass


@dataclass_json
@dataclass
class UnnamedResourceLink(ApiIdentifiedLink):
    pass


T = TypeVar("T", bound="DependencyLinks")


@dataclass_json
@dataclass
class _DependencyLinks(DataClassJsonMixin):
    configuration: List[
        Union[
            SchemaLink,
            DropdownLink,
            NamedResourceLink,
            UnnamedResourceLink,
            WorkflowTaskStatusLink,
            WorkflowTaskSchemaLink,
        ]
    ]


class DependencyLinks(_DependencyLinks):
    @classmethod
    def from_dict(cls: Type[T], kvs: Json, *, infer_missing=False) -> T:
        # from_dict is not supported properly by dataclasses-json because it's a union type.
        # See https://github.com/lidatong/dataclasses-json/issues/222.
        dependency_link = super().from_dict(kvs, infer_missing=infer_missing)
        for i, dependency in enumerate(dependency_link.configuration):
            assert isinstance(dependency, dict)
            if "resourceType" in dependency and dependency["resourceType"] == "workflow_task_schema":
                dependency_link.configuration[i] = WorkflowTaskSchemaLink.from_dict(dependency)
            elif "resourceType" in dependency and dependency["resourceType"] == "workflow_task_status":
                dependency_link.configuration[i] = WorkflowTaskStatusLink.from_dict(dependency)
            if "fieldDefinitions" in dependency:
                dependency_link.configuration[i] = SchemaLink.from_dict(dependency)
            elif "options" in dependency:
                dependency_link.configuration[i] = DropdownLink.from_dict(dependency)
            elif "resourceName" in dependency:
                dependency_link.configuration[i] = NamedResourceLink.from_dict(dependency)
            else:
                dependency_link.configuration[i] = UnnamedResourceLink.from_dict(dependency)
        return dependency_link

    @classmethod
    def from_file(cls: Type[T], file_path: str) -> T:
        with open(file_path) as f:
            contents = f.read()
        return cls.from_json(contents) if contents else cls(configuration=[])

    def to_public_dict(self):
        d = self.to_dict()
        for dep in d.get("configuration", []):
            dep.pop("resourceName", None)
            dep.pop("resourceType", None)
            # Workflow outputs are not yet supported
            dep.pop("output", None)
            subdeps = dep.get("fieldDefinitions") or dep.get("options") or []
            for subdep in subdeps:
                subdep.pop("resourceName", None)
                dep.pop("resourceType", None)
        return d
