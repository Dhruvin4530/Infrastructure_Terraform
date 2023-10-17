import hcl
import subprocess


# Run the 'git rev-parse HEAD' command to get the last commit SHA
try:
    commit_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
    print("Last commit SHA:", commit_sha)
except subprocess.CalledProcessError as e:
    print("Error:", e)

# Define the path to the terraform.tfvars file
file = f"git diff-tree --no-commit-id --name-only -r {commit_sha} | head -1 | cut -d'/' -f2"

tfvars_file = subprocess.check_output(file, shell=True, stderr=subprocess.STDOUT, text=True)
print(tfvars_file)

def get_account_name_from_tfvars(tfvars_file):

    try:
        with open(tfvars_file, 'r') as f:
        # Load the contents of the terraform.tfvars file into a dictionary
            tfvars_data = hcl.load(f)

            # Check if the 'account_name' key exists or not
            if 'account_name' in tfvars_data:
                return tfvars_data['account_name']
            else:
                return None

    except FileNotFoundError:
        return f"File {tfvars_file} not found."


# Call the function and store the result in a variable
account_name = get_account_name_from_tfvars(tfvars_file)

# Print the result
print(account_name)
