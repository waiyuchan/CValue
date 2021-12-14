from cvalue import CValue

if __name__ == '__main__':
    input_path = "demo_corpus.txt"
    output_path = "result_of_txt.csv"
    CValue(input_path, output_path)

    input_path = "demo_corpus.csv"
    output_path = "result_of_csv.csv"
    CValue(input_path, output_path)
