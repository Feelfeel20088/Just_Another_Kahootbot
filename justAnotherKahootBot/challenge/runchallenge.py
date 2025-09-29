import subprocess
import base64
import re
import pytest
import os
from justAnotherKahootBot.config.state import args 


# const
logdir = args.log_dir

challenge_path = os.path.join(logdir, 'challenge/challenge.js') 
os.makedirs(os.path.dirname(challenge_path), exist_ok=True)


# this is mostly just gonna be used for testing. 
class Challenge: 
    
    def __init__(self, challenge_code: str, token: str):
        self.challenge_code = challenge_code
        self.token = token

    # TODO fix this fucking shit
    
    @pytest.mark.challenge_tests
    def parse_challenge_code(self):
        challenge_code = 'console.log(' + self.challenge_code[:121] + ')' + self.challenge_code[121:]
        challenge_code = re.sub(r'this', 'a', challenge_code)
        return challenge_code

    
    @pytest.mark.challenge_tests
    def dump_code_and_execute(self):
        challenge_script = open("./justAnotherKahootBot/challenge/angular.js", "r").read() + self.challenge_code

        open(challenge_path, "w").write(challenge_script)
    
        result = subprocess.run(['node', challenge_path], capture_output=True, text=True)
        
        # TODO if this fails it should send a alert to promethies
        # just something to keep in mind when we add kube intagration
        if result.returncode != 0:
            print("Node.js execution failed!")
            print("Error output:", result.stderr)

        challenge = result.stdout.strip()

        decoded_token = base64.b64decode(self.token).decode('utf-8', 'strict')

        return decoded_token
        
    @pytest.mark.challenge_tests
    def xor_decoded_token(self):
        return "".join([chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(self.challenge, decoded_token)])
        
    @staticmethod
    def run_challenge(challenge_code: str, token: str) -> str:
        """
        Executes a JavaScript challenge to authenticate, modifies the challenge code, and runs it with Node.js. 
        The challenge output is XOR-ed with a decoded session token to return the final result.

        Args:
            challenge_code (str): The JavaScript code for the challenge.
            token (str): A Base64-encoded session token.

        Returns:
            str: The XOR-ed result of the challenge output and the token.
        """
        
        # yes i know this is a peice of shit dont judge
        challenge_code = 'console.log(' + challenge_code[:121] + ')' + challenge_code[121:]
        challenge_code = re.sub(r'this', 'a', challenge_code)

        challenge_script = open("./justAnotherKahootBot/challenge/angular.js", "r").read() + challenge_code

        open(challenge_path, "w").write(challenge_script)
        

        result = subprocess.run(['node', challenge_path], capture_output=True, text=True)
        challenge = result.stdout.strip()
        if result.returncode != 0:
            print("Node.js execution failed!")
            print("Error output:", result.stderr)


        decoded_token = base64.b64decode(token).decode('utf-8', 'strict')
        
        

        return "".join([chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(challenge, decoded_token)])
        

        



    