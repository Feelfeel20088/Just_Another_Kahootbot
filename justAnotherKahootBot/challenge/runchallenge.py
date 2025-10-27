import base64
class Challenge:


    
    @staticmethod
    def run_challenge(challenge_code: str, token: str) -> str:
        """
        Solves the Kahoot authentication challenge in pure Python.

        The function replicates the logic of the JavaScript challenge:
        1. Sanitizes the challenge code by removing non-ASCII and tab characters.
        2. Extracts the 'offset' expression and evaluates it.
        3. Extracts the challenge 'input' string.
        4. Computes a pseudo-randomized ASCII sequence from the input and offset.
        5. Decodes the provided Base64 token.
        6. XORs both strings character-by-character to produce the final authentication string.

        Args:
            challenge_code (str): The JavaScript code snippet containing the offset and input definitions.
            token (str): A Base64-encoded token to decode and XOR with the generated solution.

        Returns:
            str: The final decoded authentication key derived from XOR-ing the computed solution 
                 with the decoded token.

        """

        challenge_code = ''.join(c for c in challenge_code.replace('\t', '', -1) if ord(c) < 128)

        # Extract offset expression and evaluate
        offset = challenge_code.split("offset =")[1].split(";")[0]
        offset = int(eval(offset))

        # Extract input string
        input = challenge_code.split("this, '")[1].split("'")[0]

        # Generate the intermediate "solution" string
        solution = ""
        for i, c in enumerate(input):
            solution += chr(((ord(c) * i + offset) % 77) + 48)

        # Decode and XOR with token
        decoded_token = base64.b64decode(token).decode('utf-8', 'strict')
        return "".join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(solution, decoded_token))




    