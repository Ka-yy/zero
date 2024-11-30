# FOR CONTRIBUTORS 

## initialize the git repo locally and set the upstream

then set the upstream branch. *i wont get into that because you guys should already know that*

## create the virtual environment

 ```bash
 python -m venv my_env
```

This creates a `my_env` directory in your project folder.

### running the environment

#### if you're using a bash terminal

```bash
. my_env/Scripts/activate 
```

#### if youre using cmd

```cmd
cd my_env/Scripts
.\activate
```

paste this and press `enter`

your terminal should look like this, for example:

```bash
(my_env)kufre@erfuk:~/code/network-programming-project$ 
```

and the virtual environment can be ended using `deactivate`

## Then install dependencies

you can install all the necessary dependencies using:

```shell
pip install -r requirements.txt
```
