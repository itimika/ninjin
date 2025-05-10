import gspread
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import GoogleCredentials
from gspread_formatting import (
    get_conditional_format_rules,
    ConditionalFormatRule,
    BooleanRule,
    BooleanCondition,
    CellFormat,
    Color,
    GridRange
)

class SheetHandler:
    def __init__(self):
        # スコープの設定
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

        # 認証情報の読み込み
        credentials = ServiceAccountCredentials.from_json_keyfile_name('authorized_user.json', scope)

        # gspreadでGoogle Sheetsへアクセス
        gc = gspread.authorize(credentials)
        self.wb = gc.open_by_key('1SeWpqaUK8xejo4tKhz9rwSv0YUa00vMq0-oglHVKYZs')
    
    def append_row(self, sheet_name, values):
        # 既にその野菜シートがある場合
        try:
            ws = self.wb.worksheet(sheet_name)
            # 既に同じ日付の行があれば更新しないで終了する
            all_values = ws.get_all_values()
            found = any(values[0] in cell for row in all_values for cell in row)
            if found:
              return
            # 同じ日付の行がなければ、データを追記する
            ws.append_row(values)
            
        # その野菜シートがない場合
        except:
            # シートを追加する
            self.wb.add_worksheet(title=sheet_name, rows="100", cols="100")
            ws = self.wb.worksheet(sheet_name)
            
            #データを追記する
            ws.append_row(["公開日", "平均相場（円/kg）", "前市比（%）", "高値（円/kg）","中値（円/kg）","安値（円/kg）","総入荷量（t）", "見通し", "平年相場"])
            ws.append_row(values)
            
            ws = self.wb.worksheet("平均相場一覧")
            ws.append_row([sheet_name, ""])
            # 数式をI2に挿入
            ws = self.wb.worksheet(sheet_name)
            formula = "=VLOOKUP(Sheetname(), '平均相場一覧'!A:B, 2, FALSE)"
            ws.update_acell("I2", formula)
                
            self._set_rules(ws)
    
    def _set_rules(self, ws):
        # 背景色の定義
        light_red3 = Color(red=1, green=0.8, blue=0.8)
        light_green3 = Color(red=0.8, green=1, blue=0.8)
        
        # 条件付き書式のルールを取得
        rules = get_conditional_format_rules(ws)

        # 既存のルールをクリア（必要に応じて）
        rules.clear()

        # 設定1のルールを作成
        rule1 = ConditionalFormatRule(
            ranges=[GridRange.from_a1_range('B2:B1000', ws)],
            booleanRule=BooleanRule(
                condition=BooleanCondition('CUSTOM_FORMULA', ['=AND($B2>=$I$2, $B2<>"")']),
                format=CellFormat(backgroundColor=light_red3)
            )
        )

        # 設定2のルールを作成
        rule2 = ConditionalFormatRule(
            ranges=[GridRange.from_a1_range('B2:B1000', ws)],
            booleanRule=BooleanRule(
                condition=BooleanCondition('CUSTOM_FORMULA', ['=AND($B2<$I$2, $B2<>"")']),
                format=CellFormat(backgroundColor=light_green3)
            )
        )

        # ルールを追加
        rules.append(rule1)
        rules.append(rule2)

        # ルールを保存
        rules.save()