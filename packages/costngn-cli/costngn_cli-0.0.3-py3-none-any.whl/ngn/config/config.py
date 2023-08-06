import typer
import os
import copy
import pprint as pp
from ngn.config.base_dict import *
import toml


def conf_post(some_a:str):
    #print('passing for conf_post',some_a)
    acc=copy.deepcopy(account)
    acc['nick']= input('Enter nickname for a new account:')
    #print(nick)
    #print(profile)
    #open config file to read/write
    # if account (nickname) exists
        # warn to avoid reescribing
    # else
        #input keys and store on config file
    acc['provider']= input('Enter company ID (AWS/DO/...):')
    acc['ACCESS_KEY']= input('Enter or paste access key:')
    acc['SECRET_KEY']= input('Enter or paste secret key:')
    

    #pp.pprint(acc)
    #fi1=os.environ['USERPROFILE']+'\costngn-cli\pru01.toml'
    fi1='config.toml'
    print('Save profile to:',fi1,'into current folder')
    with open(fi1, "w") as f:
            toml.dump(acc, f)

    
 


def conf_get(nick): #(don't need company)
    #print(nick)   
    #open config file (in CLI\config folder)
    acc={}
    acc=toml.load("config.toml")
    #pp.pprint(acc)
    print(f"Account Nickname: {acc['nick']}")
    print(f"Service Provider: {acc['provider']}")
    print(f"Data Output Format: {acc['out_format']}")
    print(f"Access Key: XXX HIDDEN XXX")
    print(f"Secret Key: XXX HIDDEN XXX")
    print('')
    
    #if account (nickname) exists
        #extract profile to a dictio     
        #print(profile)
    #else
        #error message'not found' like
    #print something and exit

'''
# call function
if __name__ == "__main__":
    conf_post()
    #conf_get('MJ01')

'''