from marshmallow import Schema, fields

__author__ = "Noah Hummel"

class LtiRequestSchema(Schema):
    oauth_consumer_key = fields.String(required=True)
    user_id = fields.String(required=True)

    context_id = fields.String()
    context_label = fields.String()
    context_title = fields.String()
    launch_presentation_locale = fields.String()
    launch_presentation_return_url = fields.String()
    lis_person_contact_email_primary = fields.String()
    lis_person_name_family = fields.String()
    lis_person_name_full = fields.String()
    lis_person_name_given = fields.String()
    resource_link_description = fields.String()
    resource_link_title = fields.String()
    tool_consumer_info_product_family_code = fields.String()
    tool_consumer_info_version = fields.String()
    tool_consumer_instance_description = fields.String()
    tool_consumer_instance_guid = fields.String()
