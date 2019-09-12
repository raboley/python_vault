import pyvault
import pymongo

if __name__ == '__main__':

    vault_ip = ''
    username = ''
    password = ''

    hcvault = pyvault.HashicorpVault(vault_ip, username, password)

    ## just run a copy paste like this
    #     source = "secret/environments/dev"
    #     dest = "secret/environments/dev1"
    #
    #     paths = hcvault.get_source_paths(source)
    #     hcvault.copy_secrets(source, dest)

    # Get the oidc tokens
    # loop through all unique
    environment: str = "dev"

    oidc_list_to_update = hcvault.get_oidc_tokens_from_vault(environment)
    print(oidc_list_to_update)
    # update mongodb for that environment
    # for each client_id set the client_secret to be what is in vault

    mongo_username = 'admin'
    mongo_password = hcvault.get_mongo_password_for_environment(environment)

    if environment == "dev":
        environment_octet = 4
    if environment == "qa":
        environment_octet = 3
    if environment == "qa2":
        environment_octet = 14

    client = pymongo.MongoClient(
        f"mongodb://{mongo_username}:{mongo_password}@10.{environment_octet}.0.11:27017,10.{environment_octet}.0.12:27017,10.{environment_octet}.0.13:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1")
    oidc = client["oidc"]
    clients_collection = oidc["clients"]

    for client_secret_to_update in oidc_list_to_update:
        find_query = {"client_id": client_secret_to_update["name"]}
        update_query = {"$set": {"client_secret": client_secret_to_update["secret"]}}
        print(find_query, update_query)
        clients_collection.update_one(find_query, update_query)
