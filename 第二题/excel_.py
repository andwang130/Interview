import xlrd
'''
读取excle文件'''
def get_data(path):
    data = xlrd.open_workbook(path) #打开excel文件
    table = data.sheet_by_index(0)
    norws = table.nrows
    for i in range(1,norws):#读取每一行
        valeu=table.row_values(i)
        # conten=valeu[4]  #第4个元素，谁文章内容
        # title=valeu[5]     #第5个元素，是标题
        yield valeu  #生成器
       



