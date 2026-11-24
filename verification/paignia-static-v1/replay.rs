#[test]
fn frozen_static_v1_result_matches_exactly() {
    let request = include_bytes!("request.json");
    let expected = include_str!("result.json");
    let mut result = paignia_io::solve_static_json(request).expect("solve the frozen v1 request");
    result.push(b'\n');
    assert_eq!(
        std::str::from_utf8(&result).expect("wire result is UTF-8"),
        expected
    );
}
