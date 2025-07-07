# from ..Just_Another_Kahoot_Bot.challenge.runchallenge import runChallenge


# def test_run_challenge():
#     js_challenge_str = """
#     decode.call(this, 'QRPaWw16EeUJBSbi9exchBSYMTEy5set5zkHbTK2eQwkmLWDXlf4Ig14vT3Z6UTd2Y7dhcwYVqt3QxFt6u6LyPzZPkpwhtzU7b1W');
#     function decode(message) {
#         var offset = 38 * ((39 * (87 * 55)) + 43 * 40) * 80;
#         if (this.angular.isArray(offset)) 
#             console.log("Offset derived as: {", offset, "}");
#         return _.replace(message, /./g, function(char, position) {
#             return String.fromCharCode(((char.charCodeAt(0) * position) + offset) % 77 + 48);
#         });
#     }
#     """

#     client_id = "A1VUNl9+NWJYYAF2RgY1VTNPUlcAVS0iVBBAAERLS3MBRRZ4NVZVHgxSYihDA2wDZi5AVUxpBl02XwU6AklyZwxeVVJnfgpTBQ8NLmtVY1oIUgM6B05GL1R+PHBCUGtl"

#     assert runChallenge(js_challenge_str, client_id) == "b33fc2f862e61dfbf77bb4fc5f852279b2b4ff7d498f47380b3c4061e01de274359025e51d4f6498a58af73fa6f57972"