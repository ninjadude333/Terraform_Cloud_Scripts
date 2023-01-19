import requests
import json
import argparse
import sys
import time

def run_api_destroy(ws_id, token):  
    url = "https://app.terraform.io/api/v2/runs"
    api_data = {
      "data": {
        "attributes": {
          "is-destroy": True,
          "refresh": True,
          "auto-apply": apply,
          "refresh-only": False
        },
        "relationships": {
          "workspace": {
            "data": {
              "type": "workspaces",
              "id": ws_id
            }
          }
        },
        "type": "runs"
      }
    }
    payload = json.dumps(api_data)
    headers = {
      'Content-Type': 'application/vnd.api+json',
      'Authorization': 'Bearer ' + token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    jsonResponse = response.json()
    print("run id is: " + jsonResponse["data"]["id"])
    return jsonResponse["data"]["id"]

def get_run_status(run_id, token):
    url = "https://app.terraform.io/api/v2/runs/" + run_id
    payload={}
    headers = {
      'Authorization': 'Bearer ' + token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    jsonResponse = response.json()
    return jsonResponse["data"]["attributes"]["status"]

def wait_for_run_finish(run_id,status,token,ttl):
    while 'finish' not in status and 'error' not in status and 'cancel' not in status and 'applied' not in status:
            time.sleep(ttl)
            status = get_run_status(run_id,token)
            if verbose:
                print("run status is: " + status)
    return(status)

parser = argparse.ArgumentParser(
    prog='Destroy_TFC_Cloud_WS.exe',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=('''\
        This tool will send a destroy run request to a Terraform Cloud Workspace
        Ver 1.0.0
        Coded By The_Dude
        '''),
    epilog=('''\

        example for running the tool:
        Destroy_TFC_Cloud_WS.exe -org MyOrg -ws_id xcvbnmdfgdfgdfgd -token <myToken>
        
        -ws_file can be used instead of -ws_id to specify a txt file containing multiple ws-ids seperated by newline.
        use -autoapply to force destory plan apply ignoring default WS settings.

      use -v for verbose/debug mode

        '''))

parser = argparse.ArgumentParser(description='Remote destroy for TFC')

parser.add_argument('-org', action="store", dest="org_name", help="Organization Name", required=True)
parser.add_argument('-ws_id', action="store", dest="ws_id", help="Id of WS to destroy")
parser.add_argument('-ws_file', action="store", dest="ids_file_name", help="Full path including file name to the ws file")
parser.add_argument('-token', action="store", dest="tfc_token", help="Api TOKEN", required=True)
parser.add_argument('-autoapply', action="store_true", dest="apply", help="force automatic apply.")
parser.add_argument('-v', action="store_true", dest="verbose", help="Debug Mode, show extra output in console.")

if not len(sys.argv) > 1:
    args = parser.parse_args(['-h'])
    sys.exit()
else:
    args = parser.parse_args()
    org_name = args.org_name
    ws_id = args.ws_id
    ws_file = args.ids_file_name
    token = args.tfc_token
    apply = args.apply
    verbose = args.verbose


if __name__ == "__main__":

    start = ""
    end = ""
    
    if ws_id:
        run_id = run_api_destroy(ws_id,token)
        start = time.time()
        status = get_run_status(run_id,token)
        result = wait_for_run_finish(run_id,status,token,5)
        end = time.time()
        print(run_id + " ended with result: " + result + " and elapsed " + str(int(end-start)) + " seconds.")
        
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
            run_id = run_api_destroy(line.strip(),token)
            start = time.time()
            status = get_run_status(run_id,token)
            result = wait_for_run_finish(run_id,status,token,5)
            end = time.time()
            print(run_id + " ended with result: " + result + " and elapsed " + str(int(end-start)) + " seconds.")
        file1.close()
    else:
        print ("you must specify eighter a single ws-id or a file with multipe ids.")
