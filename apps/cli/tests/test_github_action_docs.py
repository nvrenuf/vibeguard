from pathlib import Path


def test_reusable_action_and_docs_exist() -> None:
    action_path = Path('.github/actions/vibeguard/action.yml')
    docs_path = Path('docs/GITHUB_ACTION.md')

    assert action_path.exists()
    assert docs_path.exists()

    action_text = action_path.read_text(encoding='utf-8')
    assert 'using: composite' in action_text
    assert 'policy_path' in action_text
    assert 'fail_on' in action_text
    assert 'format' in action_text

    docs_text = docs_path.read_text(encoding='utf-8')
    assert 'uses: nvrenuf/vibeguard/.github/actions/vibeguard@<tag-or-sha>' in docs_text
