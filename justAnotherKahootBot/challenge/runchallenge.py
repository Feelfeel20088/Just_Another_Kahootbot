import subprocess
import base64
import re
import os

def runChallenge(challenge_code: str, token) -> str:
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

    challenge_script = open("./Just_Another_Kahoot_Bot/src/Just_Another_Kahoot_Bot/challenge/angular.js", "r").read() + challenge_code

    open("./Just_Another_Kahoot_Bot/src/Just_Another_Kahoot_Bot/challenge/challenge.js", "w").write(challenge_script)
   

    result = subprocess.run(['node', "./Just_Another_Kahoot_Bot/src/Just_Another_Kahoot_Bot/challenge/challenge.js"], capture_output=True, text=True)
    challenge = result.stdout.strip()

    decoded_token = base64.b64decode(token).decode('utf-8', 'strict')
    result = []
    
    for c1, c2 in zip(challenge, decoded_token):
        result.append(chr(ord(c1) ^ ord(c2)))
    return "".join(result)

    


