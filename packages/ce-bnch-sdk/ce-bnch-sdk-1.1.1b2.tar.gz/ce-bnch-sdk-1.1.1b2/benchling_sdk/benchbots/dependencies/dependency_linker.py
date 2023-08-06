from typing import cast, Union

import typer

from benchling_sdk.benchbots.benchling_store import AllSchemaEmbeddable
from benchling_sdk.benchbots.dependencies.dependency_resolver import DependencyResolver
from benchling_sdk.benchbots.types.dependency_links import (
    DependencyLinks,
    DropdownLink,
    DropdownOptionLink,
    NamedResourceLink,
    SchemaFieldLink,
    SchemaLink,
    UnnamedResourceLink,
    WorkflowTaskOutputSchemaLink,
    WorkflowTaskSchemaLink,
    WorkflowTaskStatusLink,
)
from benchling_sdk.benchbots.types.manifest import (
    AUTOLINKED_RESOURCE_TYPES,
    BaseDependency,
    DropdownDependency,
    EntitySchemaDependency,
    Manifest,
    NamedResourceDependency,
    SchemaDependency,
    UnnamedResourceDependency,
    WorkflowTaskSchemaDependency,
    WorkflowTaskStatusDependency,
)
from benchling_sdk.models import DropdownSummary, WorkflowOutputSchema


