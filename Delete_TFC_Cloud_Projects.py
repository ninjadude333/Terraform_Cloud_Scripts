import requests
import argparse
import sys

def run_api_delete_proj(pid, token):
    url = "https://app.terraform.io/api/v2/projects/" + pid

    payload={}
    headers = {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/vnd.api+json'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(response)
    return response


parser = argparse.ArgumentParser(
    prog='Delte_TFC_Cloud_Projects.exe',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=('''\
        This tool will send a delete projects from Terraform Cloud
        Ver 1.0.0
        Coded By The_Dude
        '''),
    epilog=('''\

        example for running the tool:
        Delte_TFC_Cloud_Projectss.exe -org MyOrg -pid xcvbnmdfgdfgdfgd -token <myToken>
        
        -pid_file can be used instead of -uid to specify a txt file containing multiple pid's seperated by newline.

      use -v for verbose/debug mode

        '''))

parser = argparse.ArgumentParser(description='delete users for TFC')

parser.add_argument('-org', action="store", dest="org_name", help="Organization Name", required=True)
parser.add_argument('-pid', action="store", dest="pid", help="Id of project to delete")
parser.add_argument('-pid_file', action="store", dest="pids_file_name", help="Full path including file name to the pid's file")
parser.add_argument('-token', action="store", dest="tfc_token", help="Api TOKEN", required=True)
parser.add_argument('-v', action="store_true", dest="verbose", help="Debug Mode, show extra output in console.")

if not len(sys.argv) > 1:
    args = parser.parse_args(['-h'])
    sys.exit()
else:
    args = parser.parse_args()
    org_name = args.org_name
    pid = args.pid
    pids_file = args.pids_file_name
    token = args.tfc_token
    verbose = args.verbose


if __name__ == "__main__":
 
    if pid:
        result = run_api_delete_proj(pid,token)
        print("result: " + str(result.status_code))
        
    elif pids_file:
        file1 = open(pids_file, 'r')
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
            result = run_api_delete_proj(line.strip(),token)
            print("result: " + str(result.status_code))
        file1.close()
    else:
        print ("you must specify eighter a single pid or a file with multipe pids.")