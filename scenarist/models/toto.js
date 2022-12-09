$("#leForm").submit(function(){
			// 2D Encryption
			var input = $("#resultKeyAttempt").val();
			theKey = "kpoisaijdieyjaf";
			var theAlphabet =   "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "abcdefghijklmnopqrstuvwxyz";

			// Validate theKey:
			theKey = theKey.toUpperCase();
			var theKeysLength = theKey.length;
			var i;
			var adjustedKey = "";
			for(i = 0; i < theKeysLength; i ++)
			{
				var currentKeyChar = theAlphabet.indexOf(theKey.charAt(i));
				if(currentKeyChar < 0)
					continue;
				adjustedKey += theAlphabet.charAt(currentKeyChar);
			}
			theKey = adjustedKey;
			theKeysLength = theKey.length;

			// Transform input:
			var inputLength = input.length;
			var output = "";
			var theKeysCurrentIndex = 0;
			for(i = 0; i < inputLength; i ++)
			{
				var currentChar = input.charAt(i);
				var currentCharValue = theAlphabet.indexOf(currentChar);

				if(currentCharValue < 0)
				{
					output += currentChar;
					continue;
				}
				var lowercase = currentCharValue >= 26 ? true : false;
				currentCharValue += theAlphabet.indexOf(theKey.charAt(theKeysCurrentIndex));
				currentCharValue += 26;
				if(lowercase)
					currentCharValue = currentCharValue % 26 + 26;
				else
					currentCharValue %= 26;
				output += theAlphabet.charAt(currentCharValue);
				theKeysCurrentIndex =(theKeysCurrentIndex + 1) % theKeysLength;
			}

			// Check result for validity
			$("#resultDiv").hide("fast", function(){
				if(output == "DwsDagmwhziArpmogWaSmmckwhMoEsmgmxlivpDttfjbjdxqBwxbKbCwgwgUyam")
					$('#resultDiv').html("<p>Yeah, that's correct</p>");
				else
					$('#resultDiv').html("<p>No, that's not correct</p>");
				$("#resultDiv").show("slow");
			});
			// Output the "output" variable to the HTML for viewing
			$("#resultDiv").hide("fast", function(){
					$('#resultDiv').html("Encrypted Output: " + output);
				$("#resultDiv").show("slow");
			});
		});