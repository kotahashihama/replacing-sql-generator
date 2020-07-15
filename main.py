# import csv
import pandas as pd
import re

csv_file_name = 'test.csv'
site_url = 'https://www.google.com/'

# 記事タイプの区切り文字
delimiter = '・'

# 行の抽出範囲
row_from = 12
row_to = 29

# 記事タイプの列番号
line_article_type = 1

# 置換後文字列の列番号
line_before_replacement = 3

# 置換後文字列の列番号
line_after_replacement = 5

df = pd.read_csv(csv_file_name)
csv_array = df.iloc[row_from:row_to, [1, 3, 5]].values.tolist()

# 確認用
# print(csv_array)

types_array = []

for row in csv_array:
  if (row[0].startswith(site_url)):
    type_extracted = re.findall('^https://kekkon.kuraveil.jp/(.+)/.*$', row[0])
    row[0] = type_extracted
  else:
    delimited = row[0].split(delimiter)
    row[0] = delimited

all_text = ''

for i, item in enumerate(csv_array):
  types = ', '.join(map(lambda x: f"'{x}'", item[0]))
  before_replacement_for_like = item[1].replace('%', '\%').replace('_', '\_')
  after_replacement_for_like = item[1].replace('%', '\%').replace('_', '\_')

  before_after_text = '''
# Before: {before_replacement}
# After: {after_replacement}
'''.format(before_replacement=item[1], after_replacement=item[2]).strip()


  sql_update = '''
# 置換
UPDATE
    markdown_articles
SET
    body = REPLACE(
        body,
        '{before_replacement}',
        '{after_replacement}'
    )
WHERE
    body LIKE '%{before_replacement_for_like}%'
AND
    type in ({types})
;
'''.format(types=types, before_replacement=item[1], after_replacement=item[2], before_replacement_for_like=before_replacement_for_like).strip()

  sql_before = '''
# 置換前件数チェック
SELECT
    count(id)
FROM
    markdown_articles
WHERE
    type in ({types})
AND
    body LIKE '%{before_replacement_for_like}%'
;
'''.format(types=types, before_replacement_for_like=before_replacement_for_like).strip()

  sql_after = '''
# 置換後件数チェック
SELECT
    count(id)
FROM
    markdown_articles
WHERE
    type in ({types})
AND
    body LIKE '%{after_replacement_for_like}%'
;
'''.format(types=types, after_replacement_for_like=after_replacement_for_like).strip()

  all_text += '\n' * 3 + f'# ({i + 1}/{len(csv_array)})' + '\n'
  all_text += before_after_text + '\n' * 2
  all_text += '# トランザクション開始\nSTART TRANSACTION;' + '\n' * 2
  all_text += sql_before + '\n' * 2
  all_text += sql_update + '\n' * 2
  all_text += sql_after + '\n' * 2

  all_text += '''
# 問題なければ
COMMIT;

# 間違いがあれば
ROLLBACK;
'''.strip()

with open('generated_sql.txt', 'w') as f:
  print(all_text.strip(), file=f)
