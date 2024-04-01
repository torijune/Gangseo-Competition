import os
import openai 
import streamlit as st
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt

def get_openai_response(prompt, api_key):
    if api_key:
        openai.api_key = api_key
    else:
        openai.api_key = "OPENAI_API_KEY"
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",  # gpt-3.5-turbo # gpt-4-1106-preview
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

def get_dong(road_name, api_key):
    
    prompt = f"""
    [작업 지시]
    
    입력된 도로명 주소 또는 지번 주소를 바탕으로 해당 주소가 포함된 행정동을 찾아 출력하세요. 입력 데이터는 정확한 주소 형태로 제공될 것이며, 이를 분석하여 해당 지역의 행정동을 정확히 식별해야 합니다. 결과는 가장 정확하고 구체적인 행정동 명칭으로 제시해야 합니다.

    첫째, 사용자가 제공한 도로명 주소 및 지번 주소 '{road_name}'가 실제로 대한민국에서 속한 행정동에 대해 생각해봅시다.

    해당 주소가 실제로 대한민국의 어떤 행정동에 속해 있을까요? 주어진 주소의 실제 위치를 고려해서 어느 행정동에 속해 있는지 생각해봅시다. 둘째, 주어진 주소들은 모두 대한민국 서울특별시 강서구에 속해 있는 행정동 입니다. 이를 참고하면서 생각해봅시다. 

    너는 이 과정을 거쳐 '{road_name}'가 대한민국 서울특별시 강서구의 어느 행정동에 속해 있는지 찾아주는 AI야. 모든 단계를 거치며 실제로 있는 행정동과 주소를 고려해야하고 정확해야 합니다.


    주어진 프로세스를 통해 다음에 주어지는 2개의 예시와 같은 형태로 {road_name}의 행정동을 정확하게 찾아서 출력하세요.

    예시1)

    [입력 예시1]
    도로명 주소: 서울특별시 강서구 화곡로 320, 지하 1층 (화곡동, 6동)

    [출력 예시1]
    화곡 6동

    예시2)

    [입력 예시2]
    지번 주소: 서울특별시 강서구 화곡동 1117-15 (지하 1층)

    [출력 예시2]
    화곡 6동

    
    """
    dong = get_openai_response(prompt, api_key)
    return dong


def main():
    
    api_key = input("API Key : ")

    csv_file_path =  r'C:\Users\dnjsw\Desktop\데이터 분석 개인 프젝\2024 강서구 빅데이터 분석 공모전\Gangseo-Competition-main\DB\위험도 데이터\서울시 강서구 유흥주점영업 인허가 정보.csv'

    output_csv_file_path = "result.csv"

    df = pd.read_csv(csv_file_path)
    road_name = input("지번 주소 및 도로명 주소를 입력하세요. :")

    if '지번주소' in df.columns:
        results = []
        for road_name in df['지번주소']:
            # 각 road_name에 대해 get_dong 함수를 호출합니다.

            dong = get_dong(road_name, api_key)

             # 결과를 리스트에 추가합니다.
            results.append({'road_name': road_name, 'dong': dong})

        # 결과를 DataFrame으로 변환합니다.
        results_df = pd.DataFrame(results)

        # 결과 DataFrame을 CSV 파일로 저장합니다.
        results_df.to_csv(output_csv_file_path, index=False)
        print(f"결과가 '{output_csv_file_path}' 파일에 저장되었습니다.")
    else:
        print("CSV 파일에 'road_name' 컬럼이 없습니다.")

if __name__ == '__main__':
    main()
