simulator/build/circuit_pb2.py:
  mkdir -p simulator/build
  protoc -I=simulator/ --python_out=simulator/build/ simulator/circuit.proto
