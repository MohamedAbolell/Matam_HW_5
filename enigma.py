import json
import sys

class JSONFileException(Exception):
    pass

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

    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        raise JSONFileException(f"Could not load a valid Enigma JSON file from: {path}")

    required_fields = ['hash_map', 'wheels', 'reflector_map']
    for field in required_fields:
        if field not in data:
            raise JSONFileException(f"Missing required field: {field}")

    substitution_map = data['hash_map']
    rotors = data['wheels']
    reflector = data['reflector_map']

    return Enigma(substitution_map, rotors, reflector)

def print_usage_and_exit():

    print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>")
    sys.exit(1)

if __name__ == "__main__":
    try:
        if len(sys.argv) < 5:
            print_usage_and_exit()

        config_file = None
        input_file = None
        output_file = None

        i = 1
        while i < len(sys.argv):
            flag = sys.argv[i]

            if flag not in ['-c', '-i', '-o']:
                print_usage_and_exit()

            if i + 1 >= len(sys.argv):
                print_usage_and_exit()

            value = sys.argv[i + 1]
            if flag == '-c':
                config_file = value
            elif flag == '-i':
                input_file = value
            elif flag == '-o':
                output_file = value

            i += 2

        if not config_file or not input_file:
            print_usage_and_exit()

        try:
            with open(input_file, 'r') as input_f:
                lines = input_f.readlines()

            enigma_machine = load_enigma_from_path(config_file)

            encrypted_lines = [enigma_machine.encrypt(line.rstrip('\n')) for line in lines]
            encrypted_message = '\n'.join(encrypted_lines) + '\n'

            if output_file:
                with open(output_file, 'w') as output_f:
                    output_f.write(encrypted_message)
            else:
                print(encrypted_message)

        except Exception:
            print("The enigma script has encountered an error")
            sys.exit(1)

    except SystemExit:
        raise
    except:
        print("The enigma script has encountered an error")
        sys.exit(1)
