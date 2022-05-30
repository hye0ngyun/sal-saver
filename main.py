from deduction import *
from re import *
def numberWithCommas(x):
  return format(x, ',')

def calculate(*args):
  # 부양가족 수
  dependents = Element('dependents').value
  # 비과세액
  taxfree = int(Element('taxfree').value.replace(',', ''))
  # 세전월급
  el_before_tax_salary = Element('salary')
  before_tax_salary = el_before_tax_salary.value
  before_tax_salary = int(before_tax_salary.replace(',', ''))

  # 급여기준
  sal_year = Element('sal-year').element.checked
  severance_pay = Element('severance-pay-false').element.checked

  # 연봉, 별도
  if sal_year and severance_pay:
    before_tax_salary //= 12
  # 연봉, 포함
  elif sal_year and not severance_pay:
    before_tax_salary //= 13

  # 세전월급과 부양가족수로 각 공제금 구하기
  deductions = get_deduction(before_tax_salary, dependents, taxfree)

  el_deductions = Element('deductions')
  # 실수령 금액
  result = Element('result')
  result.element.innerText = numberWithCommas(before_tax_salary - sum(deductions.values()))

  # 공제금 총합
  el_deductions.element.innerText = numberWithCommas(sum(deductions.values()))

  # 항목별 공제금
  Element('국민연금').element.innerText = numberWithCommas(deductions['국민연금'])
  Element('건강보험').element.innerText = numberWithCommas(deductions['건강보험'])
  Element('장기요양').element.innerText = numberWithCommas(deductions['장기요양'])
  Element('고용보험').element.innerText = numberWithCommas(deductions['고용보험'])
  Element('소득세').element.innerText = numberWithCommas(deductions['소득세'])
  Element('지방소득세').element.innerText = numberWithCommas(deductions['지방소득세'])
