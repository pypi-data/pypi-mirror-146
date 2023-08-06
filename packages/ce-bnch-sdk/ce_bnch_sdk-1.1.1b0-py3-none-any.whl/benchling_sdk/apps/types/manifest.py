from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
from typing import ClassVar, List, Optional, Type, TypeVar, Union

from dataclasses_json import dataclass_json
from dataclasses_jsonschema import JsonSchemaMixin
from dataclasses_jsonschema.type_defs import JsonDict
from typing_extensions import Literal
import yaml

from benchling_sdk.apps.helpers.case_conversion import to_pascal_case, to_snake_case
from benchling_sdk.models import (
    AaSequence,
    AssayResult,
    AssayRun,
    Box,
    Container,
    CustomEntity,
    DnaSequence,
    Entry,
    Location,
    Mixture,
    Plate,
    Request,
    WorkflowTask,
)


class NamedResourceType(str, Enum):
    AA_SEQUENCE = "aa_sequence"
    BOX = "box"
    CONTAINER = "container"
    CUSTOM_ENTITY = "custom_entity"
    DNA_ALIGNMENT = "dna_alignment"  # Cannot be auto-linked because there is no SDK support
    DNA_OLIGO = "dna_oligo"  # Cannot be auto-linked because there is no SDK support
    DNA_SEQUENCE = "dna_sequence"
    ENTRY = "entry"
    FOLDER = "folder"
    LABEL_PRINTER = "label_printer"
    LABEL_TEMPLATE = "label_template"
    LOCATION = "location"
    MIXTURE = "mixture"
    PLATE = "plate"
    PROJECT = "project"
    REGISTRY = "registry"


class UnnamedResourceType(str, Enum):
    ASSAY_RESULT = "assay_result"
    ASSAY_RUN = "assay_run"
    AUTOMATION_INPUT_GENERATOR = "automation_input_generator"
    AUTOMATION_OUTPUT_PROCESSOR = "automation_output_processor"
    BLOB = "blob"
    REQUEST = "request"


AUTOLINKED_RESOURCE_TYPES = [
    NamedResourceType.AA_SEQUENCE,
    NamedResourceType.BOX,
    NamedResourceType.CONTAINER,
    NamedResourceType.CUSTOM_ENTITY,
    NamedResourceType.DNA_SEQUENCE,
    NamedResourceType.ENTRY,
    NamedResourceType.FOLDER,
    NamedResourceType.LABEL_PRINTER,
    NamedResourceType.LABEL_TEMPLATE,
    NamedResourceType.LOCATION,
    NamedResourceType.MIXTURE,
    NamedResourceType.PLATE,
    NamedResourceType.PROJECT,
    NamedResourceType.REGISTRY,
]


class SchemaType(str, Enum):
    ENTITY_SCHEMA = "entity_schema"
    CONTAINER_SCHEMA = "container_schema"
    PLATE_SCHEMA = "plate_schema"
    BOX_SCHEMA = "box_schema"
    LOCATION_SCHEMA = "location_schema"
    ASSAY_RESULT_SCHEMA = "result_schema"
    ASSAY_RUN_SCHEMA = "run_schema"
    REQUEST_SCHEMA = "request_schema"
    TASK_SCHEMA = "task_schema"
    ENTRY_SCHEMA = "entry_schema"
    WORKFLOW_TASK_SCHEMA = "workflow_task_schema"


SCHEMA_TYPE_TO_INSTANCE = {
    SchemaType.CONTAINER_SCHEMA: Container,
    SchemaType.PLATE_SCHEMA: Plate,
    SchemaType.BOX_SCHEMA: Box,
    SchemaType.LOCATION_SCHEMA: Location,
    SchemaType.ASSAY_RESULT_SCHEMA: AssayResult,
    SchemaType.ASSAY_RUN_SCHEMA: AssayRun,
    SchemaType.REQUEST_SCHEMA: Request,
    SchemaType.ENTRY_SCHEMA: Entry,
    SchemaType.WORKFLOW_TASK_SCHEMA: WorkflowTask,
}


SCHEMA_TYPE_TO_SERVICE_NAME = {
    SchemaType.CONTAINER_SCHEMA: "inventory.containers",
    SchemaType.PLATE_SCHEMA: "inventory.plates",
    SchemaType.BOX_SCHEMA: "inventory.boxes",
    SchemaType.LOCATION_SCHEMA: "inventory.locations",
    SchemaType.ASSAY_RESULT_SCHEMA: "assay_results",
    SchemaType.ASSAY_RUN_SCHEMA: "assay_runs",
    SchemaType.REQUEST_SCHEMA: "requests",
    SchemaType.ENTRY_SCHEMA: "notebook",
    SchemaType.WORKFLOW_TASK_SCHEMA: "workflow_tasks",
}


