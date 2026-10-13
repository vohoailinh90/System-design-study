# Acceptance F1

```bash
python3 scripts/check_articles.py --ids sd-01-002,sd-01-003,sd-01-004,sd-01-005
python3 -m unittest discover -s tests -p "test_batch_F1.py"
python3 -m unittest discover -s tests -p "test_check_articles.py"
```
