import requests
import json
import argparse
import sys
import time

def run_api_delete(ws_id,token):  
    url = "/workspaces/:" + ws_id + "/actions/safe-delete"
    payload={}
    headers = {
      'Authorization': 'Bearer $TOKEN',
      'Content-Type': 'application/vnd.api+json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    jsonResponse = response.json()
    print(jsonResponse)
    return jsonResponse


parser = argparse.ArgumentParser(
    prog='Safe_Delete_TFC_WS.exe',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=('''\
        This tool will delete a Terraform Cloud Workspace
        Ver 1.0.0
        Coded By The_Dude
        '''),
    epilog=('''\

        example for running the tool:
        Safe_Delete_TFC_WS.exe -ws_id xcvbnmdfgdfgdfgd -token <myToken>
        
        -ws_file can be used instead of -ws_id to specify a txt file containing multiple ws-ids seperated by newline.

      use -v for verbose/debug mode

        '''))

parser = argparse.ArgumentParser(description='Remote destroy for TFC')

parser.add_argument('-ws_id', action="store", dest="ws_id", help="Id of WS to destroy")
parser.add_argument('-ws_file', action="store", dest="ids_file_name", help="Full path including file name to the ws file")
parser.add_argument('-token', action="store", dest="tfc_token", help="Api TOKEN", required=True)
parser.add_argument('-v', action="store_true", dest="verbose", help="Debug Mode, show extra output in console.")

if not len(sys.argv) > 1:
    args = parser.parse_args(['-h'])
    sys.exit()
else:
    args = parser.parse_args()
    ws_id = args.ws_id
    ws_file = args.ids_file_name
    token = args.tfc_token
    verbose = args.verbose


if __name__ == "__main__":
    
    if ws_id:
        run_id = run_api_delete(ws_id,token)
        print(run_id)
        
    elif ws_file:
        file1 = open(ws_file, 'r')
        count = 0
          
        while True:
            count += 1

            # Get next line from file
            line = file1.readline()
            
            # if line is empty
            # end of file is reached
            if not line:
                break    

            print(line)
            run_id = run_api_delete(line.strip(),token)
            print(run_id)
        file1.close()
    else:
        print ("you must specify eighter a single ws-id or a file with multipe ids.")