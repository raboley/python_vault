#!/usr/bin/python3

import getopt
import pyvault
import sys


def main(argv):
    vault_ip = ''
    username = ''
    password = ''
    token_only = False

    # hcvault = pyvault.HashicorpVault(vault_ip, username, password)
    # hcvault.copy_secrets('secret/environments/qa', 'secret/environments/qa2')
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hv:u:p:t", ["vault-address=", "username=", "password=", "token-only"])
    except getopt.GetoptError:
        print(""" 
        error: parameters not passed in correctly, should be at least 'python main.py --vault-address=<vault_ip> --username=<okta_username> --password=<okta_password>'
        """)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("""
            Interacts hashicorp vault to authenticate and copy secrets
            
            ex. 'python main.py --vaultaddress=<vault_ip> --username=<okta_username> --password=<okta_password> --token-only'
            
            -p, --password : the okta_password to authenticate with vault server
            
            -t, --token-only : just returns the token from vault
            
            -u, --username : the okta_username to authenticate with vault server
            
            -v, --vault-address : the ip address of the vault server without the port
            
            """)
            sys.exit()
        elif opt in ("-v", "--vault-address"):
            vault_ip = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-t", "--token-only"):
            token_only = True
        # print('vault_ip is:', vault_ip)
        # print('username is:', username)
        # print('password is:', password)
        # print('just get the token?:', str(token_only))

        if vault_ip == "":
            print("""-v, --vault-address is a required argument, please add a vault ip address
                  python main.py --vault-address=<vault_ip> --username=<okta_username> --password=<okta_password> [--token-only]
                """)

            sys.exit(2)

        if username == "":
            print("""-u, --username is a required argument, please try again with an okta username"
                  
                  python main.py --vault-address=<vault_ip> --username=<okta_username> --password=<okta_password> [--token-only]
                  """)
            sys.exit(2)

        if password == "":
            print("""-p, --password is a required argument, please add an okta password
                  
                  python main.py --vault-address=<vault_ip> --username=<okta_username> --password=<okta_password> [--token-only]
                  """)
            sys.exit(2)

        if token_only == True:
            hcvault = pyvault.HashicorpVault(vault_ip, username, password)
            print('##vso[task.setvariable variable=output_vault_token;]%s' % hcvault.token)


if __name__ == '__main__':
    main(sys.argv[1:])
