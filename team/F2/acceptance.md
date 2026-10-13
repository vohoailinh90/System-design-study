# Acceptance F2

```bash
python3 scripts/check_articles.py --ids sd-01-006,sd-01-007,sd-01-008,sd-01-009
python3 -m unittest discover -s tests -p "test_batch_F2.py"
python3 -m unittest discover -s tests -p "test_check_articles.py"
```
