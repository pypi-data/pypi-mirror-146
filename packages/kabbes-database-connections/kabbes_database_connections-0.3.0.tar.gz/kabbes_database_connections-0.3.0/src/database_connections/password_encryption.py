import datetime
import database_connections.TJEncryptPassword as tj_enc


def custom_decrypt( sPassKeyFileName, sEncPassFileName ):

    return tj_enc.decryptPassword( sPassKeyFileName, sEncPassFileName )

def custom_encrypt( raw_password, passkey_path, encpass_path ):

    sTransformation = 'AES/CBC/NoPadding'
    sKeySizeInBits = '256'
    sMac = 'HmacSHA1'
    sPassKeyFileName = passkey_path
    sEncPassFileName = encpass_path
    sPassword = raw_password

    asTransformationParts = sTransformation.split ("/")
    if len (asTransformationParts) != 3:
        raise ValueError ("Invalid transformation " + sTransformation)

    sAlgorithm = asTransformationParts [0]
    sMode      = asTransformationParts [1]
    sPadding   = asTransformationParts [2]

    if sAlgorithm not in ["DES", "DESede", "AES"]:
        raise ValueError ("Unknown algorithm " + sAlgorithm)

    if sMode not in ["CBC", "CFB", "OFB"]:
        raise ValueError ("Unknown mode " + sMode)

    if sPadding not in ["PKCS5Padding", "NoPadding"]:
        raise ValueError ("Unknown padding " + sPadding)

    if sMac not in ["HmacSHA1", "HmacSHA256"]:
        raise ValueError ("Unknown MAC algorithm " + sMac)

    if not sPassword:
        raise ValueError ("Password cannot be zero length")

    sPassword = sPassword.encode().decode ('unicode_escape') # for backslash uXXXX escape sequences

    nKeySizeInBits = int (sKeySizeInBits)
    sMatch = str (datetime.datetime.now ())

    abyKey, abyMacKey = tj_enc.createPasswordEncryptionKeyFile (sTransformation, sAlgorithm, sMode, sPadding, nKeySizeInBits, sMatch, sMac, sPassKeyFileName)

    tj_enc.createEncryptedPasswordFile (sTransformation, sAlgorithm, sMode, sPadding, sMatch, abyKey, sMac, abyMacKey, sEncPassFileName, sPassword)
    print ('successfully updated password')

    decrypted = custom_decrypt(sPassKeyFileName, sEncPassFileName)

    #print (decrypted)

    assert decrypted == sPassword



if __name__ == '__main__':

    import user_profile
    import py_starter as ps

    raw_password = ps.get_secret_input( prompt = 'Enter your current password: ' )
    custom_encrypt( raw_password, user_profile.profile.encrypted_password_info['passkey_path'], user_profile.profile.encrypted_password_info['encpass_path']  )
