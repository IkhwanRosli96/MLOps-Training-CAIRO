import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--data_input', type=str)
parser.add_argument('--model_output', type=str)

args = parser.parse_args()
arguments = args.__dict__

input_file = arguments['data_input']
output_file = arguments['model_output']