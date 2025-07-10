
class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.substitution_map = hash_map
        self.rotors = wheels
        self.reflector = reflector_map

    def encrypt(self, message):
        rotor1, rotor2, rotor3 = self.rotors
        encrypted_message = ""
        counter = 0

        for char in message:
            encrypted_char = encrypt_c(char, rotor1, rotor2, rotor3,
                                      self.substitution_map, self.reflector)
            encrypted_message += encrypted_char

            if char.islower():
                counter += 1

            rotor1 += 1
            if rotor1 > 8:
                rotor1 = 1

            rotor2 = rotor2 * 2 if counter % 2 == 0 else rotor2 - 1

            if counter % 10 == 0:
                rotor3 = 10
            elif counter % 3 == 0:
                rotor3 = 5
            else:
                rotor3 = 0

        return encrypted_message
        
        
def encrypt_c(c, W1, W2, W3, hash_map, reflector_map):

    shift = ((2 * W1) - W2 + W3) % 26

    if not c.islower():
        return c

    index = hash_map[c]
    index = (index + shift) if shift != 0 else (index + 1)
    index %= 26

    for key, value in hash_map.items():
        if value == index:
            c1 = key
            break

    c2 = reflector_map[c1]

    index = hash_map[c2]
    index = (index - shift) if shift != 0 else (index - 1)
    index %= 26

    for key, value in hash_map.items():
        if value == index:
            return key

def load_enigma_from_path(path):
    pass
