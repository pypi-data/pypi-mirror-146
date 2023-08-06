
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from keycloak_api.api.attack_detection_api import AttackDetectionApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from keycloak_api.api.attack_detection_api import AttackDetectionApi
from keycloak_api.api.authentication_management_api import AuthenticationManagementApi
from keycloak_api.api.client_attribute_certificate_api import ClientAttributeCertificateApi
from keycloak_api.api.client_initial_access_api import ClientInitialAccessApi
from keycloak_api.api.client_registration_policy_api import ClientRegistrationPolicyApi
from keycloak_api.api.client_role_mappings_api import ClientRoleMappingsApi
from keycloak_api.api.client_scopes_api import ClientScopesApi
from keycloak_api.api.clients_api import ClientsApi
from keycloak_api.api.component_api import ComponentApi
from keycloak_api.api.groups_api import GroupsApi
from keycloak_api.api.identity_providers_api import IdentityProvidersApi
from keycloak_api.api.key_api import KeyApi
from keycloak_api.api.protocol_mappers_api import ProtocolMappersApi
from keycloak_api.api.realms_admin_api import RealmsAdminApi
from keycloak_api.api.role_mapper_api import RoleMapperApi
from keycloak_api.api.roles_api import RolesApi
from keycloak_api.api.roles_by_id_api import RolesByIDApi
from keycloak_api.api.root_api import RootApi
from keycloak_api.api.scope_mappings_api import ScopeMappingsApi
from keycloak_api.api.user_storage_provider_api import UserStorageProviderApi
from keycloak_api.api.users_api import UsersApi
