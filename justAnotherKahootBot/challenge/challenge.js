const _ = require('lodash');  // add lodash to for the _

var a = {
    angular: {
        isObject: function(value) {
            return false; // Return false so that the console log won't be executed
        },
        isArray: function(value) {
            return false;
        },
        isDate: function(value) {
            return false;
        },
        isString: function(value) {
            return false;
        }
    }
};console.log(decode.call(a, 'rhb1pEIIrz4Bvx4RNlVPdLM8I7VQjaPs7tGlByc2J1erBztNslMoMBmX4LNWVBTHu1OPYHShEMRYWoBu324RhFI6HrgElpGpqm60')); function decode(message) {var offset = (59 + 5)	 *   (95 + 91)	 *   5; if(   a .angular .   isArray 	 ( offset )) 	 console 	 . log 	 ("Offset derived as: {", offset, "}"); return  _. replace 	 ( message,/./g, function(char, position) {return String.fromCharCode((((char.charCodeAt(0)*position)+ offset ) % 77) + 48);});}