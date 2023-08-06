"""Stream type classes for tap-workato."""

from typing import Optional

from singer_sdk import typing as th

from tap_workato.client import WorkatoStream


class ApiCollectionsStream(WorkatoStream):
    """Stream for extracting API Collections."""

    name = "api_collections"
    path = "/api/api_collections"
    primary_keys = ["id"]
    replication_key = None
    current_page = 1
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("version", th.StringType),
        th.Property("url", th.StringType),
        th.Property("api_spec_url", th.StringType),
    ).to_dict()


class ApiClientsStream(WorkatoStream):
    """Stream for extracting API Clients."""

    name = "api_clients"
    path = "/api/api_clients"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()


class ConnectionsStream(WorkatoStream):
    """Stream for extracting Connections."""

    name = "connections"
    path = "/api/connections"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("application", th.StringType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("authorized_at", th.DateTimeType),
        th.Property("authorization_status", th.StringType),
        th.Property("authorization_error", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("external_id", th.IntegerType),
        th.Property("folder_id", th.IntegerType),
        th.Property("parent_id", th.IntegerType),
    ).to_dict()


class FoldersStream(WorkatoStream):
    """Stream for extracting Folders."""

    name = "folders"
    path = "/api/folders"
    primary_keys = ["id"]
    replication_key = None
    current_page = 1
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("parent_id", th.IntegerType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()


class RecipesStream(WorkatoStream):
    """Stream for extracting recipes."""

    name = "recipes"
    path = "/api/recipes"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.items[*]"
    current_page = 1
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("user_id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("copy_count", th.IntegerType),
        th.Property("trigger_application", th.StringType),
        th.Property("action_applications", th.ArrayType(th.StringType)),
        th.Property("applications", th.ArrayType(th.StringType)),
        th.Property("description", th.StringType),
        th.Property("parameters_schema", th.ArrayType(th.StringType)),
        th.Property("parameters", th.ObjectType()),
        th.Property("folder_id", th.IntegerType),
        th.Property("running", th.BooleanType),
        th.Property("job_succeeded_count", th.IntegerType),
        th.Property("job_failed_count", th.IntegerType),
        th.Property("lifetime_task_count", th.IntegerType),
        th.Property("last_run_at", th.DateTimeType),
        th.Property("stopped_at", th.DateTimeType),
        th.Property("version_no", th.IntegerType),
        th.Property("webhook_url", th.StringType),
        th.Property("stop_cause", th.StringType),
        th.Property("code", th.StringType),
        th.Property(
            "config",
            th.ArrayType(
                th.ObjectType(
                    th.Property("keyword", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("provider", th.StringType),
                    th.Property("skip_validation", th.BooleanType),
                    th.Property("account_id", th.IntegerType),
                )
            ),
        ),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"recipe_id": record["id"]}


class JobsStream(WorkatoStream):
    """Stream for extracting Jobs."""

    name = "jobs"
    path = "/api/recipes/{recipe_id}/jobs"
    primary_keys = ["recipe_id"]
    replication_key = None
    parent_stream_type = RecipesStream
    schema = th.PropertiesList(
        th.Property("recipe_id", th.IntegerType),
        th.Property("job_succeeded_count", th.IntegerType),
        th.Property("job_failed_count", th.IntegerType),
        th.Property("job_count", th.IntegerType),
        th.Property(
            "items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("flow_run_id", th.IntegerType),
                    th.Property("completed_at", th.DateTimeType),
                    th.Property("started_at", th.DateTimeType),
                    th.Property("title", th.StringType),
                    th.Property("is_poll_error", th.BooleanType),
                    th.Property("error", th.StringType),
                    th.Property("is_error", th.BooleanType),
                    th.Property(
                        "error_parts",
                        th.ObjectType(
                            th.Property("adapter", th.StringType),
                            th.Property("error_type", th.StringType),
                            th.Property("message", th.StringType),
                            th.Property("error_id", th.StringType),
                            th.Property("error_at", th.DateTimeType),
                            th.Property("input", th.StringType),
                            th.Property("inner_message", th.StringType),
                        ),
                    ),
                )
            ),
        ),
    ).to_dict()

    def post_process(  # type: ignore[override]
        self, row: dict, context: dict
    ) -> Optional[dict]:
        """As needed, append or transform raw data to match expected structure."""
        row["recipe_id"] = context["recipe_id"]
        return row


class OnPremGroupsStream(WorkatoStream):
    """Stream for extracting On-prem Groups."""

    name = "on_prem_groups"
    path = "/api/on_prem_groups"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("created_at", th.DateTimeType),
    ).to_dict()


class OnPremAgentsStream(WorkatoStream):
    """Stream for extracting On-prem Agents."""

    name = "on_prem_agents"
    path = "/api/on_prem_agents"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("on_prem_group_id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("cn", th.StringType),
        th.Property("os", th.StringType),
        th.Property("awaiting_setup", th.BooleanType),
        th.Property("enabled", th.BooleanType),
    ).to_dict()


