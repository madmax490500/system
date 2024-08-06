# 파일을 읽고 SchemaField로 변환하는 함수
def create_schema_fields(file_path):
    try:
        with open(file_path, 'r') as file:
            # 파일에서 단어들을 읽어옴
            words = [line.strip() for line in file]
    
        # SchemaField 형식으로 변환하여 출력
        for word in words:
            print(f"SchemaField('{word}', 'STRING', 'NULLABLE', None, ()),")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        
        
# 파일 경로 (Same directory)
file_path = 'make_adjust_schema_source.txt'

# 함수 호출
create_schema_fields(file_path)
