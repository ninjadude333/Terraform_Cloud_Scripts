import requests
import argparse
import sys

def run_api_get_workspaces(org_name,token,search_string):
    if not search_string:
        url = "https://app.terraform.io/api/v2/organizations/" + org_name + "/workspaces"
    else:
        url = "https://app.terraform.io/api/v2/organizations/" + org_name + "/workspaces?search[wildcard-name]=*" + search_string + "*"

    payload={}
    headers = {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/vnd.api+json'
    }

    ids = []
    response = requests.request("GET", url, headers=headers, data=payload)
    jsonResponse = response.json()
    for x in range(0,len(jsonResponse["data"])):
        if verbose:
            print("WS Name: {0} *** WS ID: {1}".format(jsonResponse["data"][x]["attributes"]["name"],jsonResponse["data"][x]["id"]))
        ids.append(jsonResponse["data"][x]["id"])
    return ids


parser = argparse.ArgumentParser(
    prog='Fetch_TFC_Cloud_Workspaces.exe',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=('''\
        This tool will get all workspaces names and id's from Terraform Cloud
        Ver 1.0.0
        Coded By The_Dude
        '''),
    epilog=('''\

        example for running the tool:
        Fetch_TFC_Cloud_Workspaces.exe -org MyOrg -token <myToken>
        
        -search_string can be used to add a filter word for the WS query, this word will be wrapped with wilcards.  *my_filter_string*
        -file can be used to specify a full path to an output file.

      use -v for verbose/debug mode

        '''))

parser = argparse.ArgumentParser(description='delete users for TFC')

parser.add_argument('-org', action="store", dest="org_name", help="Organization Name", required=True)
parser.add_argument('-search_string', action="store", dest="s_string", help="string to search - will be wrapped with *")
parser.add_argument('-file', action="store", dest="filePath", help="export result to file - specify complete file path")
parser.add_argument('-token', action="store", dest="tfc_token", help="Api TOKEN", required=True)
parser.add_argument('-append', action="store_true", dest="append", help="append to file? or overwrite?")
parser.add_argument('-v', action="store_true", dest="verbose", help="Debug Mode, show extra output in console.")

if not len(sys.argv) > 1:
    args = parser.parse_args(['-h'])
    sys.exit()
else:
    args = parser.parse_args()
    org_name = args.org_name
    s_string = args.s_string
    filePath = args.filePath
    token = args.tfc_token
    append = args.append
    verbose = args.verbose


if __name__ == "__main__":
    id_list = run_api_get_workspaces(org_name,token,s_string)
    mode = "a" if append else "w"
    if filePath:
        f = open(filePath, mode)
        if append:
            f.write("\n"+'\n'.join(id_list))
        else:
            f.write('\n'.join(id_list))
        f.close()
    else:
        print(id_list)