class EntityType(str, Enum):
    AA_SEQUENCE = "aa_sequence"
    CUSTOM_ENTITY = "custom_entity"
    DNA_SEQUENCE = "dna_sequence"
    MIXTURE = "mixture"


ENTITY_TYPE_TO_INSTANCE = {
    EntityType.AA_SEQUENCE: AaSequence,
    EntityType.CUSTOM_ENTITY: CustomEntity,
    EntityType.DNA_SEQUENCE: DnaSequence,
    EntityType.MIXTURE: Mixture,
}

ENTITY_TYPE_TO_SERVICE_NAME = {
    EntityType.AA_SEQUENCE: "aa_sequences",
    EntityType.CUSTOM_ENTITY: "custom_entities",
    EntityType.DNA_SEQUENCE: "dna_sequences",
    EntityType.MIXTURE: "mixtures",
}


@dataclass_json
class ManifestComponent(JsonSchemaMixin):
    pass


class NamedManifestComponent(ManifestComponent):
    name: str

    @property
    def pascal_case_name(self) -> str:
        return to_pascal_case(self.name)

    @property
    def snake_case_name(self) -> str:
        return to_snake_case(self.name)


@dataclass
class BaseDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    name: str
    description: Optional[str] = ""
    is_resource_named: ClassVar[bool] = True


@dataclass
class SchemaDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    """
    Entity schemas are represented separately as `EntitySchemaDependency`.

    Workflow task schemas are represented separately as `WorkflowTaskSchemaDependency`.
    """

    # Unfortunately dataclasses-jsonschema does not support inheritance with `allow_additional_props=False`.
    name: str
    # Exclude workflow task schemas which are special for having 2 different sets of fields
    type: Union[
        Literal[SchemaType.ENTITY_SCHEMA],
        Literal[SchemaType.CONTAINER_SCHEMA],
        Literal[SchemaType.PLATE_SCHEMA],
        Literal[SchemaType.BOX_SCHEMA],
        Literal[SchemaType.LOCATION_SCHEMA],
        Literal[SchemaType.ASSAY_RESULT_SCHEMA],
        Literal[SchemaType.ASSAY_RUN_SCHEMA],
        Literal[SchemaType.REQUEST_SCHEMA],
        Literal[SchemaType.TASK_SCHEMA],
        Literal[SchemaType.ENTRY_SCHEMA],
    ]
    description: Optional[str] = ""
    fieldDefinitions: List[BaseDependency] = field(default_factory=list)
    is_resource_named: ClassVar[bool] = True

    @property
    def instance_pascal_case_name(self) -> str:
        return SCHEMA_TYPE_TO_INSTANCE[self.type].__name__

    @property
    def instance_snake_case_name(self) -> str:
        return to_snake_case(self.instance_pascal_case_name)

    @property
    def service_name(self) -> str:
        return SCHEMA_TYPE_TO_SERVICE_NAME[self.type]


@dataclass
class EntitySchemaResourceProperties(ManifestComponent, allow_additional_props=False):  # type: ignore
    type: EntityType


@dataclass
class EntitySchemaDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    # Unfortunately dataclasses-jsonschema does not support inheritance with `allow_additional_props=False`.
    name: str
    type: Literal[SchemaType.ENTITY_SCHEMA]
    resourceProperties: EntitySchemaResourceProperties
    description: Optional[str] = ""
    fieldDefinitions: List[BaseDependency] = field(default_factory=list)
    is_resource_named: ClassVar[bool] = True

    @property
    def instance_pascal_case_name(self) -> str:
        return ENTITY_TYPE_TO_INSTANCE[self.resourceProperties.type].__name__

    @property
    def instance_snake_case_name(self) -> str:
        return to_snake_case(self.instance_pascal_case_name)

    @property
    def service_name(self) -> str:
        return ENTITY_TYPE_TO_SERVICE_NAME[self.resourceProperties.type]


@dataclass
class DropdownDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    # Unfortunately dataclasses-jsonschema does not support inheritance with `allow_additional_props=False`.
    name: str
    type: Literal["dropdown"]
    description: Optional[str] = ""
    options: List[BaseDependency] = field(default_factory=list)
    is_resource_named: ClassVar[bool] = True


