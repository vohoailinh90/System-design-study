# Acceptance F4

```bash
python3 scripts/check_articles.py --ids sd-01-014,sd-01-015,sd-01-016,sd-01-017
python3 -m unittest discover -s tests -p "test_batch_F4.py"
python3 -m unittest discover -s tests -p "test_check_articles.py"
```