class RolesStream(WorkatoStream):
    """Stream for extracting Custom Roles."""

    name = "roles"
    path = "/api/roles"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("inheritable", th.BooleanType),
        th.Property("folder_ids", th.ArrayType(th.IntegerType)),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()


# Streams For Managed Users / Customer Account
class CustomerAccountsStream(WorkatoStream):
    """Stream for extracting Managed Users or Customer Accounts."""

    name = "customer_accounts"
    path = "/api/managed_users"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.result[*]"
    current_page = 1
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("external_id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("notification_email", th.StringType),
        th.Property("error_notification_emails", th.StringType),
        th.Property("admin_notification_emails", th.StringType),
        th.Property("whitelisted_apps", th.ArrayType(th.StringType)),
        th.Property("plan_id", th.StringType),
        th.Property("origin_url", th.StringType),
        th.Property("frame_ancestors", th.StringType),
        th.Property("trial", th.BooleanType),
        th.Property("in_trial", th.BooleanType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("current_billing_period_start", th.DateTimeType),
        th.Property("current_billing_period_end", th.DateTimeType),
        th.Property("task_limit_adjustment", th.StringType),
        th.Property("task_limit", th.IntegerType),
        th.Property("task_count", th.IntegerType),
        th.Property("active_connection_limit", th.IntegerType),
        th.Property("active_connection_count", th.IntegerType),
        th.Property("active_recipe_count", th.IntegerType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"customer_account_id": record["id"]}


class CustomerChildStreams(WorkatoStream):
    """Parent Stream for all children to the CustomerAccountsStream for DRY code."""

    parent_stream_type = CustomerAccountsStream
    primary_keys = ["customer_account_id", "id"]
    replication_key = None

    def post_process(  # type: ignore[override]
        self, row: dict, context: dict
    ) -> Optional[dict]:
        """As needed, append or transform raw data to match expected structure."""
        row["customer_account_id"] = context["customer_account_id"]
        return row


class CustomerMembersStream(CustomerChildStreams):
    """Stream for extracting customers' connections."""

    name = "customer_members"
    path = "/api/managed_users/{customer_account_id}/members"
    schema = th.PropertiesList(
        th.Property("customer_account_id", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("grant_type", th.StringType),
        th.Property("role_name", th.StringType),
        th.Property("external_id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("email", th.StringType),
        th.Property("time_zone", th.StringType),
    ).to_dict()


class CustomerConnectionsStream(CustomerChildStreams):
    """Stream for extracting customers' connections."""

    name = "customer_connections"
    path = "/api/managed_users/{customer_account_id}/connections"
    records_jsonpath = "$.result[*]"
    schema = th.PropertiesList(
        th.Property("customer_account_id", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("provider", th.StringType),
        th.Property("authorized_at", th.DateTimeType),
        th.Property("authorization_status", th.StringType),
        th.Property("authorization_error", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("external_id", th.StringType),
        th.Property("folder_id", th.IntegerType),
        th.Property("parent_id", th.IntegerType),
    ).to_dict()


class CustomerFoldersStream(CustomerChildStreams):
    """Stream for extracting customers' folders."""

    name = "customer_folders"
    path = "/api/managed_users/{customer_account_id}/folders"
    records_jsonpath = "$.result[*]"
    current_page = 1
    schema = th.PropertiesList(
        th.Property("customer_account_id", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("parent_id", th.IntegerType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()


class CustomerRecipesStream(CustomerChildStreams):
    """Stream for extracting customers' recipes."""

    name = "customer_recipes"
    path = "/api/managed_users/{customer_account_id}/recipes"
    records_jsonpath = "$.result[*]"
    current_page = 1
    schema = th.PropertiesList(
        th.Property("customer_account_id", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("user_id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("copy_count", th.IntegerType),
        th.Property("trigger_application", th.StringType),
        th.Property("action_applications", th.ArrayType(th.StringType)),
        th.Property("applications", th.ArrayType(th.StringType)),
        th.Property("description", th.StringType),
        th.Property("parameters_schema", th.ArrayType(th.StringType)),
        th.Property("parameters", th.ObjectType()),
        th.Property("folder_id", th.IntegerType),
        th.Property("running", th.BooleanType),
        th.Property("job_succeeded_count", th.IntegerType),
        th.Property("job_failed_count", th.IntegerType),
        th.Property("lifetime_task_count", th.IntegerType),
        th.Property("last_run_at", th.DateTimeType),
        th.Property("stopped_at", th.DateTimeType),
        th.Property("version_no", th.IntegerType),
        th.Property("webhook_url", th.StringType),
        th.Property("stop_cause", th.StringType),
        th.Property("code", th.StringType),
        th.Property(
            "config",
            th.ArrayType(
                th.ObjectType(
                    th.Property("keyword", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("provider", th.StringType),
                    th.Property("skip_validation", th.BooleanType),
                    th.Property("account_id", th.IntegerType),
                )
            ),
        ),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "customer_account_id": record["customer_account_id"],
            "recipe_id": record["id"],
        }


# not currently possible to hit this endpoint for managed users' recipes
# class CustomerJobsStream(CustomerChildStreams):
#     """Stream for extracting Jobs."""
#
#     name = "customer_jobs"
#     path = "/api/recipes/{recipe_id}/jobs"
#     primary_keys = ["customer_account_id", "recipe_id"]
#     replication_key = None
#     parent_stream_type = CustomerRecipesStream
#     schema = th.PropertiesList(
#         th.Property("customer_account_id", th.IntegerType),
#         th.Property("recipe_id", th.IntegerType),
#         th.Property("job_succeeded_count", th.IntegerType),
#         th.Property("job_failed_count", th.IntegerType),
#         th.Property("job_count", th.IntegerType),
#         th.Property(
#             "items",
#             th.ArrayType(
#                 th.ObjectType(
#                     th.Property("id", th.IntegerType),
#                     th.Property("flow_run_id", th.IntegerType),
#                     th.Property("completed_at", th.DateTimeType),
#                     th.Property("started_at", th.DateTimeType),
#                     th.Property("title", th.StringType),
#                     th.Property("is_poll_error", th.BooleanType),
#                     th.Property("error", th.StringType),
#                     th.Property("is_error", th.BooleanType),
#                     th.Property(
#                         "error_parts",
#                         th.ObjectType(
#                             th.Property("adapter", th.StringType),
#                             th.Property("error_type", th.StringType),
#                             th.Property("message", th.StringType),
#                             th.Property("error_id", th.StringType),
#                             th.Property("error_at", th.DateTimeType),
#                             th.Property("input", th.StringType),
#                             th.Property("inner_message", th.StringType),
#                         ),
#                     ),
#                 )
#             ),
#         ),
#     ).to_dict()
#
#     def post_process(self, row: dict, context: dict) -> Optional[dict]:
#         """As needed, append or transform raw data to match expected structure."""
#         row["customer_account_id"] = context["customer_account_id"]
#         row["recipe_id"] = context["recipe_id"]
#         return row


class CustomerApiCollectionsStream(CustomerChildStreams):
    """Stream for extracting customers' folders."""

    name = "customer_api_collections"
    path = "/api/managed_users/{customer_account_id}/api_collections"
    records_jsonpath = "$.result[*]"
    schema = th.PropertiesList(
        th.Property("customer_account_id", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("version", th.StringType),
        th.Property("url", th.StringType),
        th.Property("api_spec_url", th.StringType),
    ).to_dict()


class CustomerApiEndpointsStream(CustomerChildStreams):
    """Stream for extracting customers' folders."""

    name = "customer_api_endpoints"
    path = "/api/managed_users/{customer_account_id}/api_endpoints"
    records_jsonpath = "$.result[*]"
    schema = th.PropertiesList(
        th.Property("customer_account_id", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("api_collection_id", th.IntegerType),
        th.Property("flow_id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("method", th.StringType),
        th.Property("url", th.StringType),
        th.Property("legacy_url", th.StringType),
        th.Property("base_path", th.StringType),
        th.Property("path", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("legacy", th.BooleanType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()


class CustomerApiClientsStream(CustomerChildStreams):
    """Stream for extracting customers' folders."""

    name = "customer_api_clients"
    path = "/api/managed_users/{customer_account_id}/api_clients"
    records_jsonpath = "$.result[*]"
    schema = th.PropertiesList(
        th.Property("customer_account_id", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "customer_account_id": record["customer_account_id"],
            "api_client_id": record["id"],
        }


class CustomerApiAccessProfilesStream(WorkatoStream):
    """Stream for extracting customers' folders."""

    name = "customer_api_access_profiles"
    path = "/api/managed_users/{customer_account_id}/api_access_profiles"
    primary_keys = ["customer_account_id", "api_client_id", "id"]
    replication_key = None
    parent_stream_type = CustomerApiClientsStream
    schema = th.PropertiesList(
        th.Property("customer_account_id", th.IntegerType),
        th.Property("api_client_id", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("external_id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("notification_email", th.StringType),
        th.Property("plan_id", th.StringType),
        th.Property("in_trial", th.BooleanType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()

    def post_process(  # type: ignore[override]
        self, row: dict, context: dict
    ) -> Optional[dict]:
        """As needed, append or transform raw data to match expected structure."""
        row["customer_account_id"] = context["customer_account_id"]
        row["api_client_id"] = context["api_client_id"]
        return row


class CustomerRolesStream(CustomerChildStreams):
    """Stream for extracting customers' folders."""

    name = "customer_roles"
    path = "/api/managed_users/{customer_account_id}/roles"
    schema = th.PropertiesList(
        th.Property("customer_account_id", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("inheritable", th.BooleanType),
        th.Property("folder_ids", th.ArrayType(th.IntegerType)),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()
