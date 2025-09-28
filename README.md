# infrai
AI for Infra<br>
<br>
Set virtual environment:<br>
python3 -m venv <name><br>
<br>
Note: Exclude the folder <name> from your git branch<br>
<br>
Activate virtual environment:<br>
source <name>/bin/activate<br>
<br>
Install packages:<br>
pip3 install -r requirments.txt<br>
<br>
## Setup environment:

1. Create a file called `.env` in the same folder.
2. In the `.env` file, type:

       OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxx

   Replace the `xxxxxxxxxxxxxxxxxxxxx` with your actual key from your platform profile at [https://platform.openai.com](https://platform.openai.com)

3. Add the following for the AWS environment where you will be creating resources:

       AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxxxx
       AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxx
       AWS_DEFAULT_REGION=ap-south-1

4. **Note**: Exclude the `.env` file from your Git branch (add it to `.gitignore`).

