from hashlib import sha256
import sys
import string

"""
Keys
Note: most up to date record is kept in Discord::Discord Raiders Hub::For Private Reference::Improved Alts

apple --str
smartguy89 --str > gmail + discord
smartguy88 --str > discord + gmail
smartguy87 --str > gmail + discord
smartguy86 --str > gmail + discord
"""

"""
Password that use --str

apple
smartguy89
smartguy88
smartguy87
smartguy86
"""

chars = string.ascii_letters + string.digits + string.punctuation + \
    " " + string.punctuation + string.ascii_letters + \
    string.digits + string.punctuation
if len(sys.argv) > 4:
  print(f"Chars ({len(chars)}):{chars}")


def main(args):
  global chars
  try:
    input = bytes(args[0], encoding="utf-8")
    extra = bytes(args[1] or b"", encoding="utf-8")
  except:
    print("Invalid input, requires 2 text command line inputs")
  else:
    testObj = sha256(input + extra)
    testHash = str(testObj.hexdigest())
    print(f"Full Hash:{testHash}")
    print(f"Standard Length Hash:{testHash[:10]}")
    testHashNum = str(int.from_bytes(testObj.digest(), "big"))
    # Splits string every 2nd character
    testHashNumList = [testHashNum[i:i+2]
                       for i in range(0, len(testHashNum), 2)]
    #print(testHashStr) # Debug only :)
    hashStr = "".join([chars[int(testHashNumList[n]) + int(testHashNumList[n+1])]
                      for n in range(0, len(testHashNumList)-1, 2)])
    finalHashStr = hashStr[:5] if len(hashStr) > 5 else hashStr
    if len(args) > 2:
      print(f"Hash String:Smg!88{finalHashStr}")
  print("Finish")


if __name__ == "__main__":
  main(sys.argv[1:])
