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
Setup environment:<br>
1. Create file called .env in the same folder.<br>
2. In the .env file type:<br>
	* OPENAI_API_KEY=<key><br>
Replace the <key> with the actual key from your platform profile at https://platform.openai.com<br>
3. Add following for AWS environment where you will be creating resources.<br>
	* AWS_ACCESS_KEY_ID=<key><br>
	* AWS_SECRET_ACCESS_KEY=<key><br>
	* AWS_DEFAULT_REGION=ap-south-1<br>
Note: Exclude the .env file from your git branch
