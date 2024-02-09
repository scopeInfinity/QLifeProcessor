from build import circuit_pb2
from google.protobuf import text_format
import runner
import argparse

def parse_args():
    parser = argparse.ArgumentParser(prog='Circuit Simulator')
    parser.add_argument('circuit', type=argparse.FileType('rb'))
    return parser.parse_args()

def get_circuit(file):
    textpb = file.read()
    circuit = text_format.Parse(textpb, circuit_pb2.Circuit())
    return circuit

def main():
    args = parse_args()
    circuit = get_circuit(args.circuit)
    runner.Sim(circuit).run()

if __name__ == '__main__':
    main()
