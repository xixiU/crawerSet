import pandas as pd
import os
import concurrent.futures
from osta import getScoreOnce
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit
import sys

# 查询单个成绩的函数
def query_single_score(name, cardNo, certificateNo):
    # 查询成绩
    result = getScoreOnce(name, cardNo, certificateNo)
    if result:
        return result
    else:
        # 返回查询失败的信息
        return {
            "name": name,
            "cardNo": cardNo,
            "certificateNo": certificateNo,
            "status": f"{name} 没有查询到"
        } 

# 多线程查询函数
def query_scores_from_excel(df:pd.DataFrame):
    # 从Excel文件中读取数据
    # 假设Excel中有姓名、身份证号和证书编号这几列
    results = []

    # 使用ThreadPoolExecutor进行多线程查询
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交任务到线程池
        future_to_score = {
            executor.submit(query_single_score, name=row['姓名'], cardNo=row['身份证号'], certificateNo=row['证书编号']): index 
            for index, row in df.iterrows()
        }

        # 获取查询结果
        for future in concurrent.futures.as_completed(future_to_score):
            index = future_to_score[future]
            try:
                score = future.result()
                results.append(score)
            except Exception as exc:
                print(f"在查询第 {index} 行数据时发生异常: {exc}")
                results.append({
                    "name": df.iloc[index]["姓名"],
                    "cardNo": df.iloc[index]["身份证号"],
                    "certificateNo": df.iloc[index]["证书编号"],
                    "status": f"{df.iloc[index]['姓名']} 暂未获取到成绩"
                })
    
    return results

# 使用PyQt创建一个界面，支持用户选择Excel文件并展示结果
class ScoreQueryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # 文件选择按钮
        self.btn = QPushButton('选择Excel文件', self)
        self.btn.clicked.connect(self.openFileDialog)
        layout.addWidget(self.btn)

        # 显示查询结果的文本框
        self.textEdit = QTextEdit(self)
        layout.addWidget(self.textEdit)
        
         # 导出按钮
        self.exportBtn = QPushButton('导出查询结果', self)
        self.exportBtn.clicked.connect(self.exportResults)
        layout.addWidget(self.exportBtn)

        self.setLayout(layout)
        self.setWindowTitle('成绩查询')
        self.show()

    def openFileDialog(self):
        # 打开文件对话框，选择Excel文件
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "", "Excel Files (*.xls *.xlsx)", options=options)
        if file_path:
            # 查询成绩并展示
            self.df = pd.read_excel(file_path).fillna('')
            self.results = query_scores_from_excel(self.df)
            self.displayResults(self.results)

    def displayResults(self, results):
        # 清空当前结果
        self.textEdit.clear()
        print(results)
        for result in results:
            if "status" in result:
                # 如果有查询失败的记录
                self.textEdit.append(f"{result['status']}\n")                
            else:
                # 假设结果格式为{'name': 'XXX', 'cardNo': 'XXXX', 'certificateNo': 'XXXX'}
                self.textEdit.append(f"姓名: {result['name']}, 证书编号: {result['certificateNo']}, 身份证号: {result['cardNo']}\n")
    
    def exportResults(self):
        if not self.results:
            self.textEdit.append("没有查询结果，无法导出。")
            return
        
        # 打开文件对话框，选择保存路径
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "选择保存路径", "", "Excel Files (*.xlsx);;CSV Files (*.csv)", options=options)
        
        if save_path:
            # 将结果转换为DataFrame
            df = pd.DataFrame(self.results)
            # 保存文件，根据扩展名选择保存格式
            if save_path.endswith('.xlsx'):
                df.to_excel(save_path, index=False)
            elif save_path.endswith('.csv'):
                df.to_csv(save_path, index=False, encoding='utf-8-sig')
            
            self.textEdit.append(f"查询结果已成功导出到: {save_path}")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ScoreQueryApp()
    sys.exit(app.exec_())
