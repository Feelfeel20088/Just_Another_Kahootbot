from justAnotherKahootBot.challenge.runchallenge import Challenge


def test_run_challenge():
    js_challenge_str = js_challenge_str = "decode.call(this, 'CHH7d8RTfdxAxhQMN2Qxlg81ELRIj2YTer6aeQLSslnI6djb42bmEj9K1I8NMLEcWELPCu9NF7EB3Q3vWtXreXM7FeWfOaT6dVUt'); function decode(message) {var offset = 87*99+((86*(10*12))*99+59); if(this.angular.isDate(offset)) console.log('Offset derived as:', offset); return _.replace(message,/./g,function(char,position){return String.fromCharCode((((char.charCodeAt(0)*position)+offset)%77)+48);});}"

    client_id = "DgpRK31HPkdVEVVmRFxFCX4jA1tzdgoTVUNBWw9UFQYJBgsnNlxVchpTDkwNAmhSaVRHKggIX18TI39OCHlbB2FjewwuVwQKUHIxZW9bEyVleEMBfyxdeggeTQplfVpf"
    assert Challenge.run_challenge(js_challenge_str, client_id) == "10da37c78e9316261a95005c3056fff7428afe30b5169c0c6e7de4b4ca247618611bbd5328f06daa89572fb07f9c8630"