# StuffAccountig Bot-Cliet
A bot-client for [Stuff Accouting Backend](https://github.com/denver-code/stuff_accounting_backend)
# ▹ Run using docker #
> [!NOTE]  
> For start make sure you have docker installed on your machine.
```bash
sh scripts/run.sh
```
or
``` bash
docker-compose up --build -d
```
# ▹ Installation #
> [!NOTE]  
> For start make sure you have python and redis and mongodb installed on your machine.
``` Bash
git clone https://github.com/denver-code/stuff_accounting_bot
cd stuff_accounting_bot
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```   
Rename ```  sample.env -> .env``` and don't forget to change the settings inside.

# ▹ Run #
``` Bash
source .venv/bin/activate
python3 -m bot
```
