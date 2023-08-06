# ehelply-python-sdk

Note: This SDK is generated, built, and published automatically by eHelply.

- API version: 1.1.41
- Package version: 1.1.41
For more information, please visit [https://superstack.ehelply.com/support](https://superstack.ehelply.com/support)

## Requirements.

Python >= 3.6

## Installation
### Install from PyPi (Recommended)
```sh
pip install ehelply-python-sdk
```

Then import the package:
```python
import ehelply_python_sdk
```

### Install from repository

```sh
pip install git+https://github.com/eHelply/Python-eHelply-SDK.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/eHelply/Python-eHelply-SDK.git`)

Then import the package:
```python
import ehelply_python_sdk
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import ehelply_python_sdk
```

## Getting Started and Usage

```python

import time
import ehelply-python-sdk
from pprint import pprint
from ehelply-python-sdk.api import auth_api
from ehelply-python-sdk.model.http_validation_error import HTTPValidationError
from ehelply-python-sdk.model.user_password_reset_confirmation import UserPasswordResetConfirmation
# Defining the host is optional and defaults to https://api.prod.ehelply.com
# See configuration.py for a list of all supported configuration parameters.
configuration = ehelply-python-sdk.Configuration(
    host = "https://api.prod.ehelply.com"
)


# Enter a context with an instance of the API client
with ehelply-python-sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = auth_api.AuthApi(api_client)
    user_password_reset_confirmation = UserPasswordResetConfirmation(
        email="email_example",
        confirmation_code="confirmation_code_example",
        password="password_example",
    ) # UserPasswordResetConfirmation

    try:
        # Reset Password Confirmation
        api_response = api_instance.reset_password_confirmation_users_auth_password_reset_confirm_post(user_password_reset_confirmation)
        pprint(api_response)
    except ehelply-python-sdk.ApiException as e:
        print("Exception when calling AuthApi->reset_password_confirmation_users_auth_password_reset_confirm_post: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://api.prod.ehelply.com*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AuthApi* | [**reset_password_confirmation_users_auth_password_reset_confirm_post**](docs/AuthApi.md#reset_password_confirmation_users_auth_password_reset_confirm_post) | **POST** /sam/users/auth/password/reset/confirm | Reset Password Confirmation
*BillingApi* | [**attach_payment_to_project_billing_attach_payment_to_project_post**](docs/BillingApi.md#attach_payment_to_project_billing_attach_payment_to_project_post) | **POST** /sam/billing/attach_payment_to_project | Attach Payment To Project
*BillingApi* | [**attach_payment_to_project_billing_attach_payment_to_project_post_0**](docs/BillingApi.md#attach_payment_to_project_billing_attach_payment_to_project_post_0) | **POST** /sam/billing/attach_payment_to_project | Attach Payment To Project
*BillingApi* | [**create_billing_account_billing_create_billing_account_post**](docs/BillingApi.md#create_billing_account_billing_create_billing_account_post) | **POST** /sam/billing/create_billing_account | Create Billing Account
*BillingApi* | [**create_billing_account_billing_create_billing_account_post_0**](docs/BillingApi.md#create_billing_account_billing_create_billing_account_post_0) | **POST** /sam/billing/create_billing_account | Create Billing Account
*BillingApi* | [**delete_billing_account_billing_delete_billing_account_delete**](docs/BillingApi.md#delete_billing_account_billing_delete_billing_account_delete) | **DELETE** /sam/billing/delete_billing_account | Delete Billing Account
*BillingApi* | [**delete_billing_account_billing_delete_billing_account_delete_0**](docs/BillingApi.md#delete_billing_account_billing_delete_billing_account_delete_0) | **DELETE** /sam/billing/delete_billing_account | Delete Billing Account
*BillingApi* | [**get_client_secret_billing_retrieve_secret_get**](docs/BillingApi.md#get_client_secret_billing_retrieve_secret_get) | **GET** /sam/billing/retrieve_secret | Get Client Secret
*BillingApi* | [**get_client_secret_billing_retrieve_secret_get_0**](docs/BillingApi.md#get_client_secret_billing_retrieve_secret_get_0) | **GET** /sam/billing/retrieve_secret | Get Client Secret
*BillingApi* | [**has_payment_billing_has_payment_get**](docs/BillingApi.md#has_payment_billing_has_payment_get) | **GET** /sam/billing/has_payment | Has Payment
*BillingApi* | [**has_payment_billing_has_payment_get_0**](docs/BillingApi.md#has_payment_billing_has_payment_get_0) | **GET** /sam/billing/has_payment | Has Payment
*BillingApi* | [**process_payment_billing_process_payment_post**](docs/BillingApi.md#process_payment_billing_process_payment_post) | **POST** /sam/billing/process_payment | Process Payment
*BillingApi* | [**process_payment_billing_process_payment_post_0**](docs/BillingApi.md#process_payment_billing_process_payment_post_0) | **POST** /sam/billing/process_payment | Process Payment
*BillingApi* | [**reconcile_payment_methods_billing_reconcile_payment_get**](docs/BillingApi.md#reconcile_payment_methods_billing_reconcile_payment_get) | **GET** /sam/billing/reconcile_payment | Reconcile Payment Methods
*BillingApi* | [**remove_payment_method_billing_remove_payment_method_delete**](docs/BillingApi.md#remove_payment_method_billing_remove_payment_method_delete) | **DELETE** /sam/billing/remove_payment_method | Remove Payment Method
*BillingApi* | [**remove_payment_method_billing_remove_payment_method_delete_0**](docs/BillingApi.md#remove_payment_method_billing_remove_payment_method_delete_0) | **DELETE** /sam/billing/remove_payment_method | Remove Payment Method
*BillingApi* | [**view_payment_method_billing_view_payment_method_get**](docs/BillingApi.md#view_payment_method_billing_view_payment_method_get) | **GET** /sam/billing/view_payment_method | View Payment Method
*BillingApi* | [**view_payment_method_billing_view_payment_method_get_0**](docs/BillingApi.md#view_payment_method_billing_view_payment_method_get_0) | **GET** /sam/billing/view_payment_method | View Payment Method
*LoggingApi* | [**get_logs_logging_logs_get**](docs/LoggingApi.md#get_logs_logging_logs_get) | **GET** /sam/logging/logs | Get Logs
*LoggingApi* | [**get_service_logs_logging_logs_services_service_get**](docs/LoggingApi.md#get_service_logs_logging_logs_services_service_get) | **GET** /sam/logging/logs/services/{service} | Get Service Logs
*LoggingApi* | [**get_subject_logs_logging_logs_services_service_subjects_subject_get**](docs/LoggingApi.md#get_subject_logs_logging_logs_services_service_subjects_subject_get) | **GET** /sam/logging/logs/services/{service}/subjects/{subject} | Get Subject Logs
*MetaApi* | [**delete_meta_from_uuid_meta_meta_meta_uuid_delete**](docs/MetaApi.md#delete_meta_from_uuid_meta_meta_meta_uuid_delete) | **DELETE** /meta/meta/meta/{meta_uuid} | Delete Meta From Uuid
*MetaApi* | [**delete_meta_meta_meta_service_service_type_type_entity_entity_uuid_delete**](docs/MetaApi.md#delete_meta_meta_meta_service_service_type_type_entity_entity_uuid_delete) | **DELETE** /meta/meta/meta/service/{service}/type/{type}/entity/{entity_uuid} | Delete Meta
*MetaApi* | [**get_meta_from_uuid_meta_meta_meta_uuid_get**](docs/MetaApi.md#get_meta_from_uuid_meta_meta_meta_uuid_get) | **GET** /meta/meta/meta/{meta_uuid} | Get Meta From Uuid
*MetaApi* | [**get_meta_meta_meta_service_service_type_type_entity_entity_uuid_get**](docs/MetaApi.md#get_meta_meta_meta_service_service_type_type_entity_entity_uuid_get) | **GET** /meta/meta/meta/service/{service}/type/{type}/entity/{entity_uuid} | Get Meta
*MetaApi* | [**make_slug_meta_meta_slug_post**](docs/MetaApi.md#make_slug_meta_meta_slug_post) | **POST** /meta/meta/meta/slug | Make Slug
*MetaApi* | [**post_meta_meta_meta_service_service_type_type_str_entity_entity_uuid_post**](docs/MetaApi.md#post_meta_meta_meta_service_service_type_type_str_entity_entity_uuid_post) | **POST** /meta/meta/meta/service/{service}/type/{type_str}/entity/{entity_uuid} | Post Meta
*MetaApi* | [**touch_meta_meta_meta_service_service_type_type_entity_entity_uuid_touch_post**](docs/MetaApi.md#touch_meta_meta_meta_service_service_type_type_entity_entity_uuid_touch_post) | **POST** /meta/meta/meta/service/{service}/type/{type}/entity/{entity_uuid}/touch | Touch Meta
*MetaApi* | [**update_meta_from_uuid_meta_meta_meta_uuid_put**](docs/MetaApi.md#update_meta_from_uuid_meta_meta_meta_uuid_put) | **PUT** /meta/meta/meta/{meta_uuid} | Update Meta From Uuid
*MetaApi* | [**update_meta_meta_meta_service_service_type_type_entity_entity_uuid_put**](docs/MetaApi.md#update_meta_meta_meta_service_service_type_type_entity_entity_uuid_put) | **PUT** /meta/meta/meta/service/{service}/type/{type}/entity/{entity_uuid} | Update Meta
*MonitorApi* | [**ack_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_acknowledge_post**](docs/MonitorApi.md#ack_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_acknowledge_post) | **POST** /sam/monitor/services/{service}/stages/{stage}/alarms/{alarm_uuid}/acknowledge | Ack Alarm
*MonitorApi* | [**assign_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_assign_post**](docs/MonitorApi.md#assign_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_assign_post) | **POST** /sam/monitor/services/{service}/stages/{stage}/alarms/{alarm_uuid}/assign | Assign Alarm
*MonitorApi* | [**attach_alarm_note_monitor_services_service_stages_stage_alarms_alarm_uuid_note_post**](docs/MonitorApi.md#attach_alarm_note_monitor_services_service_stages_stage_alarms_alarm_uuid_note_post) | **POST** /sam/monitor/services/{service}/stages/{stage}/alarms/{alarm_uuid}/note | Attach Alarm Note
*MonitorApi* | [**attach_alarm_ticket_monitor_services_service_stages_stage_alarms_alarm_uuid_ticket_post**](docs/MonitorApi.md#attach_alarm_ticket_monitor_services_service_stages_stage_alarms_alarm_uuid_ticket_post) | **POST** /sam/monitor/services/{service}/stages/{stage}/alarms/{alarm_uuid}/ticket | Attach Alarm Ticket
*MonitorApi* | [**clear_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_clear_post**](docs/MonitorApi.md#clear_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_clear_post) | **POST** /sam/monitor/services/{service}/stages/{stage}/alarms/{alarm_uuid}/clear | Clear Alarm
*MonitorApi* | [**get_service_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_get**](docs/MonitorApi.md#get_service_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_get) | **GET** /sam/monitor/services/{service}/stages/{stage}/alarms/{alarm_uuid} | Get Service Alarm
*MonitorApi* | [**get_service_alarms_monitor_services_service_stages_stage_alarms_get**](docs/MonitorApi.md#get_service_alarms_monitor_services_service_stages_stage_alarms_get) | **GET** /sam/monitor/services/{service}/stages/{stage}/alarms | Get Service Alarms
*MonitorApi* | [**get_service_heartbeats_monitor_services_service_stages_stage_heartbeats_get**](docs/MonitorApi.md#get_service_heartbeats_monitor_services_service_stages_stage_heartbeats_get) | **GET** /sam/monitor/services/{service}/stages/{stage}/heartbeats | Get Service Heartbeats
*MonitorApi* | [**get_service_kpis_monitor_services_service_kpis_get**](docs/MonitorApi.md#get_service_kpis_monitor_services_service_kpis_get) | **GET** /sam/monitor/services/{service}/kpis | Get Service Kpis
*MonitorApi* | [**get_service_monitor_services_service_get**](docs/MonitorApi.md#get_service_monitor_services_service_get) | **GET** /sam/monitor/services/{service} | Get Service
*MonitorApi* | [**get_service_spec**](docs/MonitorApi.md#get_service_spec) | **GET** /sam/monitor/services/{service}/specs/{spec} | Getservicespec
*MonitorApi* | [**get_service_specs**](docs/MonitorApi.md#get_service_specs) | **GET** /sam/monitor/services/{service}/specs | Getservicespecs
*MonitorApi* | [**get_service_vitals_monitor_services_service_stages_stage_vitals_get**](docs/MonitorApi.md#get_service_vitals_monitor_services_service_stages_stage_vitals_get) | **GET** /sam/monitor/services/{service}/stages/{stage}/vitals | Get Service Vitals
*MonitorApi* | [**get_services_monitor_services_get**](docs/MonitorApi.md#get_services_monitor_services_get) | **GET** /sam/monitor/services | Get Services
*MonitorApi* | [**get_services_with_specs**](docs/MonitorApi.md#get_services_with_specs) | **GET** /sam/monitor/specs/services | Getserviceswithspecs
*MonitorApi* | [**hide_service_monitor_services_service_stages_stage_hide_post**](docs/MonitorApi.md#hide_service_monitor_services_service_stages_stage_hide_post) | **POST** /sam/monitor/services/{service}/stages/{stage}/hide | Hide Service
*MonitorApi* | [**ignore_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_ignore_post**](docs/MonitorApi.md#ignore_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_ignore_post) | **POST** /sam/monitor/services/{service}/stages/{stage}/alarms/{alarm_uuid}/ignore | Ignore Alarm
*MonitorApi* | [**register_service_monitor_services_post**](docs/MonitorApi.md#register_service_monitor_services_post) | **POST** /sam/monitor/services | Register Service
*MonitorApi* | [**search_alarms_monitor_services_service_alarms_get**](docs/MonitorApi.md#search_alarms_monitor_services_service_alarms_get) | **GET** /sam/monitor/services/{service}/alarms | Search Alarms
*MonitorApi* | [**show_service_monitor_services_service_stages_stage_show_post**](docs/MonitorApi.md#show_service_monitor_services_service_stages_stage_show_post) | **POST** /sam/monitor/services/{service}/stages/{stage}/show | Show Service
*MonitorApi* | [**terminate_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_terminate_post**](docs/MonitorApi.md#terminate_alarm_monitor_services_service_stages_stage_alarms_alarm_uuid_terminate_post) | **POST** /sam/monitor/services/{service}/stages/{stage}/alarms/{alarm_uuid}/terminate | Terminate Alarm
*MonitorApi* | [**trigger_alarm_monitor_services_service_stages_stage_alarms_post**](docs/MonitorApi.md#trigger_alarm_monitor_services_service_stages_stage_alarms_post) | **POST** /sam/monitor/services/{service}/stages/{stage}/alarms | Trigger Alarm
*NotesApi* | [**create_note_notes_notes_post**](docs/NotesApi.md#create_note_notes_notes_post) | **POST** /notes/notes/notes | Create Note
*NotesApi* | [**delete_note_notes_notes_note_id_delete**](docs/NotesApi.md#delete_note_notes_notes_note_id_delete) | **DELETE** /notes/notes/notes/{note_id} | Delete Note
*NotesApi* | [**get_note_notes_notes_note_id_get**](docs/NotesApi.md#get_note_notes_notes_note_id_get) | **GET** /notes/notes/notes/{note_id} | Get Note
*NotesApi* | [**update_note_notes_notes_note_id_put**](docs/NotesApi.md#update_note_notes_notes_note_id_put) | **PUT** /notes/notes/notes/{note_id} | Update Note
*ProjectsApi* | [**add_member_to_project_projects_projects_project_uuid_members_entity_uuid_post**](docs/ProjectsApi.md#add_member_to_project_projects_projects_project_uuid_members_entity_uuid_post) | **POST** /sam/projects/projects/{project_uuid}/members/{entity_uuid} | Add Member To Project
*ProjectsApi* | [**archive_project_projects_projects_project_uuid_delete**](docs/ProjectsApi.md#archive_project_projects_projects_project_uuid_delete) | **DELETE** /sam/projects/projects/{project_uuid} | Archive Project
*ProjectsApi* | [**create_project_key_projects_projects_project_uuid_keys_post**](docs/ProjectsApi.md#create_project_key_projects_projects_project_uuid_keys_post) | **POST** /sam/projects/projects/{project_uuid}/keys | Create Project Key
*ProjectsApi* | [**create_project_projects_projects_post**](docs/ProjectsApi.md#create_project_projects_projects_post) | **POST** /sam/projects/projects | Create Project
*ProjectsApi* | [**create_usage_type_projects_usage_types_post**](docs/ProjectsApi.md#create_usage_type_projects_usage_types_post) | **POST** /sam/projects/usage/types | Create Usage Type
*ProjectsApi* | [**delete_usage_type_projects_usage_types_usage_type_key_delete**](docs/ProjectsApi.md#delete_usage_type_projects_usage_types_usage_type_key_delete) | **DELETE** /sam/projects/usage/types/{usage_type_key} | Delete Usage Type
*ProjectsApi* | [**get_all_project_usage_projects_projects_project_uuid_usage_get**](docs/ProjectsApi.md#get_all_project_usage_projects_projects_project_uuid_usage_get) | **GET** /sam/projects/projects/{project_uuid}/usage | Get All Project Usage
*ProjectsApi* | [**get_member_projects_projects_members_entity_uuid_projects_get**](docs/ProjectsApi.md#get_member_projects_projects_members_entity_uuid_projects_get) | **GET** /sam/projects/members/{entity_uuid}/projects | Get Member Projects
*ProjectsApi* | [**get_project_keys_projects_projects_project_uuid_keys_get**](docs/ProjectsApi.md#get_project_keys_projects_projects_project_uuid_keys_get) | **GET** /sam/projects/projects/{project_uuid}/keys | Get Project Keys
*ProjectsApi* | [**get_project_members_projects_projects_project_uuid_members_get**](docs/ProjectsApi.md#get_project_members_projects_projects_project_uuid_members_get) | **GET** /sam/projects/projects/{project_uuid}/members | Get Project Members
*ProjectsApi* | [**get_project_projects_projects_project_uuid_get**](docs/ProjectsApi.md#get_project_projects_projects_project_uuid_get) | **GET** /sam/projects/projects/{project_uuid} | Get Project
*ProjectsApi* | [**get_specific_project_usage_projects_projects_project_uuid_usage_usage_type_key_get**](docs/ProjectsApi.md#get_specific_project_usage_projects_projects_project_uuid_usage_usage_type_key_get) | **GET** /sam/projects/projects/{project_uuid}/usage/{usage_type_key} | Get Specific Project Usage
*ProjectsApi* | [**get_usage_type_projects_usage_types_usage_type_key_get**](docs/ProjectsApi.md#get_usage_type_projects_usage_types_usage_type_key_get) | **GET** /sam/projects/usage/types/{usage_type_key} | Get Usage Type
*ProjectsApi* | [**remove_member_from_project_projects_projects_project_uuid_members_entity_uuid_delete**](docs/ProjectsApi.md#remove_member_from_project_projects_projects_project_uuid_members_entity_uuid_delete) | **DELETE** /sam/projects/projects/{project_uuid}/members/{entity_uuid} | Remove Member From Project
*ProjectsApi* | [**remove_project_key_projects_projects_project_uuid_keys_delete**](docs/ProjectsApi.md#remove_project_key_projects_projects_project_uuid_keys_delete) | **DELETE** /sam/projects/projects/{project_uuid}/keys | Remove Project Key
*ProjectsApi* | [**sandbox_projects_sandbox_get**](docs/ProjectsApi.md#sandbox_projects_sandbox_get) | **GET** /sam/projects/sandbox | Sandbox
*ProjectsApi* | [**search_projects_projects_projects_get**](docs/ProjectsApi.md#search_projects_projects_projects_get) | **GET** /sam/projects/projects | Search Projects
*ProjectsApi* | [**search_usage_type_projects_usage_types_get**](docs/ProjectsApi.md#search_usage_type_projects_usage_types_get) | **GET** /sam/projects/usage/types | Search Usage Type
*ProjectsApi* | [**update_project_projects_projects_project_uuid_put**](docs/ProjectsApi.md#update_project_projects_projects_project_uuid_put) | **PUT** /sam/projects/projects/{project_uuid} | Update Project
*ProjectsApi* | [**update_usage_type_projects_usage_types_usage_type_key_put**](docs/ProjectsApi.md#update_usage_type_projects_usage_types_usage_type_key_put) | **PUT** /sam/projects/usage/types/{usage_type_key} | Update Usage Type
*SecurityApi* | [**create_encryption_key_security_encryption_categories_category_keys_post**](docs/SecurityApi.md#create_encryption_key_security_encryption_categories_category_keys_post) | **POST** /sam/security/encryption/categories/{category}/keys | Create Encryption Key
*SecurityApi* | [**create_key_security_keys_post**](docs/SecurityApi.md#create_key_security_keys_post) | **POST** /sam/security/keys | Create Key
*SecurityApi* | [**delete_key_security_keys_key_uuid_delete**](docs/SecurityApi.md#delete_key_security_keys_key_uuid_delete) | **DELETE** /sam/security/keys/{key_uuid} | Delete Key
*SecurityApi* | [**generate_token_security_tokens_post**](docs/SecurityApi.md#generate_token_security_tokens_post) | **POST** /sam/security/tokens | Generate Token
*SecurityApi* | [**get_encryption_key_security_encryption_categories_category_keys_get**](docs/SecurityApi.md#get_encryption_key_security_encryption_categories_category_keys_get) | **GET** /sam/security/encryption/categories/{category}/keys | Get Encryption Key
*SecurityApi* | [**get_key_security_keys_key_uuid_get**](docs/SecurityApi.md#get_key_security_keys_key_uuid_get) | **GET** /sam/security/keys/{key_uuid} | Get Key
*SecurityApi* | [**search_keys_security_keys_get**](docs/SecurityApi.md#search_keys_security_keys_get) | **GET** /sam/security/keys | Search Keys
*SecurityApi* | [**verify_key_security_keys_verify_post**](docs/SecurityApi.md#verify_key_security_keys_verify_post) | **POST** /sam/security/keys/verify | Verify Key
*SupportApi* | [**create_contact_support_contact_post**](docs/SupportApi.md#create_contact_support_contact_post) | **POST** /sam/support/contact | Create Contact
*SupportApi* | [**create_ticket_support_projects_project_uuid_members_member_uuid_tickets_post**](docs/SupportApi.md#create_ticket_support_projects_project_uuid_members_member_uuid_tickets_post) | **POST** /sam/support/projects/{project_uuid}/members/{member_uuid}/tickets | Create Ticket
*SupportApi* | [**delete_contact_support_contact_delete**](docs/SupportApi.md#delete_contact_support_contact_delete) | **DELETE** /sam/support/contact | Delete Contact
*SupportApi* | [**list_tickets_support_projects_project_uuid_members_member_uuid_tickets_get**](docs/SupportApi.md#list_tickets_support_projects_project_uuid_members_member_uuid_tickets_get) | **GET** /sam/support/projects/{project_uuid}/members/{member_uuid}/tickets | List Tickets
*SupportApi* | [**update_ticket_support_projects_project_uuid_members_member_uuid_tickets_ticket_id_put**](docs/SupportApi.md#update_ticket_support_projects_project_uuid_members_member_uuid_tickets_ticket_id_put) | **PUT** /sam/support/projects/{project_uuid}/members/{member_uuid}/tickets/{ticket_id} | Update Ticket
*SupportApi* | [**view_ticket_support_projects_project_uuid_members_member_uuid_tickets_ticket_id_get**](docs/SupportApi.md#view_ticket_support_projects_project_uuid_members_member_uuid_tickets_ticket_id_get) | **GET** /sam/support/projects/{project_uuid}/members/{member_uuid}/tickets/{ticket_id} | View Ticket
*UsersApi* | [**confirm_signup**](docs/UsersApi.md#confirm_signup) | **POST** /sam/users/auth/signup/confirm | Confirmsignup
*UsersApi* | [**create_participant**](docs/UsersApi.md#create_participant) | **POST** /sam/users/participants | Createparticipant
*UsersApi* | [**create_user**](docs/UsersApi.md#create_user) | **POST** /sam/users | Createuser
*UsersApi* | [**delete_participant**](docs/UsersApi.md#delete_participant) | **DELETE** /sam/users/participants/{participant_id} | Deleteparticipant
*UsersApi* | [**delete_user**](docs/UsersApi.md#delete_user) | **DELETE** /sam/users/{user_id} | Deleteuser
*UsersApi* | [**get_participant**](docs/UsersApi.md#get_participant) | **GET** /sam/users/participants/{participant_id} | Getparticipant
*UsersApi* | [**get_user**](docs/UsersApi.md#get_user) | **GET** /sam/users/{user_id} | Getuser
*UsersApi* | [**login**](docs/UsersApi.md#login) | **POST** /sam/users/auth/login | Login
*UsersApi* | [**refresh_token**](docs/UsersApi.md#refresh_token) | **POST** /sam/users/auth/{app_client}/refresh-token | Refreshtoken
*UsersApi* | [**reset_password**](docs/UsersApi.md#reset_password) | **POST** /sam/users/auth/password/reset | Resetpassword
*UsersApi* | [**reset_password_confirmation_users_auth_password_reset_confirm_post**](docs/UsersApi.md#reset_password_confirmation_users_auth_password_reset_confirm_post) | **POST** /sam/users/auth/password/reset/confirm | Reset Password Confirmation
*UsersApi* | [**search_participants**](docs/UsersApi.md#search_participants) | **GET** /sam/users/participants | Searchparticipants
*UsersApi* | [**signup**](docs/UsersApi.md#signup) | **POST** /sam/users/auth/signup | Signup
*UsersApi* | [**update_participant**](docs/UsersApi.md#update_participant) | **PUT** /sam/users/participants/{participant_id} | Updateparticipant
*UsersApi* | [**update_user**](docs/UsersApi.md#update_user) | **PUT** /sam/users/{user_id} | Updateuser
*UsersApi* | [**user_validations**](docs/UsersApi.md#user_validations) | **POST** /sam/users/validations/{field} | Uservalidations


## RecursionError
When APIs/SDKs are large, imports in ehelply-python-sdk.apis and ehelply-python-sdk.models may fail with a
RecursionError indicating the maximum recursion limit has been exceeded. In that case, there are a couple of solutions:

Solution 1:
Use specific imports for apis and models like:
- `from ehelply_python_sdk.api.default_api import DefaultApi`
- `from ehelply_python_sdk.model.pet import Pet`

Solution 2:
Before importing the package, adjust the maximum recursion limit as shown below:

```python
import sys
sys.setrecursionlimit(1500)

import ehelply_python_sdk
from ehelply_python_sdk.apis import *
from ehelply_python_sdk.models import *
```

