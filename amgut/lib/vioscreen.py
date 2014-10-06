from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64decode, b64encode

from amgut import AMGUT_CONFIG
from amgut import media_locale
from amgut import AG_DATA_ACCESS


def pkcs7_pad_message(in_message):
    # http://stackoverflow.com/questions/14179784/python-encrypting-with-pycrypto-aes
    length = 16 - (len(in_message) % 16)
    return (in_message + chr(length)*length)


def pkcs7_unpad_message(in_message, ):
    return in_message[:-ord(in_message[-1])]


def encrypt_key(survey_id):
    """Encode minimal required vioscreen information to AES key"""
    userinfo = AG_DATA_ACCESS.get_person_info(survey_id)
    # clean up gender
    if userinfo["gender"] == "Male":
        gender_id = 1
    elif userinfo["gender"] == "Female":
        gender_id = 2
    else:
        # Default to female?
        gender_id = 2

    # clean up birthdate
    if userinfo['birth_month'] == "Unspecified":
        userinfo['birth_month'] = '01'
    if userinfo['birth_year'] == "Unspecified":
        userinfo['birth_year'] = '1800'
    if len(userinfo['birth_month']) == 1:
        userinfo['birth_month'] = '0' + userinfo['birth_month']
    dob = ''.join([userinfo['birth_month'], "01", userinfo['birth_year']])

    # clean up name
    splitname = userinfo['name'].split(' ', 1)
    firstname = splitname[0]
    if len(splitname) == 1:
        # only first or last given, so default as first
        lastname = ""
    else:
        lastname = splitname[1]

    regcode = AMGUT_CONFIG.vioscreen_regcode
    returnurl = "http://microbio.me%s%s" % (media_locale["SITEBASE"],
                                            "/authed/portal/")
    assess_query = ("FirstName=%s&LastName=%s"
                    "&RegCode=%s"
                    "&Username=%s"
                    "&DOB=%s"
                    "&Gender=%d"
                    "&AppId=1&Visit=1&ReturnUrl={%s}" %
                    (firstname, lastname, regcode, survey_id, dob, gender_id,
                     returnurl))

    # PKCS7 add bytes equal length of padding
    pkcs7_query = pkcs7_pad_message(assess_query)

    # Generate AES encrypted information string
    key = AMGUT_CONFIG.vioscreen_cryptokey
    iv = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    encoded = b64encode(iv + cipher.encrypt(pkcs7_query))
    return encoded


def decode_key(encoded):
    """decode AES and remove IV and PKCS#7 padding"""
    key = AMGUT_CONFIG.vioscreen_cryptokey
    iv = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return pkcs7_unpad_message(cipher.decrypt(b64decode(encoded))[16:])