class DependencyLinker:
    dependency_resolver: DependencyResolver

    def __init__(self, dependency_resolver: DependencyResolver):
        self.dependency_resolver = dependency_resolver

    def link_dependencies(
        self,
        manifest: Manifest,
    ) -> DependencyLinks:
        dependency_links = DependencyLinks(configuration=[])
        self.update_dependency_links(dependency_links, manifest)
        self.remove_unneeded_dependencies(dependency_links, manifest)
        return dependency_links

    # noinspection PyMethodMayBeStatic
    def remove_unneeded_dependencies(
        self,
        dependency_links: DependencyLinks,
        manifest: Manifest,
    ) -> None:
        dependency_names = (
            [dependency.name for dependency in manifest.configuration] if manifest.configuration else []
        )
        dependency_links.configuration = [
            link for link in dependency_links.configuration if link.name in dependency_names
        ]

    def update_dependency_links(self, dependency_links: DependencyLinks, manifest: Manifest) -> None:
        if manifest.configuration:
            for dependency in manifest.configuration:
                if isinstance(dependency, WorkflowTaskSchemaDependency):
                    dependency_links.configuration.append(self.link_workflow_task_schema(dependency))
                elif isinstance(dependency, WorkflowTaskStatusDependency):
                    dependency_links.configuration.append(self.link_workflow_task_status(dependency))
                elif isinstance(dependency, (SchemaDependency, EntitySchemaDependency)):
                    dependency_links.configuration.append(self.link_schema(dependency))
                elif isinstance(dependency, DropdownDependency):
                    dependency_links.configuration.append(self.link_dropdown(dependency))
                elif isinstance(dependency, NamedResourceDependency):
                    if dependency.type in AUTOLINKED_RESOURCE_TYPES:
                        dependency_links.configuration.append(self.link_resource(dependency))
                    else:
                        resource_id = typer.prompt(
                            f'Dependency "{dependency.name}" cannot be auto-linked '
                            f'because it is of type "{dependency.type}".\n'
                            "Please enter the resource's API ID"
                        )
                        resource_name = typer.prompt("Please enter the resource's name")
                        dependency_links.configuration.append(
                            NamedResourceLink(
                                name=dependency.name,
                                resourceId=resource_id,
                                resourceName=resource_name,
                                type=dependency.type,
                            )
                        )
                elif isinstance(dependency, UnnamedResourceDependency):
                    resource_id = typer.prompt(
                        f'Dependency "{dependency.name}" cannot be auto-linked '
                        f'because it is of type "{dependency.type}".\n'
                        "Please enter the resource's API ID"
                    )
                    dependency_links.configuration.append(
                        UnnamedResourceLink(
                            name=dependency.name,
                            resourceId=resource_id,
                            type=dependency.type,
                        )
                    )
                else:
                    raise NotImplementedError(f"Unsupported dependency={dependency}")

    def link_schema(self, schema_dependency: Union[EntitySchemaDependency, SchemaDependency]) -> SchemaLink:
        schema = self.dependency_resolver.resolve_schema_by_id_or_name(
            schema_dependency=schema_dependency,
            initial_id_or_name=schema_dependency.name,
        )
        schema_fields = (
            [
                self.link_field(schema, field_dependency)
                for field_dependency in schema_dependency.fieldDefinitions
            ]
            if schema_dependency.fieldDefinitions
            else []
        )
        typer.echo(f"Linking {schema_dependency.name} to {schema.id}")
        return SchemaLink(
            name=schema_dependency.name,
            resourceId=schema.id,
            resourceName=cast(str, schema.name),
            type=schema_dependency.type,
            fieldDefinitions=schema_fields,
        )

    def link_workflow_task_status(
        self, workflow_task_status_dependency: WorkflowTaskStatusDependency
    ) -> WorkflowTaskStatusLink:
        workflow_task_status = self.dependency_resolver.resolve_workflow_task_status_by_id_or_name(
            workflow_task_status_dependency=workflow_task_status_dependency,
            initial_id_or_name=workflow_task_status_dependency.name,
        )
        typer.echo(f"Linking {workflow_task_status_dependency.name} to {workflow_task_status.id}")
        return WorkflowTaskStatusLink(
            name=workflow_task_status_dependency.name,
            resourceId=workflow_task_status.id,
            resourceName=cast(str, workflow_task_status.display_name),
            type="workflow_task_status",
        )

    def link_workflow_task_schema(
        self, schema_dependency: WorkflowTaskSchemaDependency
    ) -> WorkflowTaskSchemaLink:
        schema = self.dependency_resolver.resolve_schema_by_id_or_name(
            schema_dependency=schema_dependency,
            initial_id_or_name=schema_dependency.name,
        )
        schema_fields = (
            [
                self.link_field(schema, field_dependency)
                for field_dependency in schema_dependency.fieldDefinitions
            ]
            if schema_dependency.fieldDefinitions
            else []
        )
        if schema_dependency.output and schema_dependency.output.fieldDefinitions:
            output_field_definitions = [
                BaseDependency(name=output_field.name)
                for output_field in schema_dependency.output.fieldDefinitions
            ]
            output_schema = WorkflowOutputSchema(
                name=schema_dependency.name,
                field_definitions=schema.workflow_output_schema.field_definitions,  # type: ignore
            )
            output_schema_fields = [
                self.link_field(output_schema, field_dependency)
                for field_dependency in output_field_definitions
            ]
        else:
            output_schema_fields = []
        typer.echo(f"Linking {schema_dependency.name} to {schema.id}")
        return WorkflowTaskSchemaLink(
            name=schema_dependency.name,
            resourceId=schema.id,
            resourceName=cast(str, schema.name),
            fieldDefinitions=schema_fields,
            output=WorkflowTaskOutputSchemaLink(fieldDefinitions=output_schema_fields),
            type="workflow_task_schema",
        )

    def link_field(self, schema: AllSchemaEmbeddable, field_dependency: BaseDependency) -> SchemaFieldLink:
        field = self.dependency_resolver.resolve_field_by_id_or_name(
            schema=schema,
            initial_id_or_name=field_dependency.name,
            dependency_name=field_dependency.name,
        )
        typer.echo(f"Linking {field_dependency.name} to {field.id}")
        return SchemaFieldLink(
            name=field_dependency.name,
            resourceId=field.id,
            resourceName=cast(str, field.name),
        )

    def link_dropdown(self, dropdown_dependency: DropdownDependency) -> DropdownLink:
        dropdown = self.dependency_resolver.resolve_dropdown_by_id_or_name(
            dropdown_dependency=dropdown_dependency,
            initial_id_or_name=dropdown_dependency.name,
        )
        options = (
            [
                self.link_option(dropdown, option_dependency)
                for option_dependency in dropdown_dependency.options
            ]
            if dropdown_dependency.options
            else []
        )
        typer.echo(f"Linking {dropdown_dependency.name} to {dropdown.id}")
        return DropdownLink(
            name=dropdown_dependency.name,
            resourceId=dropdown.id,
            resourceName=cast(str, dropdown.name),
            type=dropdown_dependency.type,
            options=options,
        )

    def link_option(
        self, parent_dropdown: DropdownSummary, option_dependency: BaseDependency
    ) -> DropdownOptionLink:
        option = self.dependency_resolver.resolve_option_by_id_or_name(
            dropdown=parent_dropdown,
            initial_id_or_name=option_dependency.name,
            dependency_name=option_dependency.name,
        )
        typer.echo(f"Linking {option_dependency.name} to {option.id}")
        return DropdownOptionLink(
            name=option_dependency.name,
            resourceId=option.id,
            resourceName=cast(str, option.name),
        )

    def link_resource(self, resource_dependency: NamedResourceDependency) -> NamedResourceLink:
        resource = self.dependency_resolver.resolve_resource_by_id_or_name(
            resource_dependency=resource_dependency,
            initial_id_or_name=resource_dependency.name,
        )
        typer.echo(f"Linking {resource_dependency.type} {resource_dependency.name} to {resource.id}")
        return NamedResourceLink(
            name=resource_dependency.name,
            resourceId=cast(str, resource.id),
            resourceName=cast(str, resource.name),
            type=resource_dependency.type,
        )