@dataclass
class _WorkflowTaskSchemaOutput(ManifestComponent, allow_additional_props=False):  # type: ignore
    fieldDefinitions: List[BaseDependency] = field(default_factory=list)


@dataclass
class WorkflowTaskSchemaDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore

    # Unfortunately dataclasses-jsonschema does not support inheritance with `allow_additional_props=False`.
    name: str
    type: Literal[SchemaType.WORKFLOW_TASK_SCHEMA]
    description: Optional[str] = ""
    fieldDefinitions: List[BaseDependency] = field(default_factory=list)
    is_resource_named: ClassVar[bool] = True
    output: Optional[_WorkflowTaskSchemaOutput] = None


@dataclass
class WorkflowTaskStatusDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    # Unfortunately dataclasses-jsonschema does not support inheritance with `allow_additional_props=False`.
    name: str
    type: Literal["workflow_task_status"]
    description: Optional[str] = ""
    is_resource_named: ClassVar[bool] = True


@dataclass
class NamedResourceDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    # Unfortunately dataclasses-jsonschema does not support inheritance with `allow_additional_props=False`.
    name: str
    type: NamedResourceType
    description: Optional[str] = ""
    is_resource_named: ClassVar[bool] = True


@dataclass
class UnnamedResourceDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    # Unfortunately dataclasses-jsonschema does not support inheritance with `allow_additional_props=False`.
    name: str  # The dependency still has a name, but the resource itself does not.
    type: UnnamedResourceType
    description: Optional[str] = ""
    is_resource_named: ClassVar[bool] = False


@dataclass
class ManifestInfo(ManifestComponent, allow_additional_props=False):  # type: ignore
    name: str
    version: str
    description: Optional[str] = ""


Dependency = Union[
    SchemaDependency,
    EntitySchemaDependency,
    DropdownDependency,
    NamedResourceDependency,
    UnnamedResourceDependency,
    WorkflowTaskStatusDependency,
    WorkflowTaskSchemaDependency,
]


@dataclass
class _Manifest(ManifestComponent, allow_additional_props=False):  # type: ignore
    manifestVersion: Literal[1]
    info: ManifestInfo
    configuration: Optional[List[Dependency]]


T = TypeVar("T", bound="Manifest")


class Manifest(_Manifest):
    @classmethod
    def from_dict(cls: Type[T], data: JsonDict, validate=True, validate_enums: bool = True) -> T:  # type: ignore
        # from_dict is not supported properly by dataclasses-json because it's a union type.
        # See https://github.com/lidatong/dataclasses-json/issues/222.
        manifest = super().from_dict(data)
        if manifest.configuration:
            for i, dependency in enumerate(manifest.configuration):
                assert isinstance(dependency, dict)
                if dependency["type"] == "dropdown":
                    manifest.configuration[i] = DropdownDependency.from_dict(dependency)
                elif dependency["type"] == SchemaType.WORKFLOW_TASK_SCHEMA:
                    manifest.configuration[i] = WorkflowTaskSchemaDependency.from_dict(dependency)
                elif dependency["type"] == SchemaType.ENTITY_SCHEMA:
                    manifest.configuration[i] = EntitySchemaDependency.from_dict(dependency)
                elif dependency["type"] == "workflow_task_status":
                    manifest.configuration[i] = WorkflowTaskStatusDependency.from_dict(dependency)
                elif dependency["type"] in [schema_type.value for schema_type in SchemaType]:
                    manifest.configuration[i] = SchemaDependency.from_dict(dependency)
                elif dependency["type"] in [resource_type.value for resource_type in NamedResourceType]:
                    manifest.configuration[i] = NamedResourceDependency.from_dict(dependency)
                else:
                    manifest.configuration[i] = UnnamedResourceDependency.from_dict(dependency)
        return manifest

    @classmethod
    def from_file(cls: Type[T], file_path: str) -> T:
        with open(file_path) as f:
            manifest_yaml = f.read()
        manifest_dict = yaml.load(manifest_yaml, Loader=yaml.SafeLoader)
        return cls.from_dict(manifest_dict)

    def to_public_json(self):
        d = self.to_dict()
        dependencies = d.get("configuration") or []
        for dep in dependencies:
            # resourceProperties is currently unsupported in the API
            dep.pop("resourceProperties", None)
            # output also isn't supported yet
            dep.pop("output", None)
        return json.dumps(d, ensure_ascii=True)
