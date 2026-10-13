# Acceptance F3

```bash
python3 scripts/check_articles.py --ids sd-01-010,sd-01-011,sd-01-012,sd-01-013
python3 -m unittest discover -s tests -p "test_batch_F3.py"
python3 -m unittest discover -s tests -p "test_check_articles.py"
```
