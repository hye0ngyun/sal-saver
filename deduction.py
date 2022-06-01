#-*-coding:utf-8-*-
# 세전 월급을 입력하면 세금을 계산하여 세후 금액을 구하는 모듈
# 공제(Deduction): 사전적 의미로 일정 금액, 수량 등을 뺀다는 뜻
import pandas as pd
# from get_income_tax import get_income_tax
import sys
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


def truncate(n):
    return int(round(n / 10) * 10)


def get_income_tax(salary, dependents):
  """
  salary: 월급
  dependents: 부양가족
  """
  df = pd.read_excel('./modified_simple_tax_amount_table.xls')
  base_salary = int(salary / 1000) # 엑셀 시트 단위가 천으로 돼있기때문
  # 월급이 10,000천원 초과하는 경우 엑셀시트에 명시된 계산으로 소득세 계산
  income_tax = 0
  if 10000 < base_salary <= 14000:
    income_tax = df.iloc[-1][dependents] + ((base_salary - 10000) * 1000) * (98/100) * (35/100) # 10,000천원 행, 부양가족수 열에 해당하는 소득세 + 10,000천원을 초과하는 금액에 98%를 곱한 금액의 35퍼센트 상당액
    #  ((base_salary - 10000) * 1000) ==> 엑셀 시트 단위 변환을 위해 1000 곱해서 초과액 구하기
  elif 14000 < base_salary <= 28000:
    income_tax = df.iloc[-1][dependents] + 1372000 + ((base_salary - 14000) * 1000) * (98/100) * (38/100)
  elif 28000 < base_salary <= 30000:
    income_tax = df.iloc[-1][dependents] + 6585600 + ((base_salary - 28000) * 1000) * (98/100) * (40/100)
  elif 30000 < base_salary <= 45000:
    income_tax = df.iloc[-1][dependents] + 7369600 + ((base_salary - 30000) * 1000) * (40/100)
  elif 45000 < base_salary <= 87000:
    income_tax = df.iloc[-1][dependents] + 13369600 + ((base_salary - 45000) * 1000) * (42/100)
  elif 87000 < base_salary:
    income_tax = df.iloc[-1][dependents] + 31009600 + ((base_salary - 87000) * 1000) * (45/100)
  else:
    income_tax = df[df['미만'] > base_salary].iloc[0][dependents] # df[df['미만'] > base_salary].iloc[0] - base_salary에 해당하는 행 선택, [dependents] - 부양가족수에 해당하는 열 선택 ==> 월급에 해당하는 행에서 부양가족수에 해당하는 열의 소득세
  
  # 소득세 반환
  return income_tax

def get_deduction(salary, dependents, taxfree, get_list=True):
  salary = int(salary)
  dependents = int(dependents)
  taxfree = int(taxfree)
  # 비과세액 적용
  salary = salary - taxfree
  # 국민연금은 월 소득액(비과세액 제외)에서 4.5%를 공제한다.
  # 월 최저금액 28만원, 최고금액 449만원으로 과세한다.
  # 즉, 최저 월급 28만원에서 449만원 까지 과세비율이 달라진다.
  if 280000 <= salary <= 4990000:
    국민연금 = salary * 0.045
  elif salary <= 280000:
    국민연금 = 280000 * 0.045
  elif salary > 4990000:
    국민연금 = 4990000 * 0.045

  # 건강보험은 월 소득액(비과세액 제외)에서 3.06%를 공제한다.
  if 280000 <= salary <= 78100000:
    건강보험 = salary * 0.0343
  elif salary <= 280000:
    건강보험 = 280000 * 0.0343
  elif salary > 78100000:
    건강보험 = 4990000 * 0.0343

  # 장기요양보험은 건강보험금액에서 6.55%를 공제한다.
  장기요양 = round(건강보험 * 0.01152) * 10

  # 고용보험은 월 소득액(비과세액 제외)에서 0.65%를 공제합니다.
  고용보험 = salary * 0.008

  # 소득세는 급여와 부양가족수에 따라 국세청의 근로소득 간이세액표 자료를 기준으로 공제한다.
  # 부양가족수는 기본공제대상자(본인 포함)에 해당하는 부양가족의 수이다.
  # 단, 부양가족은 연간 소득금액이 100만원을 초과하는 경우에는 해당하지 않는다.
  dependents = 1
  소득세 = get_income_tax(salary, dependents)
  # 지방소득세는 소득세의 10%를 공제한다.
  지방소득세 = 소득세 * 0.1


  공제금액 = {
    "국민연금": 국민연금,
      "건강보험": 건강보험,
      "장기요양": 장기요양,
      "고용보험": 고용보험,
      "소득세": 소득세,
      "지방소득세": 지방소득세,
  }

  공제금액 = {k: truncate(v) for k, v in 공제금액.items()}
  
  # if get_list:
  #   return 국민연금, 건강보험, 장기요양, 고용보험, 소득세, 지방소득세
  return 공제금액



if __name__ == '__main__':
  # import pandas as pd
  # df = pd.read_excel('./modified_simple_tax_amount_table.xls')
  # base_salary = 200000
  # dependents = 1
  # income_tax = df.iloc[-1][dependents] + 1372000 + (base_salary - 14000) * (98/100) * (38/100)
  # print(income_tax)
  
  money = '2,000,000'

  money = int(money.replace(',', ''))

  # 국민연금은 월 소득액(비과세액 제외)에서 4.5%를 공제한다.
  # 월 최저금액 28만원, 최고금액 449만원으로 과세한다.
  # 즉, 최저 월급 28만원에서 449만원 까지 과세비율이 달라진다.
  if 280000 <= money <= 4990000:
    국민연금 = money * 0.045
  elif money <= 280000:
    국민연금 = 280000 * 0.045
  elif money > 4990000:
    국민연금 = 4990000 * 0.045

  # 건강보험은 월 소득액(비과세액 제외)에서 3.06%를 공제한다.
  if 280000 <= money <= 78100000:
    건강보험 = money * 0.0343
  elif money <= 280000:
    건강보험 = 280000 * 0.0343
  elif money > 78100000:
    건강보험 = 4990000 * 0.0343

  # 장기요양보험은 건강보험금액에서 6.55%를 공제한다.
  장기요양 = round(건강보험 * 0.01152) * 10

  # 고용보험은 월 소득액(비과세액 제외)에서 0.65%를 공제합니다.
  고용보험 = money * 0.008

  # 소득세는 급여와 부양가족수에 따라 국세청의 근로소득 간이세액표 자료를 기준으로 공제한다.
  # 부양가족수는 기본공제대상자(본인 포함)에 해당하는 부양가족의 수이다.
  # 단, 부양가족은 연간 소득금액이 100만원을 초과하는 경우에는 해당하지 않는다.
  부양가족 = 1
  소득세 = get_income_tax(money, 부양가족)
  # 지방소득세는 소득세의 10%를 공제한다.
  지방소득세 = 소득세 * 0.1

  공제금액 = 국민연금 + 건강보험 + 장기요양 + 고용보험 + 소득세 + 지방소득세

  세후금액 = money - 공제금액

  print(f'공제액 합계: {공제금액}')
  print(f'국민연금: {국민연금}\n건강보험: {건강보험}\n장기요양: {장기요양}\n고용보험: {고용보험}\n소득세: {소득세}\n지방소득세: {지방소득세}')
  print(f'세후금액: {세후금액}')

