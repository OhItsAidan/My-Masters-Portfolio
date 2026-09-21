# SSH-Honeypot-Project
This is my SSH Honeypot for CMP509 Ethical Hacking - This is one of the largest projects I have attempted, so feedback is appreciated :)
The Honeypot is mainly designed to run inside Docker, but if desired, you can also run it inside a Linux VM, or if you want to run it inside Windows, download PuTTY and connect to it through SSH that way using PowerShell.

## 📁 File Structure
```
ssh_honeypot_project/
├── Dockerfile
├── README.md
├── requirements.txt
├── server.key
├── server.pub
├── ssh_honeypot.log
├── src/
| └── ssh_honeypot.py
```
## Let's begin!
Start by navigating to the folder within your chosen shell, ideally PowerShell if on Windows, or the standard Linux Terminal if on Linux.
### 1. Build the Docker Image

```bash
docker build -t ssh_honeypot .
```

### 2. Run the Docker Container
```bash
docker run -d -p 2222:2222 --name ssh_honeypot ssh-honeypot
```

### 3. Once running, you should be able to log in with any credentials
It will ask you to fingerprint the server to add your machine to known hosts so it can verify you, that is fine. Once done, you should be able to get in without the key.
```
ssh -i server.key -p 2222 testuser@127.0.0.1
testuser@127.0.0.1's password: 
```
If you make any changes to the honeypot, you will need to stop the container and rebuild it. 

### 4. Commands
Use this command for a list of other commands available within the honeypot, each command entered is logged in the log file, so you can analyse activity.
```bash
help
```
## 🔐 SSH Key Permissions
You need to ensure the server key has the correct permissions. If the key is refused, use this command:
```bash
chmod 600 server.key
```

## 📄 Log Output
A big part of this project is to capture the activity within the honeypot, the results are recorded into /app/ssh_honeypot.log inside the container. You can view them with this command:
```bash
docker exec -it ssh_honeypot cat /app/ssh_honeypot.log
```
If you want to copy the logs to your host machine, run:
```bash
docker cp ssh_honeypot:/app/ssh_honeypot.log ./ssh_honeypot.log
```
If you are running the Honeypot outside of Docker, then the log file provided should automatically fill with activity data.

### ⚠️ Known Issues
- If you end up rebuilding often, you may need to remove the old container.
- Always run Docker with sudo if your user does not have the necessary permissions.

### 📚 Usage
 - This honeypot is for educational and research purposes only. Please use it responsibly and do not expose it to the public internet.
 - If running outside of a container, remove all instances of '/app' inside the source code so the program can find the right files.
#
I have put some Cyberpunk-themed files in here for immersion as well as some movie references, hope you recognise them!

If any issues, please do not hesitate to reach me on my email - a1dankhd@gmail.com








