function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
$(() => {
  // 연봉/월급 입력시 값으
  $("#salary, #taxfree").on("input", (e) => {
    // 숫자 이외의 값이 들어오면 '' 빈 문자열로 대체
    const input = e.target.value.toString().replace(/\D/g, "");
    // 사용자가 입력한 숫자를 시각적으로 보기 좋게 100단위로 컴마 삽입
    e.target.value = numberWithCommas(Number(input));
  });
  
  // 부양가족수 정규식과 min max
  $("#dependents").on("input", (e) => {
    let input = e.target.value.toString().replace(/\D/g, "");
    if (input < 1) {
      input = 1;
    } else if (input > 11) {
      input = 11;
    }
    e.target.value = Number(input);
  });
  // 예상 실수령액

  // 급여기준 연봉, 월급 클릭 시 퇴직금 활성, 비활성화
  $("#sal-year").on("click", () => {
    $(".btn-group2 > input").first().prop("checked", true);
    $(".btn-group2 > label")
      .removeClass("disabled")
      .removeClass("btn-secondary")
      .addClass("btn-outline-primary");
    $(".sal-title").text("연봉");
  });
  $("#sal-month").on("click", () => {
    $(".btn-group2 > input").prop("checked", false);
    $(".btn-group2 > label")
      .addClass("disabled")
      .addClass("btn-secondary")
      .removeClass("btn-outline-primary");
    $(".sal-title").text("월급");
  });
});
